#!/usr/bin/env python3
"""
~/bin/extractDateInExtensionAndSecondColumn.py
  Initially, this scripts aimed to transform the following text:

From:
---------------------
08 de janeiro de 2026	 # OBM4198913-01

12 de dezembro de 2025	 # OBM4067371-01

11 de dezembro de 2025	 # OBM4060034-01
---------------------

To:
---------------------
2026-01-08\tOBM4198913-01
2025-12-12\tOBM4067371-01
2025-12-11\tOBM4060034-01
---------------------

Defaults:
  current directory => the current working directory
  data filename => 'dates and ordernumbers.txt'

"""
import datetime
import os
from pathlib import Path
import sys
DEFAULT_DATAFILENAME = 'dates and ordernumbers.txt'
meses = [
  'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro',
]


class TextCleaner:

  def __init__(self, filepath=None, text=None):
    self.filepath = filepath
    self.text = text
    self.lines = []
    self.result_list = []

  def remove_repeats(self):
    """
    TODO: adapt module uniquetuples.py in lblib.collections
      so that it removes the tuples when both values have repeats in list
    :return:
    """
    print('size', len(self.result_list))
    c = 0
    n_deleted = 0
    while c < len(self.result_list) - 2:
      c_deleted = False
      tupl1 = self.result_list[c]
      for i in range(c + 1, len(self.result_list)):
        tupl2 = self.result_list[i]
        if tupl1 == tupl2:
          del self.result_list[c]
          n_deleted +=1
          print(n_deleted, 'DELETED', c, 'equals to', i, tupl2)
          c_deleted = True
          break
      if c_deleted:
        continue
      c += 1
    print('size', len(self.result_list))
    print('n_deleted', n_deleted)


  def extract_columns_fr_line(self, line):
    pp = line.split('#')
    if len(pp) < 2:
      return
    strdate = pp[0]
    strpiece = pp[1]
    triple = strdate.split(' de ')
    day = int(triple[0])
    longmonth = triple[1]
    year = int(triple[2])
    nmonth = meses.index(longmonth) + 1
    pdate = datetime.date(year=year, month=nmonth, day=day)
    tupl = pdate, strpiece
    self.result_list.append(tupl)

  def extract_columns(self):
    """
    The first column is a date with 'de'/'de'
    The second column starts with a '#'
    :return:
    """
    for line in self.lines:
      self.extract_columns_fr_line(line)

  def fetch_text_if_needed(self):
    if self.filepath:
      with open(self.filepath) as f:
        self.text = f.read()
    self.lines = self.text.split('\n')

  def process(self):
    self.fetch_text_if_needed()
    self.extract_columns()
    self.remove_repeats()
    self.show_output()

  def show_output(self):
    for tupl in self.result_list:
      pdate = tupl[0]
      piece = tupl[1]
      scrmsg = f"{pdate}\t{piece}"
      print(scrmsg)


def adhoctest1():
  """
  """
  t = """
08 de janeiro de 2026	 # OBM4198913-01

12 de dezembro de 2025	 # OBM4067371-01

11 de dezembro de 2025	 # OBM4060034-01  
  """
  tc = TextCleaner(text=t)
  tc.process()


def get_args():
  fopath, fn = None, None
  for arg in sys.argv[1:]:
    if arg.startswith('-h'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-dp='):
      fopath = arg[len('-dp='):]
    elif arg.startswith('-fn='):
      fn = arg[len('-fn='):]
  fopath = fopath or Path(os.getcwd())
  fn = fn or DEFAULT_DATAFILENAME
  return fopath, fn


def get_datafilepath():
  dirpath, filename = get_args()
  datafile = Path(dirpath, filename)
  return datafile


def process():
  datafile = get_datafilepath()
  tc = TextCleaner(filepath=datafile)
  tc.process()


if __name__ == '__main__':
  """
  adhoctest1()
  process()
  """
  process()
