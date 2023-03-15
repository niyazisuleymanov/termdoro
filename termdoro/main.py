#!/usr/bin/env python3
from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
from bullet import Numbers
from collections import defaultdict
from configparser import ConfigParser
from curses import curs_set, error, use_default_colors, wrapper
from datetime import datetime, timedelta
from dateutil.parser import parse, ParserError
from enum import Enum
from math import floor
from os import system
from os.path import dirname, join, isfile
from platform import system as os_name
from playsound import playsound
from pyfiglet import Figlet
from re import compile, fullmatch
from shutil import get_terminal_size
from signal import signal, SIGINT
from sqlite3 import connect, Connection, Cursor
from sys import exit
from time import time as t_time, mktime, localtime, sleep
from typing import List, Optional, Tuple

VERSION = "v2.0.0"

TIMEDELTA_REGEX = compile(r'((?P<years>\d+)y ?)?'
                          r'((?P<days>\d+)d ?)?'
                          r'((?P<hours>\d+)h ?)?'
                          r'((?P<minutes>\d+)m ?)?'
                          r'((?P<seconds>\d+)s ?)?')


def parse_time(time: str) -> Optional[int]:
  try:
    return int(time)
  except ValueError:
    seconds = duration_parser(time)
    if seconds is not None:
      return seconds

    seconds = datetime_parser(time)
    if seconds is not None:
      return seconds

    return None


def duration_parser(time: str) -> Optional[int]:
  matches = fullmatch(TIMEDELTA_REGEX, time)
  if not matches:
    return None

  components = defaultdict(int)
  for key, value in matches.groupdict().items():
    if value is None:
      continue

    if key != "years":
      components[key] += int(value)
    else:
      components["days"] += int(value) * 365

  return floor(timedelta(**components).total_seconds())


def datetime_parser(time: str) -> Optional[int]:
  try:
    to_time = mktime(parse(time).timetuple())
  except ParserError:
    return None

  now = mktime(localtime(t_time()))

  if now >= to_time:
    return None

  return floor(to_time - now)


def format(time: int) -> str:
  seconds, formatted_seconds = time, ""

  for period, period_seconds in (
      ('y', 31557600),
      ('d', 86400),
      ('h', 3600),
      ('m', 60),
      ('s', 1),
  ):
    if (seconds >= period_seconds):
      formatted_seconds += str(int(seconds / period_seconds))
      formatted_seconds += period
      formatted_seconds += " "
      seconds = seconds % period_seconds
  return formatted_seconds.rstrip()


def pad_text(text: str, x: int, y: int) -> str:
  f = Figlet(font="univers", width=x)
  lines = f.renderText(text).split("\n")

  longest_input_line = max(map(len, lines))
  number_of_input_lines = len(lines)

  if x < longest_input_line or y < number_of_input_lines:
    longest_input_line = len(text)
    number_of_input_lines = 1
    lines = [text]

  padding_top = int((y - number_of_input_lines) / 2) + 1
  padding_left = int((x - longest_input_line) / 2)
  padding_bottom = y - number_of_input_lines - padding_top

  output = padding_top * (" " * x + "\n")
  for line in lines:
    padding_right = x - len(line) - padding_left
    output += padding_left * " " + line + padding_right * " " + "\n"
  output += padding_bottom * (" " * x + "\n")
  return output


CONFIG_PATH = join(dirname(__file__), 'termdoro.cfg')


def is_config_created() -> bool:
  return True if isfile(CONFIG_PATH) else False


def create_default_config() -> None:
  if is_config_created is True:
    return

  config = ConfigParser()
  config["DEFAULT"] = {
      'sessions': "6",
      'work_time': f"{25 * 60}",
      'break': f"{5 * 60}",
      'long_break': f"{15 * 60}",
      'long_break_timing': "4"
  }
  with open(CONFIG_PATH, 'w') as config_file:
    config.write(config_file)


