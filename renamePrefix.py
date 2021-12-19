#!/usr/bin/env python3
"""
This script renames files in a directory prepending their names them with a "prefix".
It's possible to define an extension (parameter "-e=<ext>") so that only files with that extension will be renamed.

Usage:
  renamePrefix.py "<prefix-str>" [-e=<ext>]

Example:
  renamePrefix.py "all mp4 files get this - -e=mp4

Obs:
  1) This script, at this time, doesn't work when running from a different directory
    (it may be changed in the future to make it more flexible, ie to make it able to be run from any location);
  2) when not using an extension parameter, files and directories will be renamed.
"""
import os
import sys  # shutil, sys


class Renamer:
  """
  This class processes the renaming logics. It works as a job-chain, ie each method prepares a part of the whole.
    Take a look at method process() to observe the pieces in the job-chain.
  """

  def __init__(self, prefix, extension):
    self.prefix = prefix
    self.extension = extension
    self.rename_pairs = []
    self.process_renames()

  def prep_renames(self):
    if self.extension is None:
      files = os.listdir('.')
    else:
      files = os.listdir('.' + self.extension)
    if len(files) == 0:
      print('No files to rename.')
      return
    sorted(files)
    zfillsize = len(str(len(files)))
    for i, filename in enumerate(files):
      seq = i + 1
      new_filename = self.prefix + filename
      pair = (filename, new_filename)
      self.rename_pairs.append(pair)
      print(str(seq).zfill(zfillsize), 'Renaming: [' + filename + ']')
      print(str(seq).zfill(zfillsize), '> to:', new_filename)

  def confirm_renames(self):
    if len(self.rename_pairs) == 0:
      return
    total_files = len(self.rename_pairs)
    print('total_files', total_files)
    ans = input('Are you sure? (*Y/n) ')
    if ans in ['y', 'Y', '']:
      return True
    return False

  def do_renames(self):
    if len(self.rename_pairs) == 0:
      return
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
      print(str(seq).zfill(zfillsize), 'Renaming: [' + filename + ']')
      print(str(seq).zfill(zfillsize), '> to:', new_filename)
      os.rename(filename, new_filename)
      n_renames += 1
    print('n_renames', n_renames, 'total_files', total_files)

  def process_renames(self):
    self.prep_renames()
    if self.confirm_renames():
        self.do_renames()


def get_prefix_n_extension_arg():
  """
  Gets the parameter arguments from the command line
  :return prefix, extension:
  """
  extension = None
  if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(0)
  prefix = sys.argv[1]
  if len(sys.argv) > 2:
    for arg in sys.argv[2:]:
      if arg.startswith('-e='):
        extension = arg[len('-e='):]
  return prefix, extension


def process():
  prefix, extension = get_prefix_n_extension_arg()
  Renamer(prefix, extension)


if __name__ == '__main__':
  process()
