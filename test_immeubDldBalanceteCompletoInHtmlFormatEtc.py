#!/usr/bin/env python3
"""
test_immeubDldBalanceteCompletoInHtmlFormatEtc.py

  Unit-test for immeubDldBalanceteCompletoInHtmlFormatEtc.py

  # ==============
  # Below there are two TestCases
  # 1) YearMonthRangeTestCase(unittest.TestCase)
  # 2) BalanceteDownloaderTestCase(unittest.TestCase)
  # ==============
"""
import immeubDldBalanceteCompletoInHtmlFormatEtc as imm
import unittest
from dateutil.relativedelta import relativedelta


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
    self.ymrange = imm.YearMonthRange(year_from=year_from, month_from=month_from, year_to=year_to, month_to=month_to)
    self.firstdate = datetime.date(year=year_from, month=month_from, day=1)
    self.lastdate = datetime.date(year=year_to, month=month_to, day=1)

  @classmethod
  def get_ymrange2_n_its_firstdate(cls):
    year_from = 2021
    month_from = 3
    year_to = None
    month_to = None
    ymrange2 = imm.YearMonthRange(year_from=year_from, month_from=month_from, year_to=year_to, month_to=month_to)
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
    yearmonthrange = imm.YearMonthRange(2020, 11, 2021, 10)
    balancete_dldr = imm.BalanceteDownloader(yearmonthrange, None)  # immeub_code = None (ie immeub_code_default)
    immeub_code = imm.immeub_code_default
    self.assertEqual(immeub_code, balancete_dldr.immeub_code)
    dld_commands = []
    current_date = yearmonthrange.firstdate
    for i in range(yearmonthrange.size):
      month_2dign = str(current_date.month).zfill(2)
      urlparams = {'immeub_code': immeub_code, 'month_2dign': month_2dign, 'year': current_date.year}
      url = imm.baseurl.format(**urlparams)
      filename = imm.basefilename.format(**urlparams)
      dld_comm = imm.dld_comm_base.format(url, filename)
      dld_commands.append(dld_comm)
      current_date += relativedelta(months=1)
    balancete_dld_comm_list = balancete_dldr.get_dld_command_list()
    self.assertEqual(len(dld_commands), len(balancete_dld_comm_list))
    for i in range(yearmonthrange.size):
      self.assertEqual(dld_commands[i], balancete_dld_comm_list[i])
