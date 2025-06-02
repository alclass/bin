#!/usr/bin/env python3
"""
localuserpylib/pydates/localpydates.py
  A local user's Python library dedicated to date functions
"""
import datetime


def gen_last_n_monday_dates(n=50):
  """
  localuserpylib/dates/localpydates/gen_last_n_monday_dates
  """
  today = datetime.date.today()
  # take today as monday until proven contrary
  monday_date = today
  weekday = today.isoweekday()
  if weekday > 1:
    minus_days = weekday - 1
    monday_date = today - datetime.timedelta(days=minus_days)
  # yields the last n monday dates
  for i in range(n):
    yield monday_date
    monday_date = monday_date - datetime.timedelta(days=7)
  return


def gen_all_mondays_inbetweenfrom_asc(oldest_date: datetime.date):
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


def gen_all_mondays_inbetweenfrom_desc(oldest_date: datetime.date):
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


def gen_all_mondays_inbetweenfrom(oldest_date: datetime.date, ascending_order=True):
  if ascending_order:
    return gen_all_mondays_inbetweenfrom_asc(oldest_date)
  else:
    return gen_all_mondays_inbetweenfrom_desc(oldest_date)


def transform_datetime_into_date(pdatetime: datetime.datetime) -> datetime.date:
  if pdatetime is None:
    return None
  y, m, d = pdatetime.year, pdatetime.month, pdatetime.day
  pdate = datetime.date(year=y, month=m, day=d)
  return pdate


def get_nearest_monday_from(pdatetime: datetime.datetime):
  pdate = transform_datetime_into_date(pdatetime)
  if pdate is None:
    return None
  weekday = pdate.isoweekday()
  # weekday = 1 is monday, if it's greater than 1, go to the previous monday in calendar
  if weekday == 1:
    return pdate
  if weekday < 4:
    minus_days = weekday - 1
    # nearest monday is in the past
    monday_date = pdate - datetime.timedelta(days=minus_days)
    return monday_date
  plus_days = 8 - weekday
  # nearest monday is in the future
  monday_date = pdate + datetime.timedelta(days=plus_days)
  return monday_date


def get_weekdayname_from_isoweekday(isoweekday: int):
  weekdaynames = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
  ]
  if isoweekday in range(1, 8):
    return weekdaynames[isoweekday - 1]
  return None


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
    scrmsg = f"{difday} from {pdate} (weekday={weekdayname}) nearest monday is {nearest_monday} (weekday={nearest_monday_weekdayname})"
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
