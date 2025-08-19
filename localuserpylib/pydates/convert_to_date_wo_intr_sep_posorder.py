#!/usr/bin/env python3
"""
lib/datefs/convert_to_date_wo_intr_sep_posorder.py
  Has functions for converting str's or attr_obj's into datetime. date's et-al

Differently from the introspect_dates.py modules, it does not use parameters used by the latter, ie:

  a) sep (separator) => STRDATE_SEPARATORS = ['-', '/', '.'] or
  b) posorder => ORDERPOS_TOKENS_AVAILABLE = ['ymd', 'ydm', 'dmy', 'mdy']

Because of that, only the two following formats are acceptable here:
  a) either yyyy-mm-dd (mm & dd don't need to have a leftzero if less than 10) or
    e.g. 2023-1-1
  b) yyyymmdd in which case mm & dd need to have a leftzero if less than 10
    e.g. 20230101

Also:
  the convertion here accepts an object that implements the three integer attributes: year, month & day.
    e.g. an object such as collection.namedtuple('Name', fields=['year', 'month', day']
      of course, in the case above, the final consistency check will be taken
      through datetime. date's constructor.
"""
import copy
import datetime
import random
from typing import Union  # Optional, List, Dict, Any, Tuple
from dateutil.relativedelta import relativedelta
from jedi.inference.gradual.typing import AnyClass
DEFAULT_N_RANDOMDATES_TO_MAKE = 3


def convert_str_or_attrsobj_to_date_or_none(str_or_obj):
  """
    Tries to tranform/convert parameter pdate into a datetime. date value, or else returns None.

  The input is tested for 'date' in 5 subsequent conversion-tests, ie:
    1 if it's a datetime. date itself or a subclass of it (which is returned rightaway) or
    2 if it's an object that contains, as properties, the int attributes year, month & day
    3 if it's an object whose str-repr has the prefix form "yyyy-mm-dd" ie,
    at_least_1digit_year-1or2digit_month-1or2digit_day
    4 if all above failed, it tries to find a date in a string of the form "yyyymmdd" without the "-" separator
  param: pdate object | string | None
  output: datetime. date | None

  if issubclass(datetime.date, type(str_or_obj)):
    return str_or_obj
  """
  if str_or_obj is None:
    return None
  if isinstance(str_or_obj, datetime.date):
    # notice that a datetime.datetime object may also "enter" here,
    # so, also because of unit-test equality necessity, a datetime.date must be reconstructed for the output
    o = str_or_obj
    return datetime.date(year=o.year, month=o.month, day=o.day)
  try:
    # in this first try, aim is to find an object that contains the 3 integer attrs named: year, month & day
    o = str_or_obj
    year = int(o.year)
    month = int(o.month)
    day = int(o.day)
    return datetime.date(year=year, month=month, day=day)
  except (AttributeError, TypeError, ValueError):
    # AttributeError catches the lack of the attribute
    # ValueError catches in case int(n) fails
    # TypeError is necessary because an object's inner attribute may be None
    pass
  try:
    str_or_obj = str(str_or_obj)[:10]
    pp = str_or_obj.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, ValueError):
    # IndexError catches whether the indexed element (ie e[i]) does not exist
    # ValueError catches in case int(n) fails
    # * TypeError is not necessary for is-None has already been checked above
    pass
  # last try with a strdate without separators (ie yyyymmdd instead of yyyy-mm-dd)
  return make_date_or_none_wo_separators(str_or_obj)


def is_date_weekend(pdate):
  try:
    weekidx = pdate.weekday()
    # 5 is Saturday, 6 is Sunday
    if weekidx in [5, 6]:
      return True
    return False
  except TypeError:
    pass
  return False


def get_tuplelist_splitting_prefixdate_n_name_fr_lines(strlist):
  """
  Gets a tuple list from dates and names extracted from each line (in lines or strlist)

  Example:
    Suppose the lines below as input:
      (omitting quotes)
      2010-11-07 Luiz Lewis
      2013-11-07 Alex Escobar
      2030-11-07 Ann Rose
      1999-11-07 Mary Ann
    output would be: [
      (datetime.date(2010, 11, 07), 'Luiz Lewis'),
      (datetime.date(2013, 11, 07), 'Alex Escobar'),
      (datetime.date(2030, 11, 07), 'Ann Rose'),
      (datetime.date(1999, 11, 07), 'Mary Ann'),
    ]
  """
  if strlist is None or len(strlist) == 0:
    return None, None
  strlist = map(lambda s: s.strip(' \t\r\n'), strlist)
  tuplelist = [(make_date_or_none(s[:10]), s[11:]) for s in strlist if len(s) > 10]
  tuplelist = [te for te in tuplelist if te[0] is not None]
  return tuplelist


