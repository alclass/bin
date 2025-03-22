#!/usr/bin/env python3
"""
renameRemovingASpecStrTokenPlusASizeOffset.py

This script renames files in a directory following the conditions:
1) a renamable file should contain a "specified string" (SpecStrToken)
  1.1) the SpecStrToken is to be removed from name
2) immediately following SpecStrToken, a certain number of characters
  2.1) this continuation in charsize is also to be removed
  2.2) SpecStrToken is counted in the charsize length given

IMPORTANT:
  => At the time of writing, full paths do not yet work with this script, only local directories.

Usage:
  $<this_script> -s="<SpecStrToken>" [-c=<continuation_sizelength>]
where:
  -s is the specified string to be removed (clean up from name)
  -c is an integer for the continuation size length, this number includes the size of SpecStrToken
     if c is not given, size will fall back to SpecStrToken's size

Example:
  Suppose a directory with 3 filenames, ie:
    => "register 1 _25_03_19_20_42_00 done.txt"
    => "register 2 _25_03_20_20_08_05 almost done.txt"
    => "register 3 _25_03_21_19_58_31 yet to begin.txt"

Running:
  $<this_script> -s="_25_03"> -c=18

Will result the following renamed (cleaned up) filenames:
  => "register 1 done.txt"
  => "register 2 almost done.txt"
  => "register 3 yet to begin.txt"

"""
import glob
import os.path
import sys
default_specstr = '_25_03_'  # all renamable files have this specstr
default_specstrsize = len('_25_03_21_20_31_39')  # it should be 3*6=18, only size matters here not the str content
default_dot_ext = '.pdf'


class Renamer:

  def __init__(self, specstr=None, whole_removal_strsize=None, dot_ext=None):
    self.specstr = specstr
    self.whole_removal_strsize = whole_removal_strsize
    self.treat_specstr_n_size()
    self.dot_ext = dot_ext
    self.pdf_filenames = []
    self.rename_pairs = []
    self.rename_confirmed = None
    self.process()

  def treat_specstr_n_size(self):
    if self.specstr is None:
      self.specstr = default_specstr
    if self.whole_removal_strsize is None:
      self.whole_removal_strsize = len(self.specstr)

  def treat_dot_ext(self):
    if self.dot_ext is None:
      self.dot_ext = default_dot_ext
    if not self.dot_ext.startswith('.'):
      self.dot_ext = '.' + self.dot_ext

  def gather_files(self):
    param_glob = '*' + self.dot_ext
    self.pdf_filenames = glob.glob(param_glob)

  def derive_newfilenames(self):
    seq = 0
    for filename in self.pdf_filenames:
      idx = filename.find(specstr)
      if idx > -1:
        nextidx = idx + specstrsize
        newfilename = filename[:idx] + filename[nextidx:]
        seq += 1
        print(seq)
        print('FROM: ', filename)
        print('  TO: ', newfilename)
        rename_pair = (filename, newfilename)
        self.rename_pairs.append(rename_pair)

  def confirm_renames(self):
    n_renamepairs = len(self.rename_pairs)
    if n_renamepairs == 0:
      print('No files to rename.')
      return
    scrmsg = "Confirm renaming the %d renames above? (Y/n) [ENTER] means Yes " % n_renamepairs
    ans = input(scrmsg)
    self.rename_confirmed = False
    if ans in ['Y', 'y', '']:
      self.rename_confirmed = True

  def do_renames(self):
    if len(self.rename_pairs) == 0:
      print('No files to rename.')
      return
    if not self.rename_confirmed:
      print('Not renaming files.')
      return
    seq = 0
    for rename_pair in self.rename_pairs:
      filename, newfilename = rename_pair
      seq += 1
      if not os.path.isfile(filename):
        print(seq, 'source filename', filename, 'does not exist, not renaming, continuing...')
      if os.path.isfile(newfilename):
        print('target filename', filename, 'exists, not renaming, continuing...')
      seq += 1
      print('FROM: ', filename)
      print('  TO: ', newfilename)
      os.rename(filename, newfilename)
      print(seq, 'renamed')

  def process(self):
    self.gather_files()
    self.derive_newfilenames()
    self.confirm_renames()
    self.do_renames()


def get_args():
  specstr, whole_removal_strsize, dot_ext = None, None, None
  for arg in sys.argv:
    if arg.startswith('-h'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-s='):
      specstr = arg[len('-s='):]
    elif arg.startswith('-c='):
      whole_removal_strsize = int(arg[len('-c='):])
    elif arg.startswith('-e='):
      dot_ext = arg[len('-e='):]
  return specstr, whole_removal_strsize, dot_ext


def process():
  """

  """
  specstr, whole_removal_strsize, dot_ext = get_args()
  Renamer(specstr, whole_removal_strsize, dot_ext)


if __name__ == "__main__":
  process()
