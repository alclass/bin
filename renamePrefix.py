#!/usr/bin/env python3
import os
import sys  # shutil, sys


class Renamer:

  def __init__(self, prefix):
    self.prefix = prefix
    self.rename_pairs = []
    self.process_renames()

  def prep_renames(self):
    files = os.listdir('.')
    sorted(files)
    zfillsize = len(str(len(files)))
    for i, filename in enumerate(files):
      seq = i + 1
      new_filename = self.prefix + filename
      pair = (filename, new_filename)
      self.rename_pairs.append(pair)
      print (str(seq).zfill(zfillsize), 'Renaming: [' + filename + ']')
      print (str(seq).zfill(zfillsize), '> to:', new_filename)

  def confirm_renames(self):
    total_files = len(self.rename_pairs)
    print ('total_files', total_files)
    ans = input('Are you sure? (*Y/n) ')
    if ans in ['y', 'Y', '']:
      return True
    return False

  def do_renames(self):
    total_files = len(self.rename_pairs)
    n_renames = 0
    zfillsize = len(str(total_files))
    for i, pair in enumerate(self.rename_pairs):
      filename, new_filename = pair
      if not os.path.isfile(filename):
        print('File [' + filename + '] does not exist.')
        continue
      if os.path.isfile(new_filename):
        print('File [' + filename + '] already exists.')
        continue
      seq = i + 1
      print (str(seq).zfill(zfillsize), 'Renaming: [' + filename + ']')
      print (str(seq).zfill(zfillsize), '> to:', new_filename)
      os.rename(filename, new_filename)
      n_renames += 1
    print ('n_renames', n_renames, 'total_files', total_files)

  def process_renames(self):
    self.prep_renames()
    if self.confirm_renames():
        self.do_renames()


def get_prefix_arg():
  """

  :return:
  """
  prefix = sys.argv[1]
  return prefix


def process():
  prefix = get_prefix_arg()
  Renamer(prefix)


if __name__ == '__main__':
  process()