def read_config() -> List[int]:
  if is_config_created is False:
    create_default_config()

  config = ConfigParser()
  config.read(CONFIG_PATH)

  default = config["DEFAULT"]

  sessions = int(default["sessions"])
  work_time = int(default["work_time"])
  short_break = int(default["break"])
  long_break = int(default["long_break"])
  long_break_timing = int(default["long_break_timing"])

  config_list = []
  for i in range(2 * sessions - 1):
    if i % 2 == 0:
      config_list.append(work_time)
    elif (i // 2 + 1) % long_break_timing == 0:
      config_list.append(long_break)
    else:
      config_list.append(short_break)
  return config_list


def change_config() -> None:
  if is_config_created is False:
    create_default_config()

  cli = Numbers('Sessions: ', type=int)
  sessions = cli.launch()
  cli = Numbers('Work time (in mins): ', type=int)
  work_time = cli.launch()
  cli = Numbers('Break time (in mins): ', type=int)
  break_time = cli.launch()
  cli = Numbers('Long break time (in mins): ', type=int)
  long_break = cli.launch()
  cli = Numbers('Long break timing: ', type=int)
  long_break_timing = cli.launch()

  config = ConfigParser()
  config['DEFAULT'] = {
      'sessions': str(sessions),
      'work_time': f"{work_time * 60}",
      'break': f"{break_time * 60}",
      'long_break': f"{long_break * 60}",
      'long_break_timing': str(long_break_timing)
  }

  with open(CONFIG_PATH, 'w') as config_file:
    config.write(config_file)


def init_db() -> Tuple[Cursor, Connection]:
  db_path = join(dirname(__file__), 'termdoro.db')
  connection = connect(db_path)
  cursor = connection.cursor()
  cursor.execute(f"CREATE TABLE IF NOT EXISTS history ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        start_date TEXT, \
        work_time INTEGER, \
        break_time INTEGER, \
        end_date TEXT \
    )")
  connection.commit()
  return (cursor, connection)


def store(start_date: datetime, work_time: int, break_time: int) -> None:
  if work_time == 0:
    return

  end_date = start_date + timedelta(seconds=work_time + break_time)

  start_date_str = start_date.strftime("%H:%M:%S %-d %B, %Y")
  end_date_str = end_date.strftime("%H:%M:%S %-d %B, %Y")

  cursor, connection = init_db()
  cursor.execute('INSERT INTO history VALUES (?, ?, ?, ?, ?)',
                 (None, start_date_str, work_time, break_time, end_date_str))
  connection.commit()


def print_history() -> None:
  cursor, _ = init_db()
  res = cursor.execute("SELECT * FROM history")
  history = res.fetchall()

  if len(history) == 0:
    print("no recorded history yet. start your first session\n")
    parser.print_help()
  for record in history:
    start_date = datetime.strptime(record[1], "%H:%M:%S %d %B, %Y")
    work_time = format(int(record[2]))
    break_time = format(int(record[3])) if int(record[3]) > 0 else "no"
    end_date = datetime.strptime(record[4], "%H:%M:%S %d %B, %Y")

    if (start_date.year == end_date.year and
        start_date.month == end_date.month and start_date.day == end_date.day):
      start_time = start_date.strftime("%H:%M:%S")
      interval = f"{start_time} - {record[4]}"  # same day interval
      print(f"spent {work_time} working with {break_time} break [{interval}]")
    else:
      interval = f"[{record[1]} - {record[4]}]"  # interval spanning two days
      print(f"spent {work_time} working with {break_time} break [{interval}]")


class Mode(Enum):
  POMODORO = 1
  COUNTDOWN = 2


class Session:

  def __init__(self,
               time: str,
               notify: bool,
               play_sound: bool,
               sound_to_play: Optional[str] = None) -> None:
    if is_config_created() is False:
      create_default_config()

    self.notify = notify
    self.play_sound = play_sound

    if play_sound is True:
      if sound_to_play is None:
        sound_path = join(dirname(__file__), "termdoro.mp3")
        self.sound_to_play = sound_path
      else:
        self.sound_to_play = sound_to_play

    if time is None:
      self.sessions: List[int] = read_config()
      self.mode = Mode.POMODORO
    else:
      session = parse_time(time)
      if session is None:
        parser.print_help()
        exit(1)
      else:
        self.sessions: List[int] = [session]
      self.mode = Mode.COUNTDOWN

    self.current_session = 0
    self.start_date = datetime.now()
    self.work_time = 0
    self.break_time = 0
    self.done = False

  def alarm(self) -> None:
    if self.notify is True:
      if self.current_session % 2 == 0:
        if len(self.sessions) - 1 == self.current_session:
          title = "All sessions done!"
          message = "Now go touch some grass."
        else:
          title = "Break time!"
          time = format(self.sessions[self.current_session + 1])
          message = f"Take a {time} break."
      else:
        title = "Work time!"
        time = format(self.sessions[self.current_session + 1])
        message = f"Work for {time}."

      if os_name() == "Linux":
        icon_path = join(dirname(__file__), "termdoro.png")
        command = f"notify-send -i {icon_path} '{title}' '{message}'"
        system(command)
      elif os_name() == "Darwin":
        command = f"""
          osascript -e 'display notification "{message}" with title "{title}"'
        """
        system(command)

      # TODO: add Windows support (maybe)

    if self.play_sound is True:
      playsound(self.sound_to_play, block=False)

  def step(self) -> None:
    if self.current_session % 2 == 0:
      self.work_time += 1
    else:
      self.break_time += 1

    if self.mode is Mode.POMODORO:
      if self.sessions[self.current_session] - 1 == 0:
        self.alarm()

        if self.current_session < len(self.sessions) - 1:
          self.current_session += 1
        else:
          store(self.start_date, self.work_time, self.break_time)
          self.done = True
      else:
        self.sessions[self.current_session] -= 1
    elif self.mode is Mode.COUNTDOWN:
      if self.sessions[self.current_session] - 1 == 0:
        self.alarm()
        store(self.start_date, self.work_time, self.break_time)
        self.done = True
      else:
        self.sessions[self.current_session] -= 1

  def sigint_handler(self, signal, frame) -> None:
    store(self.start_date, self.work_time, self.break_time)
    exit(1)

  def _draw(self, stdscr) -> None:
    signal(SIGINT, self.sigint_handler)

    use_default_colors()
    try:
      curs_set(False)
    except error:
      # fails on some terminals
      pass

    while self.done is False:
      stdscr.clear()

      # BUG: stdscr.getmaxyx() never updates; maybe sleep(1) is the issue
      x, y = get_terminal_size()
      time = format(self.sessions[self.current_session])
      text = pad_text(time, x - 1, y - 1)

      try:
        stdscr.addstr(text)
      except:
        pass
      stdscr.refresh()

      # TODO: replace sleep with continuous time update:
      #       int(ceil((target - datetime.now()).total_seconds()))
      #       after adding continuous time update input keys will be snappier
      sleep(1)

      self.step()

    # guarantee that the sound alarm goes off after the last session ends
    # playsound is not blocked and program finishes before alarm sound plays
    stdscr.clear()
    x, y = get_terminal_size()
    done = pad_text("done!", x - 1, y - 1)

    # TODO: rather than hardcoding loop duration set it to (audio_length + 5s)
    #       if no alarm sound is enabled set it to 10s
    end_time = t_time() + 15
    while t_time() < end_time:
      try:
        stdscr.addstr(done)
      except:
        pass
      stdscr.refresh()

  def draw(self) -> None:
    wrapper(self._draw)


def is_valid_file(parser: ArgumentParser, arg: str) -> str:
  if isfile(arg) is False:
    parser.error(f"File {arg} does not exist!")
  else:
    return arg


parser = ArgumentParser(prog="termdoro",
                        description="pomodoro in your terminal",
                        formatter_class=RawTextHelpFormatter)

time = parser.add_argument_group("time")
time.add_argument("TIME",
                  nargs="?",
                  help="starts a countdown to TIME. example values for TIME:\n\
10, '1y 10d 1h 5m 30s', '1 January 4:00 PM'")
time.add_argument("-n",
                  "--notify",
                  action="store_true",
                  help="enable notifications")
time.add_argument("-s",
                  "--sound",
                  metavar="FILE",
                  nargs="?",
                  default=SUPPRESS,
                  type=lambda x: is_valid_file(parser, x),
                  help="enable sound with optional FILE")

options = parser.add_mutually_exclusive_group()
options.add_argument("-c",
                     "--config",
                     help="change pomodoro configuration",
                     action="store_true")
options.add_argument("-H",
                     "--history",
                     help="show pomodoro history",
                     action="store_true")
options.add_argument("-v",
                     "--version",
                     help="echo pomodoro version",
                     action="store_true")


def main() -> None:
  args = parser.parse_args()
  if args.config:
    change_config()
  elif args.history:
    print_history()
  elif args.version:
    print(VERSION)
  else:
    play_sound = True if hasattr(args, "sound") else False
    sound_to_play = args.sound if play_sound is True else None
    Session(time=args.TIME,
            notify=args.notify,
            play_sound=play_sound,
            sound_to_play=sound_to_play).draw()


if __name__ == "__main__":
  main()
