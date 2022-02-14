#!/usr/bin/env python3
"""
This script extracts (removes) a specified Reg Exp mark-string from all filenames having a chosen extension.

The example below (in future versions will be a "preset"):

$ renameCleanRegExp.py -e=mp4 -r="\[\w+\d*\]+"

will do the following:

=> each filename in the current folder having letters (at least one) or numbers within square brackets will have that part (letters or numbers within square brackets) removed;

=> Suppose the following filenames are available:
    fn1 "file 1 [blah] [bla] foo.mp4
    fn2 "file2 [blah 123] bar.mp4
    fn3 "file3 blah.mp4

Running:
$ renameCleanRegExp.py -e=mp4 -r="\[\w+\d*\]+"

The renames will be:
    fn1 to "file 1  foo.mp4
    fn2 to "file2  bar.mp4

Notice fn3 is not renamed (it does not match regexp "\[\w+\d*\]+")
:: meaning: letters (at least one [+]) or numbers (zero or more [*]) within square brackets

Obs: the additional parameter -y will rename without confirmation (take care when using this "auto" parameter, take even more care because regexp act sometimes not what we think they should!...)
"""
import glob
import os
import re
import sys


DEFAULT_RENAME_EXTENSION = 'mp4'


class Renamer:
  """
  class Renamer:
  """
  def __init__(self, specified_restr, extension=None, autorename_without_confirmation=False, abspath=None):
    """

    :param specified_str:
    :param extension:
    :param abspath:
    """
    self.specified_restr = specified_restr
    self.extension = extension
    if self.extension is None:
      self.extension = DEFAULT_RENAME_EXTENSION
    self.abspath = abspath
    if self.abspath is None or not os.path.isdir(self.abspath):
      self.abspath = os.path.abspath('.')
    self.target_filenames = []
    self.n_target_filenames = 0
    self.rename_pairs = []
    self.n_renames = 0
    self.autorename_without_confirmation = autorename_without_confirmation
    self.user_has_confirmed_interactively = False
    # self.rename_process()

  def prepare_for_rename(self):
    """

    :return:
    """
    print("Folder (from the command line, not yet implemented as a generic API) =>")
    print(self.abspath)
    print("Replace Reg Exp str =>", self.specified_restr)
    for i, target_filename in enumerate(self.target_filenames):
      re_match_o = re.search(self.specified_restr, target_filename)
      print('Trying to match', self.specified_restr, 'in', target_filename)
      if re_match_o is None:
        continue
      remove_str = re_match_o.group(0)
      if len(remove_str) > 0:
        newname = target_filename.replace(remove_str, '')
        if os.path.isfile(newname):
          continue
        rename_pair = (target_filename, newname)
        self.rename_pairs.append(rename_pair)
        seq = i + 1
        print(seq, ' => Rename:')
        print('FROM:', target_filename)
        print('TO:  ', newname)

  def confirm_the_renames_if_any(self):
    self.user_has_confirmed_interactively = False
    if len(self.rename_pairs) == 0:
      return
    screen_msg = 'Rename the %d files shown above (*Y/n) ? ' % len(self.rename_pairs)
    ans = input(screen_msg)
    if ans in ['Y', 'y', '']:
      self.user_has_confirmed_interactively = True

  def do_rename(self):
    """

    :return:
    """
    if len(self.rename_pairs) == 0:
      print('No files to rename.')
      return
    self.n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      target_filename = rename_pair[0]
      new_namefile = rename_pair[1]
      if not os.path.isfile(target_filename):
        continue
      if os.path.isfile(new_namefile):
        continue
      self.n_renames += 1
      print('FROM =>', target_filename)
      print('TO   =>', new_namefile)
      os.rename(target_filename, new_namefile)

  def rename_process(self):
    """

    :return:
    """
    os.chdir(self.abspath)
    self.target_filenames = glob.glob('*.' + self.extension)
    print('total files:', len(self.target_filenames))
    self.prepare_for_rename()
    print('autorename_without_confirmation', self.autorename_without_confirmation)
    if self.autorename_without_confirmation:
      self.do_rename()
    else:
      self.confirm_the_renames_if_any()
      if self.user_has_confirmed_interactively:
        self.do_rename()
    self.show_numbers()

  def show_numbers(self):
    """

    :return:
    """
    print('Number of rename pairs:', len(self.rename_pairs))
    print('Number of renamed:',      self.n_renames)


def get_str_arg():
  specified_restr = None
  autorename_without_confirmation = False
  ext = None
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-r='):
      specified_restr = arg[len('-r='):]
    elif arg.startswith('-e='):
      ext = arg[len('-e='):]
    elif arg in ['-Y', '-y']:
      autorename_without_confirmation = True
  if specified_restr is None:
    print(__doc__)
    error_msg = 'specified_str is missing. Program cannot continue.'
    raise ValueError(error_msg)
  return specified_restr, ext, autorename_without_confirmation


def process():
  specified_restr, extension, autorename_without_confirmation = get_str_arg()
  print(
    'Input parameters:',
    'specified_restr [', specified_restr, ']',
    '| extension [', extension, ']',
    '| autorename', autorename_without_confirmation
  )
  renamer = Renamer(specified_restr, extension, autorename_without_confirmation)
  renamer.rename_process()


if __name__ == '__main__':
  process()
