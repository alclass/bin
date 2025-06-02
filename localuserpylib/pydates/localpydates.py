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


def adhoc_test1():
  y, m, d = 2024, 11, 12
  pdate = datetime.date(year=y, month=m, day=d)
  for i, idate in enumerate(gen_all_mondays_inbetweenfrom(pdate, ascending_order=True)):
    seq = i + 1
    print(seq, idate)


def process():
  adhoc_test1()


if __name__ == '__main__':
  """
  adhoc_test()
  """
  process()
