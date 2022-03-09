# Termdoro
Termdoro is pomodoro in your terminal.

## Default Configuration

- Work: 25 minutes
- Break: 5 minutes
- Long break: 15 minutes
- Long break after 4 sessions
- Total of 6 sessions

# Installation

```
pip install termdoro
```

# Usage
 ```
Usage: termdoro [OPTIONS] [TIME]
  If OPTIONS and TIME is not given, termdoro will operate in
  pomodoro mode.

  Or you can use termdoro in stopwatch and countdown mode:

  Start a countdown to or from TIME. Example values for TIME:
  10, '1h 5m 30s', '12:00', '2020-01-01', '2020-01-01 14:00 UTC'.

  If TIME is not given, termdoro will operate in stopwatch mode
  and count forward.

  Hotkeys:
      L       Lap (stopwatch mode only)
      R       Reset
      SPACE   Pause (will delay absolute TIME)
      +       Plus (will add 10 seconds)
      -       Minus (will subtract 10 seconds)
      Q       Quit

Options:
  -a, --alt-format              Use colon-separated time format
  -b, --blink                   Flash terminal at end of countdown
  -B, --no-bell                 Don't ring terminal bell at end of countdown
  -c, --critical N              Draw final N seconds in red and announce them
                                individually with --voice or --exec-cmd
                                (defaults to 3)
  --config                      Configure pomodoro session settings
  -f, --font FONT               Choose from
                                http://www.figlet.org/examples.html
  --pomodoro                    Start pomodoro (default behavior)
  -p, --voice-prefix TEXT       Add TEXT to the beginning of --voice and
                                --exec annunciations (except per-second ones)
  -q, --quit-after N            Quit N seconds after countdown (use with -b or
                                -t) or terminate stopwatch after N seconds
  -s, --no-seconds              Don't show seconds (except for last minute of
                                countdown and first minute of stopwatch)
  --stopwatch                   Start a stopwatch
  -t, --text TEXT               Text to display at end of countdown
  -T, --title TEXT              Text to display on top of countdown/stopwatch
  -W, --no-window-title         Don't update terminal title with
                                remaining/elapsed time
  -v, --voice VOICE             Spoken countdown (at fixed intervals with per-
                                second annunciations starting at --critical;
                                requires `espeak` on Linux or `say` on macOS;
                                choose VOICE from `say -v '?'` or `espeak
                                --voices`)
  -o, --outfile PATH            File to write current remaining/elapsed time
                                to
  --exec-cmd CMD                Runs CMD every second. '{0}' and '{1}' in CMD
                                will be replaced with the remaining/elapsed
                                number of seconds and a more sparse
                                annunciation as in --voice, respectively. For
                                example, to get a callout at five seconds
                                only, use: --exec-cmd "if [ '{0}' == '5' ];
                                then say -v Alex {1}; fi"
  --no-figlet                   Don't use ASCII art for display
  --no-figlet-y-offset INTEGER  Vertical offset within the terminal (only for
                                --no-figlet)
  --no-text-magic               Don't try to replace non-ASCII characters (use
                                with -t)
  --version                     Show version and exit
  -z, --time                    Show current time instead of
                                countdown/stopwatch
  -Z, --time-format TEXT        Format for --time (defaults to "%H:%M:%S",
                                ignores --no-seconds)
  --help                        Show this message and exit.
```

# Credits
Termdoro uses [trehn/termdown](https://github.com/trehn/termdown) for the
terminal countdown timer and stopwatch.
