import os
import sqlite3

termdoro_dir = os.path.dirname(__file__)
db_dir = os.path.join(termdoro_dir, 'termdoro.db')

class Data:
  connection = sqlite3.connect(db_dir)
  cursor = connection.cursor()

  def __init__(self):
    self.cursor.execute(
      'CREATE TABLE IF NOT EXISTS termdoro ( \
          id INTEGER PRIMARY KEY AUTOINCREMENT, \
          startyear TEXT, \
          startmonth TEXT, \
          startweek TEXT, \
          startday TEXT, \
          starthour TEXT, \
          startminute TEXT, \
          startsecond TEXT, \
          endyear TEXT, \
          endmonth TEXT, \
          endweek TEXT, \
          endday TEXT, \
          endhour TEXT, \
          endminute TEXT, \
          endsecond TEXT, \
          timeworkedinhours INTEGER, \
          timeworkedinminutes INTEGER, \
          timeworkedinseconds INTEGER \
      )'
    )
    self.connection.commit()

  def addTimeElapsed(self, seconds, start_time) -> None:
    start_year = start_time.format('YYYY')
    start_month = start_time.format('MMMM')
    start_week = start_time.isocalendar()[1]
    start_day = start_time.format('DD')
    start_hour = start_time.format('HH')
    start_minute = start_time.format('mm')
    start_second = start_time.format('ss')

    end_time = start_time.shift(seconds=seconds)

    end_year = end_time.format('YYYY')
    end_month = end_time.format('MMMM')
    end_week = end_time.isocalendar()[1]
    end_day = end_time.format('DD')
    end_hour = end_time.format('HH')
    end_minute = end_time.format('mm')
    end_second = end_time.format('ss')

    timeworkedinminutes = round(seconds / 60, 2)
    timeworkedinhours = round(timeworkedinminutes / 60, 2)

    self.cursor.execute(
      'INSERT INTO termdoro VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
      (None,
      start_year, start_month, start_week, start_day, 
      start_hour, start_minute, start_second,
      end_year, end_month, end_week, end_day,
      end_hour, end_minute, end_second,
      timeworkedinhours, timeworkedinminutes, seconds)
    )
    self.connection.commit()