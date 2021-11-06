#!/usr/bin/env python3
"""
This script (first version 2021-11) issues wget-dowload commands for "immeuble balancetes" within a given month range.

Examples:
   $immeubDldBalanceteCompletoHtmlFormatEtc.py -yi=2021 -mi=3 -yf=2021 -mf=7

Explanation:
   The above command will mount and download-issue the url's for all monthly balancetes
      between 2021-03 and 2021-07 both included.
   This example encompasses 5 months (march to july 2021).
   (In parallel, please notice that, for the CDutra case, a maximum of 12 prior months
     may be available. The script does not limit that so avoid entering more than 12 months
    into the past.)

Parameters:
  *  all parameters are optional, if none given,
     the default will be today's year and today's month
     which means the current month's balancete is intended to be downloaded.
  -yi :: starting year
  -mi :: starting month of starting year
  -yi :: ending year
  -mi :: ending month of ending year
"""
import datetime
from dateutil.relativedelta import relativedelta
import math
import os
import sys
import unittest


baseurl = "http://fernandoefernandes.com.br/ffnet_sys/sefudoff.php?cod={immeub_code}&period={month_2dign}/{year}"
basefilename = "{year}-{month_2dign} balancete completo {immeub_code} CDutra.html"
dld_comm_base = 'wget "{0}" -O "{1}"'
immeub_code_default = '0154'  # hardcoded by now


def months_inbetween_both_included(d1, d2):
  diff = (d1.year - d2.year) * 12 + d1.month - d2.month
  diff = abs(diff) + 1  # the +1 is because year-month takes effect in the last date
  return diff


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
  def n_months_inbetween(self):
    return months_inbetween_both_included(self.lastdate, self.firstdate)

  @property
  def size(self):
    return self.n_months_inbetween

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

  def __eq__(self, other_ymrange):
    if self.firstdate == other_ymrange.firstdate and self.lastdate == other_ymrange.lastdate:
      return True
    return False

  def __str__(self):
    dictdate = {'firstdate': self.firstdate, 'lastdate': self.lastdate, 'months_inbetween': self.n_months_inbetween}
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

  def mount_n_ret_dld_command_line_per_month(self, pdate):
    month_2dign = str(pdate.month).zfill(2)
    interpol_params = {'immeub_code': self.immeub_code, 'month_2dign': month_2dign, 'year': pdate.year}
    url = baseurl.format(**interpol_params)
    filename = basefilename.format(**interpol_params)
    dld_comm = dld_comm_base.format(url, filename)
    return dld_comm

  def get_dld_command_list(self):
    dld_command_list = []
    for currentdate in self.yearmonthrange.get_yearmonths_as_datelist():
      dld_comm = self.mount_n_ret_dld_command_line_per_month(currentdate)
      dld_command_list.append(dld_comm)
    return dld_command_list

  def show_dlds_year_month(self):
    print('======== List for Download Confirmation ========')
    print('The balancete(s) for the months below will be issued for download on current folder:')
    for i, currentdate in enumerate(self.yearmonthrange.get_yearmonths_as_datelist()):
      j_label = str(i+1).zfill(self.yearmonthrange.zfill_decimalplaces)
      print(j_label, 'Balancete immeub', self.immeub_code, 'for month',
            str(currentdate.year) + '-' + str(currentdate.month).zfill(2))
    print('======== Total: ', self.yearmonthrange.size)

  def confirm_year_month_tuplelist_downloads(self):
    verb = 'Is'
    noun = 'month'
    if self.yearmonthrange.size > 1:
      verb = 'Are'
      noun = 'months'
    ans = input(verb + ' the download ' + noun + ' above okay? *Y/n ')
    if ans in ['Y', 'y', '']:
      return True
    return False

  def dld_balancetes_thru_yearmonthrange(self):
    print('========')
    print('The balancete(s) for the months below will be issued for download on current folder:')
    for currentdate in self.yearmonthrange.get_yearmonths_as_datelist():
      comm = self.mount_n_ret_dld_command_line_per_month(currentdate)
      os.system(comm)

  def process_dld_balancetes_thru_yearmonthrange(self):
    self.show_dlds_year_month()
    bool_confirm = self.confirm_year_month_tuplelist_downloads()
    print('bool_confirm', bool_confirm)
    if bool_confirm:
      self.dld_balancetes_thru_yearmonthrange()


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
      year_from = int(arg[len('-yi='):])
    elif arg.startswith('-yf='):
      year_to = int(arg[len('-yf='):])
    elif arg.startswith('-mi='):
      month_from = int(arg[len('-mi='):])
    elif arg.startswith('-mf='):
      month_to = int(arg[len('-mf='):])
  return YearMonthRange(year_from, month_from, year_to, month_to)


def process():
  yearmonthrange = get_args()
  print(yearmonthrange)
  balancete_dldr = BalanceteDownloader(yearmonthrange)
  balancete_dldr.process_dld_balancetes_thru_yearmonthrange()


if __name__ == '__main__':
  process()


# ==============
# Below there are two TestCases
# 1) YearMonthRangeTestCase(unittest.TestCase)
# 2) BalanceteDownloaderTestCase(unittest.TestCase)
# ==============

