# Termdoro

Termdoro is pomodoro in your terminal.

## Default Configuration

- Work: 25 minutes
- Break: 5 minutes
- Long break: 15 minutes
- Long break after 4 sessions
- Total of 6 sessions

## Installation

```console
pip3 install termdoro
```

## Usage

```console
usage: termdoro [-h] [-n] [-s [FILE]] [-c | -H | -v] [TIME]

pomodoro in your terminal

options:
  -h, --help            show this help message and exit
  -c, --config          change pomodoro configuration
  -H, --history         show pomodoro history
  -v, --version         echo pomodoro version

time:
  TIME                  starts a countdown to TIME. example values for TIME:
                        10, '1y 10d 1h 5m 30s', '1 January 4:00 PM'
  -n, --notify          enable notifications
  -s [FILE], --sound [FILE]
                        enable sound with optional FILE
```

## Notes

If sound does not work install `PyObjC`.

```console
pip3 install PyObjC 
```
