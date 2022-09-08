#!/usr/bin/env python3
'''
dldCDutraCondFFMonthlySyntheticBalances.py

This script download the html-files equivalent to the 
  monthly balancetes for condominium CDutra.
It is expected that the last 12 months of balancetes
  will be available.

Usage:
$<this_script>
    [-m1=<month1>] [-m2=<month2>]
    [-y1=<year1>] [-y2=<year2>] [-dontdld]

Obs:
 1) all parameters are optional;
 2) if none is given, default will represent
    12 months from last month down to completing 12 months backwards.

where:
  <year1> :: is starting year
  <year2> :: is ending year
  <month1> :: is month of starting year
  <month2> :: is month of ending year
  -dontdld :: only prints to the screen, do not download any file

Example:
========
$pyDldCDutraCondFFSyntheticBalance.py -m1=9 -m2=8 -y1=2021 -y2=2022

More info:

1) The service/server makes available a 12-month past period.
   Earlier than that downloaded files gotten are content-empty.

2) This script cuts off when attempting to download months earlier
   than a year ago.
'''
import datetime
from dateutil.relativedelta import relativedelta
import os
import sys
urlBase = 'https://fernandoefernandes.com.br/ffnet_sys/sefudoff.php?cod=0154&period=%(month)02d/%(year)d'
fnBase = '%(year)d-%(month)02d Balancete Sintetico Cond CDutra.html'


def get_last_available_dld_date():
  today = datetime.date.today()
  last_available_dld_date = today - relativedelta(months=13)
  return last_available_dld_date


class CDutraBalanceteDownloader:

  def __init__(self, year_month_tuplelist, dodld=True):
    self.year_month_tuplelist = year_month_tuplelist
    self.dodld = dodld
    self.last_available_dld_date = get_last_available_dld_date()
    self.print_year_month_tuplelist()

  def print_year_month_tuplelist(self):
    for i, tupl in enumerate(self.year_month_tuplelist):
      year, month = tupl
      cdate = datetime.date(year, month, 1)
      if cdate < self.last_available_dld_date:
        print(cdate,'is not available as date which is', self.last_available_dld_date)
        continue
      url = urlBase %{'month':month, 'year':year}
      filename = fnBase %{'month':month, 'year':year}
      seq = i + 1
      comm = 'wget "%s" -O "%s"' %(url, filename)
      print(seq, '=>', comm)

  def do_dld(self):
    seq = 0
    if not self.dodld:
      print('Not to be downloaded')
      return
    print(' ======== Downloading if missing ========')
    for i, tupl in enumerate(self.year_month_tuplelist):
      year, month = tupl
      if cdate < self.date_out_of_range:
        print(cdate,'is not available as date')
        continue
      url = urlBase %{'month':month, 'year':year}
      filename = fnBase %{'month':month, 'year':year}
      seq = i + 1
      if os.path.isfile(filename):
        print(seq, 'Filename', filename, 'is already in folder.')
        continue
      comm = 'wget "%s" -O "%s"' %(url, filename)
      print(seq, '=>', comm)
      os.system(comm)


def generate_year_month_tuples(m1, m2, y1, y2):
  '''
  Example:
    m1 = 11, m2 = 2, y1 = 2021, y2 = 2022
    result = [(2022, 2), (2022, 1), (2021, 12), (2022, 11)]
  '''
  if y1 == y2 and m1 > m2 or m1 not in range(1, 13) or m2 not in range(1, 13):
    daterangepoints = [m1, m2, y1, y2]
    error_msg = 'Inconsistent date range points %s' %str(daterangepoints)
    raise ValueError(error_msg)
  year_month_tuplelist = []
  month = m2
  year = y2
  while y1 <= year:
    ymtupl = (year, month)
    year_month_tuplelist.append(ymtupl)
    month -= 1
    if month < 1:
      year -= 1
      month = 12
    if year == y1:
      if m1 > month:
        break
    elif year < y1:
      break
  return year_month_tuplelist


def get_args():
  m1 = None
  y1 = None
  m2 = None
  y2 = None
  dodld = True
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-m1='):
      m1 = arg[len('-m1='):]
    elif arg.startswith('-m2='):
      m2 = arg[len('-m2='):]
    elif arg.startswith('-y1='):
      y1 = arg[len('-y1='):]
    elif arg.startswith('-y2='):
      y2 = arg[len('-y2='):]
    elif arg.startswith('-dontdld'):
      dodld = False
  today = datetime.date.today()
  if y2 is None:
    y2 = today.year
  if y1 is None:
    y1 = today.year - 1
  if m2 is None:
    m2 = today.month - 1
  if m1 is None:
    m1 = today.month
  m1, m2, y1, y2 = int(m1), int(m2), int(y1), int(y2)
  print('start => %02d/%d' %(m1, y1), ':: end => %02d/%d' %(m2, y2),':: dontdld =', not dodld)
  return m1, m2, y1, y2, dodld


def process():
  m1, m2, y1, y2, dodld = get_args()
  year_month_tuplelist = generate_year_month_tuples(m1, m2, y1, y2)
  downloader = CDutraBalanceteDownloader(year_month_tuplelist, dodld)
  downloader.do_dld()


if __name__ == '__main__':
  process()