def get_first_tuple_elem_splitting_prefixdate_n_name_fr_lines(strlist, sort_asc=False, sort_desc=False):
  """
  Gets a top tuple element from dates and names extracted from each line (in lines or strlist)

  Example:
    Suppose the lines belows:
      2010-11-07 Luiz Lewis
      2013-11-07 Alex Escobar
      2030-11-07 Ann Rose
      1999-11-07 Mary Ann

  The results, return for newest and oldest and not sorted, are:
    notsorted = (datetime.date(2010, 11, 7), 'Luiz Lewis')
    newest = (datetime.date(2030, 11, 7), 'Ann Rose')
    oldest = (datetime.date(1999, 11, 7), 'Mary Ann')
  """
  tuplelist = get_tuplelist_splitting_prefixdate_n_name_fr_lines(strlist)
  if len(tuplelist) == 0:
    return None, None
  if sort_asc:
    tuplelist = sorted(tuplelist, key=lambda k: k[0])
  elif sort_desc:
    tuplelist = sorted(tuplelist, key=lambda k: k[0], reverse=True)
  top_name, pdate = tuplelist[0]
  return top_name, pdate


def find_oldest_name_n_its_prefix_date_in_strlist(strlist):
  """
  @see docstr for get_first_tuple_elem_splitting_prefixdate_n_name_fr_lines()
  """
  return get_first_tuple_elem_splitting_prefixdate_n_name_fr_lines(strlist, sort_asc=True)


def find_newest_name_n_its_prefix_date_in_strlist(strlist):
  """
  @see docstr for get_first_tuple_elem_splitting_prefixdate_n_name_fr_lines()
  """
  return get_first_tuple_elem_splitting_prefixdate_n_name_fr_lines(strlist, sort_desc=True)


def make_date_or_none_wo_separators(pdate):
  """
  Transforms/converts an 8-char string under the form yyyymmdd (without '-') into datetime. date
    Notice
      a) strdate is this case must have 8-char and all of them must be integer
      b) the datetime. date constructor itself does the validation/consistency of the date
  """
  if pdate is None:
    return None
  try:
    strdate = str(pdate)
    year = int(strdate[:4])
    month = int(strdate[4:6])
    day = int(strdate[6:8])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, ValueError):
    pass
  return None


def make_date_or_none(pdate):
  """
  Just an alias to the main function
  """
  return convert_str_or_attrsobj_to_date_or_none(pdate)


def make_date_or_today(pdate: str | datetime.date | None = None) -> datetime.date | None:
  """
    Calls the main function for converting to a date.
    If receives a None, returns 'today'.

  Reminder that:
    b) this function uses make_date_or_none() (which is itself an alias of the main function)
    a) both forms: yyyy-mm-dd & yyyymmdd are tried from here
  """
  pdate = make_date_or_none(pdate)
  if pdate is None:
    return datetime.date.today()
  return pdate


def make_date_or_today_forbid_future(pdate: str | datetime.date | None = None) -> datetime.date | None:
  pdate = make_date_or_today(pdate)
  today = datetime.date.today()
  if pdate > today:
    return today
  return pdate


def make_date_from_str_or_none(strdate):
  """
  Just an alias to the main function
  """
  return convert_str_or_attrsobj_to_date_or_none(strdate)


def get_delta_diff_between_dates(
    start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]
  ) -> relativedelta | None:
  start_date = make_date_or_none(start_date)
  if start_date is None:
    return None
  end_date = make_date_or_none(end_date)
  if end_date is None:
    return None
  if start_date > end_date:
    tmpdate = end_date
    end_date = start_date
    start_date = tmpdate
  # Calculate the difference
  delta = relativedelta(end_date, start_date)
  return delta


def calc_n_completedays_between_dates(
    start_date: Union[str, datetime.date], end_date: Union[str, datetime.date]
  ) -> int | None:
  """
  Calculates the number of days elapsed between two dates
  """
  start_date = make_date_or_none(start_date)
  end_date = make_date_or_none(end_date)
  if start_date is None or end_date is None:
    return None
  if start_date > end_date:
    tmpdate = start_date
    start_date = end_date
    end_date = tmpdate
  diff = end_date - start_date
  return diff.days


def trans_convertabledates_to_datelist(datelist: list[datetime.date | str] | None) -> list[datetime.date]:
  odates = []
  if datelist is None:
    return []
  for pdate in datelist:
    if isinstance(pdate, datetime.date):
      odates.append(pdate)
      continue
    odate = make_date_or_none(pdate)
    if isinstance(odate, datetime.date):
      odates.append(odate)
  return odates