class YearMonthRangeTestCase(unittest.TestCase):
  """
  This TestCase is more encompassing than the second one below (see also its docstring).
  This difference was due to the fact that the second class has user input and
    network connection (the download proper).

  Anyways, the YearMonthRange class is tested for its properties (attributes)
    and its derivations (example: the generated list of dates within the range).
  """
  def setUp(self):
    year_from = 2021
    month_from = 3
    year_to = 2021
    month_to = 7
    self.ymrange = YearMonthRange(year_from=year_from, month_from=month_from, year_to=year_to, month_to=month_to)
    self.firstdate = datetime.date(year=year_from, month=month_from, day=1)
    self.lastdate = datetime.date(year=year_to, month=month_to, day=1)

  @classmethod
  def get_ymrange2_n_its_firstdate(cls):
    year_from = 2021
    month_from = 3
    year_to = None
    month_to = None
    ymrange2 = YearMonthRange(year_from=year_from, month_from=month_from, year_to=year_to, month_to=month_to)
    firstdate = datetime.date(year_from, month_from, 1)
    return ymrange2, firstdate

  def test1_1_firstdate(self):
    self.assertEqual(self.firstdate, self.ymrange.firstdate)

  def test1_2_lastdate(self):
    self.assertEqual(self.lastdate, self.ymrange.lastdate)

  def test1_3_n_months_inbetween(self):
    n_months_inbetween = 7 - 3 + 1  # ie = 5
    self.assertEqual(n_months_inbetween, self.ymrange.n_months_inbetween)
    self.assertEqual(n_months_inbetween, self.ymrange.size)

  def test1_4_zfill_decimalplaces(self):
    zfill_decimalplaces = 1  # ie int's for 5 months just needs one digit (1,2,3,4,5 instead of 01,02,03,04,05)
    self.assertEqual(zfill_decimalplaces, self.ymrange.zfill_decimalplaces)

  def test1_5_yms_as_datelist(self):
    date2 = self.firstdate + relativedelta(months=1)
    date3 = date2 + relativedelta(months=1)
    date4 = date3 + relativedelta(months=1)
    yms_as_datelist = [self.firstdate, date2, date3, date4, self.lastdate]
    self.assertEqual(yms_as_datelist, self.ymrange.get_yearmonths_as_datelist())

  def test2_1_firstdate(self):
    ymrange2, firstdate = self.get_ymrange2_n_its_firstdate()
    self.assertEqual(firstdate, ymrange2.firstdate)

  def test2_2_lastdate(self):
    ymrange2, firstdate = self.get_ymrange2_n_its_firstdate()
    lastdate = firstdate
    self.assertEqual(lastdate, ymrange2.lastdate)

  def test2_3_n_months_inbetween(self):
    ymrange2, _ = self.get_ymrange2_n_its_firstdate()
    n_months_inbetween = 1  # lastdate is None, this means range has only one month
    self.assertEqual(n_months_inbetween, ymrange2.n_months_inbetween)
    self.assertEqual(n_months_inbetween, ymrange2.size)

  def test2_4_zfill_decimalplaces(self):
    ymrange2, _ = self.get_ymrange2_n_its_firstdate()
    zfill_decimalplaces = 1  # ie int's for 5 months just needs one digit (1,2,3,4,5 instead of 01,02,03,04,05)
    self.assertEqual(zfill_decimalplaces, ymrange2.zfill_decimalplaces)

  def test2_5_yms_as_datelist(self):
    ymrange2, firstdate = self.get_ymrange2_n_its_firstdate()
    yms_as_datelist = [self.firstdate]
    self.assertEqual(yms_as_datelist, ymrange2.get_yearmonths_as_datelist())

  def test3_equality(self):
    ymrange1 = YearMonthRange(2020, 11, 2021, 10)
    ymrange2 = YearMonthRange(2020, 11, 2021, 10)
    self.assertEqual(ymrange1, ymrange2)


class BalanceteDownloaderTestCase(unittest.TestCase):
  """
  BalanceteDownloader has only one test, ie the comparison of the downlaad commands.
  This also tests the url's and filenames which are composed of triple year, month and immeub_code
  In terms of data nothing else needs to be tested. However, the user input and
    the actual download and file downloaded could be tested.
    1) The user input is a kind of behavior test and
    2) the download test is a kind of network-dependant test.
  So the idea here was to test the more common unit-test routines, ie data transformed along program execution.
  """

  def test1_download_commands(self):
    yearmonthrange = YearMonthRange(2020, 11, 2021, 10)
    balancete_dldr = BalanceteDownloader(yearmonthrange, None)  # immeub_code = None (ie immeub_code_default)
    immeub_code = immeub_code_default
    self.assertEqual(immeub_code, balancete_dldr.immeub_code)
    dld_commands = []
    current_date = yearmonthrange.firstdate
    for i in range(yearmonthrange.size):
      month_2dign = str(current_date.month).zfill(2)
      urlparams = {'immeub_code': immeub_code, 'month_2dign': month_2dign, 'year': current_date.year}
      url = baseurl.format(**urlparams)
      filename = basefilename.format(**urlparams)
      dld_comm = dld_comm_base.format(url, filename)
      dld_commands.append(dld_comm)
      current_date += relativedelta(months=1)
    balancete_dld_comm_list = balancete_dldr.get_dld_command_list()
    self.assertEqual(len(dld_commands), len(balancete_dld_comm_list))
    for i in range(yearmonthrange.size):
      self.assertEqual(dld_commands[i], balancete_dld_comm_list[i])
