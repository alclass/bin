#!/usr/bin/env python3
"""
Author: @LuizLewis
Obs: upgrading to Python 3 on 2021-03-13 in parallel improving script to class-based processing.
"""
import glob
import os
import string
import sys


class Renamer:
  """
  This class takes a start number as parameter, loops thru all files on folder,
    prefixes numbers sequencially to all files, asks rename confirmation,
    if confirmed, renames all files on folder.
  """

  def __init__(self, start_number):
    """
    start_number determines the first prefix number for renames
    The numbering goes along the alphanumeric ordering given by sorted(files)
    """
    self.start_number = start_number
    self.rename_pairs = []
    self.zfillsize = None
    self.process_rename()

  def prep_rename(self):
    """
    Prepare renames
    """
    files = os.listdir('.')
    sorted(files)
    total_files = len(files)
    self.zfillsize = len(str(total_files))
    fileseq = self.start_number
    for i, filename in enumerate(files):
      new_filename = str(fileseq).zfill(self.zfillsize) + ' ' + filename
      seq = i + 1
      print(str(seq).zfill(self.zfillsize), 'Renaming: [' + filename + ']')
      print(str(seq).zfill(self.zfillsize), '>>>   To: [' + new_filename + ']')
      pair = (filename, new_filename)
      self.rename_pairs.append(pair)
      fileseq += 1
    print('total_files', total_files)

  def confirm_rename(self):
    """
    Returns True if user types either y or Y or '' (nothing)
    """
    print('There are', len(self.rename_pairs), 'renames.')
    ans = input('Are you sure to rename? (*Y/n) ')
    if ans in ['y', 'Y', '']:
      return True
    print ('No renames.')
    return False

  def do_rename(self):
    """
    Executes renames that are "buffered" in self.rename_pairs
    """
    n_renames = 0
    for i, pair in enumerate(self.rename_pairs):
      seq = i + 1
      filename, new_filename = pair
      if not os.path.isfile(filename):
        print(seq, 'File [%s] does not exist.')
        continue
      if os.path.isfile(new_filename):
        print(seq, 'File [%s] already exists.')
        continue
      print(str(seq).zfill(self.zfillsize), 'Renaming: [' + filename + ']')
      print(str(seq).zfill(self.zfillsize), '>>>   To: [' + new_filename + ']')
      os.rename(filename, new_filename)
      n_renames += 1
      print ('n_renames = ', n_renames)

  def process_rename(self):
    """
    Process renames on folder
    """
    self.prep_rename()
    if self.confirm_rename():
      self.do_rename()


def process():
  start_number = 1
  try:
    start_number = int(sys.argv[1])
  except (IndexError, ValueError):
    pass
  print('start_number', start_number)
  Renamer(start_number)


if __name__ == "__main__":
    process()