def trans_datelist_to_strdatelist(
      datelist: list[datetime.date | str | AnyClass] | None,
      raises_if_any_not_date: bool = False
  ):
  """
  Transforms a date list into a string date list

  Note: even when an element is not a datetime.date and raises_if_any_not_date = False,
    this function also guarantees that the elements are transformable to dates
    so that the end result will a list in which elements are in the form yyyy-mm-dd,
    i.e., year dash month dash day
  """
  strdatelist = []
  for pdate in datelist:
    if not isinstance(pdate, datetime.date):
      if raises_if_any_not_date:
        errmsg = f'Error: An element (date={pdate}) is not a date in trans_datelist_to_strdatelist(). Halting.'
        raise TypeError(errmsg)
      else:
        continue
    if pdate is None:
      if raises_if_any_not_date:
        errmsg = f'Error: An element (date={pdate}) is not a date in trans_datelist_to_strdatelist(). Halting.'
        raise TypeError(errmsg)
      else:
        continue
    odate = copy.copy(pdate)
    if not isinstance(odate, datetime.date):
      odate = make_date_or_none(odate)
      if odate is None:
        if raises_if_any_not_date:
          errmsg = (f'Error: An element (date={pdate}) is not convertible-to-date in trans_datelist_to_strdatelist().'
                    f' Halting.')
          raise TypeError(errmsg)
        else:
          continue
    strdate = str(odate)
    strdatelist.append(strdate)
  return strdatelist


def make_random_dates(p_n_randomdates_to_make=3, dateini=None, datefim=None):
  """
  5, '2025-05-09', '2025-07-09'
  """
  try:
    n_randomdates_to_make = int(p_n_randomdates_to_make)
  except TypeError:
    n_randomdates_to_make = DEFAULT_N_RANDOMDATES_TO_MAKE
  radius = n_randomdates_to_make * 3
  today = datetime.date.today()
  dateini = make_date_or_none(dateini)
  if dateini is None:
    dateini = today - relativedelta(days=radius)
  datefim = make_date_or_none(datefim)
  if datefim is None:
    datefim = today
  if dateini > datefim:
    tmpdate = datefim
    datefim = dateini
    dateini = tmpdate
  n_days_between = datefim - dateini
  days_bucket_indices = list(range(n_days_between.days))
  randomdates = []
  while len(randomdates) < n_randomdates_to_make or len(days_bucket_indices) == 0:
    yet_to_draw = len(days_bucket_indices)
    index_drawn = random.randint(0, yet_to_draw-1)
    del days_bucket_indices[index_drawn]
    randomdate = dateini + relativedelta(days=index_drawn)
    randomdates.append(randomdate)
  randomdates.sort()
  return randomdates


def swap_dates_if_first_is_greater_than_second(date1, date2):
  date1 = make_date_or_none(date1)
  if date1 is None:
    errmsg = "Error: first date in swap_dates_if_first_is_greater_than_second(first, second) is None."
    raise ValueError(errmsg)
  date2 = make_date_or_none(date2)
  if date2 is None:
    errmsg = "Error: second date in swap_dates_if_first_is_greater_than_second(first, second) is None."
    raise ValueError(errmsg)
  if date1 > date2:
    # swap them so that second is greater (as date1 > date2 already rules out equality between the two) than first
    tmpdate = date1
    date1 = date2
    date2 = tmpdate
  return date1, date2


def adhoc_test():
  class C1:
    def __init__(self, year=None, month=None, day=None):
      self.year = year
      self.month = month
      self.day = day

  y, m, d = 2020, 7, 3
  expected_date = datetime.date(year=y, month=m, day=d)
  attrs_obj = C1(y, m, d)
  returned_date = make_date_or_none(attrs_obj)
  print('attrs_obj', attrs_obj.year)
  print(expected_date, returned_date)


def adhoc_test2():
  # swap
  d1 = '2025-06-15'
  d2 = '2025-06-5'
  scrmsg = f"date1={d1} & date2={d2}"
  print(scrmsg)
  d1, d2 = swap_dates_if_first_is_greater_than_second(d1, d2)
  scrmsg = f"after swap: date1={d1} & date2={d2}"
  print(scrmsg)


def adhoctest3():
  text = """
  2010-11-07 Luiz Lewis
  2013-11-07 Alex Escobar
  2030-11-07 Ann Rose
  1999-11-07 Mary Ann
  """
  print(text)
  strlines = text.split('\n')
  notsorted = get_first_tuple_elem_splitting_prefixdate_n_name_fr_lines(strlines)
  print(f"notsorted = {notsorted}")
  newest = find_newest_name_n_its_prefix_date_in_strlist(strlines)
  print(f"newest = {newest}")
  oldest = find_oldest_name_n_its_prefix_date_in_strlist(strlines)
  print(f"oldest = {oldest}")
  n_dates, dateini, datefim = 5, '2025-05-09', '2025-07-09'
  randomdates = make_random_dates(n_dates, dateini, datefim)
  scrmsg = f"""n_dates, dateini, datefim = {n_dates}, {dateini}, {datefim}
  randomdates = {randomdates}"""
  print(scrmsg)
  strdatelist = ['2025-05-09', '2025-07-09']
  print('strdatelist', strdatelist)
  datelist = trans_convertabledates_to_datelist(strdatelist)
  print('datelist trans_convertabledates_to_datelist', datelist)
  ret_strdatelist = trans_datelist_to_strdatelist(datelist)
  print('ret_strdatelist trans_datelist_to_strdatelist', ret_strdatelist)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  adhoc_test2()
  """
  adhoctest3()
