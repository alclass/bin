#!/usr/bin/env python3
'''
This script (first version 2021-11) issues wget-dowload commands for "immeuble balancetes" within a given month range.

Examples:
   $immeubDldBalanceteCompletoHtmlFormatEtc.py -yi=2021 -mi=3 -yf=2021 -mf=7

Explanation:
   The above command will mount and issue the url's for all monthly balancetes between 2021-03 and 2021-07 both included.
   This example encompasses 5 months (march to july 2021).
   (In parallel, please notice that, for the CDutra case, a maximum of 12 prior months may be available. The script does not limit that so avoid entering more than 12 months into the past.)

Parameters:
  *  all parameters are optional, if none given,
     the default will be today's year and today's month
     which means the current month's balancete is intended to be downloaded.
  -yi :: starting year
  -mi :: starting month of starting year
  -yi :: ending year
  -mi :: ending month of ending year
'''
import datetime
from dateutil.relativedelta import relativedelta
import math
import os
import sys


baseurl = "http://fernandoefernandes.com.br/ffnet_sys/sefudoff.php?cod={immeub_code}&period={month_2dign}/{year}"
basefilename = "{year}-{month_2dign} balancete completo {immeub_code} CDutra.html"
immeub_code_default = '0154'  # hardcoded by now


def months_inbetween_both_included(d1, d2):
  diff = (d1.year - d2.year) * 12 + d1.month - d2.month
  diff = abs(diff) + 1  # the +1 is because year-month takes effect in the last date
  return  diff


class YearMonthRange:

  def __init__(self, year_from, month_from, year_to=None, month_to=None):
    self.year_from, self.month_from, self.year_to, self.month_to = year_from, month_from, year_to, month_to
    self.validate_n_default_yearmonths()
    self.current_yearmonth = None
    self._zfill_decimalplaces = None

  def validate_n_default_yearmonths(self):
    today = datetime.date.today()
    if self.year_from is None:
      self.year_from = today.year
    if self.year_to is None:
      self.year_to = self.year_from
    if self.month_from is None:
      self.month_from = today.month
    if self.month_to is None:
      self.month_to = self.month_from
    if self.firstdate > self.lastdate:
      error_msg = 'Error in given dates => firstdate (%s) > lastdate (%s)' % (firstdate, lastdate)
      raise ValueError(error_msg)

  @property
  def firstdate(self):
    firstdate = datetime.date(year=self.year_from, month=self.month_from, day=1)
    return firstdate

  @property
  def lastdate(self):
    lastdate = datetime.date(year=self.year_to, month=self.month_to, day=1)
    return lastdate

  @property
  def months_inbetween(self):
    return months_inbetween_both_included(self.lastdate, self.firstdate)

  @property
  def size(self):
    return self.months_inbetween

  @property
  def zfill_decimalplaces(self):
    if self._zfill_decimalplaces is None:
      self._zfill_decimalplaces = math.floor(math.log(self.size, 10)) + 1
    return self._zfill_decimalplaces

  def next(self):
    """
      year_from, month_from, year_to, month_to
    :return:
    """
    if self.current_yearmonth is None:
      self.current_yearmonth = self.firstdate
    else:
      self.current_yearmonth += relativedelta(months=1)
    yield self.current_yearmonth

  def get_yearmonths_as_datelist(self):
    current_date = self.firstdate
    yearmonths = []
    while current_date <= self.lastdate:
      yearmonths.append(current_date)
      current_date += relativedelta(months=1)
    return yearmonths

  def __str__(self):
    dictdate = {'firstdate': self.firstdate, 'lastdate': self.lastdate, 'months_inbetween': self.months_inbetween}
    outstr = '''YearMonthRange:
    firstdate = {firstdate}
    lastdate  = {lastdate}
    months_inbetween = {months_inbetween}
    '''.format(**dictdate)
    return outstr


class BalanceteDownloader:

  def __init__(self, yearmonthrange, immeub_code=None):

    if immeub_code is None:
      self.immeub_code = immeub_code_default
    self.yearmonthrange = yearmonthrange

  def mount_n_ret_command_line_per_month(self, pdate):
    year, month = pdate.year, pdate.month
    month_2dign = str(month).zfill(2)
    interpol_params = {'month_2dign': month_2dign, 'year': year, 'immeub_code': self.immeub_code}
    url = baseurl.format(**interpol_params)
    filename = basefilename.format(**interpol_params)
    comm = 'wget "{0}" -O "{1}"'.format(url, filename)
    return comm

  def show_dlds_year_month(self):
    print('======== List for Download Confirmation ========')
    print('The balancete(s) for the months below will be issued for download on current folder:')
    for i, currentdate in enumerate(self.yearmonthrange.get_yearmonths_as_datelist()):
      j_label = str(i+1).zfill(self.yearmonthrange.zfill_decimalplaces)
      print (j_label, 'Balancete immeub', self.immeub_code, 'for month', str(currentdate.year) + '-' + str(currentdate.month).zfill(2))
    print('======== Total: ', self.yearmonthrange.size)

  def confirm_year_month_tuplelist_downloads(self):
    verb = 'Is'; noun = 'month'
    if self.yearmonthrange.size > 1:
      verb = 'Are'; noun = 'months'
    ans = input(verb + ' the download ' + noun + ' above okay? *Y/n ')
    if ans in ['Y', 'y', '']:
      return True
    return False

  def dld_balancetes_thru_yearmonthrange(self):
    print('========')
    print('The balancete(s) for the months below will be issued for download on current folder:')
    for currentdate in self.yearmonthrange.get_yearmonths_as_datelist():
      comm = self.mount_n_ret_command_line_per_month(currentdate)
      os.system(comm)

  def process_dld_balancetes_thru_yearmonthrange(self):
    self.show_dlds_year_month()
    bool_confirm = self.confirm_year_month_tuplelist_downloads()
    print('bool_confirm', bool_confirm)
    if bool_confirm:
      self.dld_balancetes_thru_yearmonthrange()


def treat_year_month_params(months, years):
  year_month_tuple_list = []
  months = treat_month_param(months)
  years = treat_month_year_params(years)
  for year in years:
    for month in months:
      year_month = (year, month)
      year_month_tuple_list.append(year_month)
  return year_month_tuple_list


def get_args():
  year_from = None
  year_to = None
  month_from = None
  month_to = None
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    if arg.startswith('-yi'):
      year_from = int(arg[len('-yi='): ])
    elif arg.startswith('-yf='):
      year_to = int(arg[len('-yf='):])
    elif arg.startswith('-mi='):
      month_from = int(arg[len('-mi='): ])
    elif arg.startswith('-mf='):
      month_to = int(arg[len('-mf='):])
  return YearMonthRange(year_from, month_from, year_to, month_to)


def test1():
  year_from, month_from, year_to, month_to = 2020, 10, 2021, 5
  yearmonthrange = YearMonthRange(year_from, month_from, year_to, month_to)
  print(yearmonthrange)
  for i, o in enumerate(yearmonthrange.get_yearmonths_as_datelist()):
    print(i, o)
  year_from, month_from, year_to, month_to = 2018, 1, 2019, 4
  yearmonthrange = YearMonthRange(year_from, month_from, year_to, month_to)
  print(yearmonthrange)
  for i, o in enumerate(yearmonthrange.get_yearmonths_as_datelist()):
    print(i, o)


def process():
  yearmonthrange = get_args()
  print(yearmonthrange)
  balancete_dldr = BalanceteDownloader(yearmonthrange)
  balancete_dldr.process_dld_balancetes_thru_yearmonthrange()


if __name__ == '__main__':
  # test1()
  process()
  # process()
