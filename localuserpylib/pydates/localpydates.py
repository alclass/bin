#!/usr/bin/env python3
"""
localuserpylib/pydates/localpydates.py
  A local user's Python library dedicated to date functions
"""
import datetime
from typing import Generator
from xmlrpc.client import boolean


def gen_last_n_monday_dates_from_date(pdate: datetime.date, n=50) -> Generator[datetime.date, None, None]:
  """
  localuserpylib/dates/localpydates/gen_last_n_monday_dates_from_today

  This note below is not about the function itself, but to remid about how to use the Generator type.

  The syntax is Generator[YieldType, SendType, ReturnType].

    YieldType: The type of the values yielded by the generator.
    SendType: The type of values that can be sent to the generator using the .send() method (usually None if not used).
    ReturnType: The type of the value returned by the generator when it finishes (usually None
      if it doesn't return a value explicitly).

  The 3 values in the Generator type above mean:
    1 datetime.date: the YieldType
    2 None: because it doesn't receive values through .send()
    3 None: on the last return value (a simple return returns None)

  """
  # take pdate as monday until proven contrary
  monday_date = pdate
  weekday = pdate.isoweekday()
  if weekday > 1:
    minus_days = weekday - 1
    monday_date = pdate - datetime.timedelta(days=minus_days)
  # yields the last n monday dates
  for i in range(n):
    yield monday_date
    monday_date = monday_date - datetime.timedelta(days=7)
  return


def gen_last_n_monday_dates_from_today(n=50) -> Generator[datetime.date, None, None]:
  today = datetime.date.today()
  return gen_last_n_monday_dates_from_date(today, n)


def gen_all_mondays_inbetweenfrom_asc(oldest_date: datetime.date) -> Generator[datetime.date, None, None]:
  today = datetime.date.today()
  # take oldest_date as monday until proven contrary
  monday_date = oldest_date
  weekday = monday_date.isoweekday()
  # weekday = 1 is monday, if it's greater than 1, go to the next monday in calendar
  if weekday > 1:
    plus_days = 8 - weekday
    # go to the future finding monday
    monday_date = oldest_date + datetime.timedelta(days=plus_days)
  # yields each monday upwardly until today or its previous monday
  while monday_date <= today:
    yield monday_date
    # go to the future
    monday_date = monday_date + datetime.timedelta(days=7)
  return


def gen_all_mondays_inbetweenfrom_desc(oldest_date: datetime.date) -> Generator[datetime.date, None, None]:
  today = datetime.date.today()
  # take today as monday until proven contrary
  monday_date = today
  weekday = today.isoweekday()
  # weekday = 1 is monday, if it's greater than 1, go to the previous monday in calendar
  if weekday > 1:
    minus_days = weekday - 1
    # go to the past finding monday
    monday_date = today - datetime.timedelta(days=minus_days)
  # yields each monday downwardly until oldest_date or its next monday
  while monday_date >= oldest_date:
    yield monday_date
    # go to the past
    monday_date = monday_date - datetime.timedelta(days=7)
  return


def gen_all_mondays_inbetweenfrom(oldest_date: datetime.date, ascending_order=True) \
     -> Generator[datetime.date, None, None]:
  if ascending_order:
    return gen_all_mondays_inbetweenfrom_asc(oldest_date)
  else:
    return gen_all_mondays_inbetweenfrom_desc(oldest_date)


def transform_datetime_into_date(pdatetime: datetime.datetime) -> datetime.date | None:
  if pdatetime is None:
    return None
  y, m, d = pdatetime.year, pdatetime.month, pdatetime.day
  pdate = datetime.date(year=y, month=m, day=d)
  return pdate


def get_nearest_monday_from(pdatetime: datetime.datetime) -> datetime.date | None:
  """
  Returns the nearest monday date of the input date according to the following convention:
    1 if date is already a monday, return it
    2 if date is either a Tuesday, Wednesday or Thursday, return its previous monday (past of input date)
    3 if date is either a Friday, Saturday or Sunday, return its next monday (future of input date)

  :param pdatetime:
  :return:
  """
  pdate = transform_datetime_into_date(pdatetime)
  if pdate is None:
    return None
  weekday = pdate.isoweekday()
  # weekday = 1 is monday, if it's greater than 1, go to the previous monday in calendar
  if weekday == 1:
    return pdate
  if weekday in [2, 3, 4]:  # ie Tuesday, Wednesday or Thursday
    minus_days = weekday - 1
    # nearest monday is in the past
    monday_date = pdate - datetime.timedelta(days=minus_days)
    return monday_date
  # date is in [5, 6, 7] ie Friday, Saturday, Sunday
  plus_days = 8 - weekday
  # nearest monday is in the future
  monday_date = pdate + datetime.timedelta(days=plus_days)
  return monday_date


def get_weekdayname_from_isoweekday(isoweekday: int) -> str | None:
  """
  Returns the weekday's English name from its isoweekday number
  :param isoweekday:
  :return:
  """
  if isoweekday is None:
    return None
  weekdaynames = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
  ]
  if isoweekday in range(1, 8):
    return weekdaynames[isoweekday - 1]
  return None


def transform_std_strdate_into_pydate(strdate: str | None) -> datetime.date | None:
  if strdate is None:
    return None
  try:
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    pdate = datetime.date(year=year, month=month, day=day)
    return pdate
  except (IndexError, ValueError):
    pass
  return None


def is_strdate_a_std_str_date(strdate: str | None) -> boolean:
  """
  if isinstance(pdate, datetime.date):
    return True
  """
  pdate = transform_std_strdate_into_pydate(strdate)
  if pdate is None:
    return False
  return True


def is_strdate_before_today(strdate: str | None) -> boolean:
  pdate = transform_std_strdate_into_pydate(strdate)
  if not isinstance(pdate, datetime.date):
    return False
  today = datetime.date.today()
  if pdate < today:
    return True
  return False


def adhoc_test2():
  pdate = today = datetime.date.today()
  weekday = pdate.isoweekday()
  scrmsg = f"today is {today} and weekday is {weekday}"
  print(scrmsg)
  for difday in range(0, 15):
    pdate = pdate - datetime.timedelta(days=1)
    weekday = pdate.isoweekday()
    weekdayname = get_weekdayname_from_isoweekday(weekday)
    nearest_monday = get_nearest_monday_from(pdate)
    nearest_monday_weekday = nearest_monday.isoweekday()
    nearest_monday_weekdayname = get_weekdayname_from_isoweekday(nearest_monday_weekday)
    scrmsg = (
      f"{difday} from {pdate} (weekday={weekdayname}) nearest monday is {nearest_monday} "
      f"(weekday={nearest_monday_weekdayname})"
    )
    print(scrmsg)


def adhoc_test1():
  y, m, d = 2024, 11, 12
  pdate = datetime.date(year=y, month=m, day=d)
  for i, idate in enumerate(gen_all_mondays_inbetweenfrom(pdate, ascending_order=True)):
    seq = i + 1
    print(seq, idate)


def process():
  adhoc_test1()
  adhoc_test2()


if __name__ == '__main__':
  """
  adhoc_test()
  """
  process()
