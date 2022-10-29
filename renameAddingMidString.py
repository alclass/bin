#!/usr/bin/env python3
# No longer need in Python3: -*- coding: utf-8 -*-
"""
Usage:
$renameAddingMidString.py -e=[<extension>] -p=[<pos>] -i="<string-to-be-added>"

Parameters:
  -i="<string-to-be-added>" :: string to be inclused, required
  -e=[<extension>] :: file extension, optional, if none is given, "mp4" will be used
  -p=[<pos>] :: integer index position in name, optional,
                if none is given, "0" will be used; -1 means "include at the end"
  -d="<absolute_path_to_rename_folder>" :: string represent the abspath to rename folder, optional,
                if none is given, running folder will be used

Example:
  renameCleanSpecifiedStr.py -e=pdf -i=" [John Surname]" -p=-1 -d="."

With the example above, files such as (in the current folder, notice -d=".":
  "The book of science.pdf" & This book.pdf"
will be renamed to:
  "The book of science [John Surname].pdf" & This book [John Surname].pdf"

Another example:

renameAddingMidString.py
  -e=pdf
  -i=" yyyy Friedrich Nietzsche [archive-org]"
  -p=-1
  -d="/home/dados/Books/Books pdf/Social Sci pdf Bks/Philosophy pdf Bks/
      Individual Philosophers pdf Bks/Nietzche, Friedrich pdf Bks"

"""
# import glob
import os
import sys


DEFAULT_EXTENSION = 'mp4'


def extract_filename_from_files(files, extension):
  filenames = []
  for f in files:
    _, filename = os.path.split(f)
    if filename.endswith(extension):
      filenames.append(filename)
  return filenames


def clean_emptystr_inlist(listin):
  return list(filter(lambda c: c != '', listin))


class Renamer:
  """

  """
  
  def __init__(self, include_str, ext_list_as_str=None, pos=0, dir_abspath=None):
    """
    """
    self.rename_pairs = []
    self.is_renames_confirmed = False
    if include_str is None or include_str == '' or type(include_str) != str:
      error_msg = ' Error:\n Cannot continue without an include string.\n Please retry entering an include string.'
      raise ValueError(error_msg)
    else:
      self.include_str = include_str
    self.ext_list = []
    self.set_extlist(ext_list_as_str)
    self.pos = None
    self.set_pos(pos)
    self.dir_abspath = None
    self.set_dir_abspath(dir_abspath)

  def set_dir_abspath(self, dir_abspath):
    if dir_abspath is None or dir_abspath == '.':
      self.dir_abspath = os.path.abspath('.')
      return
    if os.path.isdir(dir_abspath):
      self.dir_abspath = dir_abspath
      return
    self.dir_abspath = os.path.abspath('.')

  def set_pos(self, pos):
    """

    :param pos:
    :return:
    """
    if pos is None:
      self.pos = 0
      return
    try:
      self.pos = int(pos)
    except ValueError:
      self.pos = 0
    # if program flow gets here, self.pos is set and of type int
    if self.pos < -1:  # -1 means "include at the end", circular position has not been implemented yet
      self.pos = 0

  def set_extlist(self, ext_list):
    """
    extList is treated here as transfered-by-copy,
      ie, it's not passed as reference below, being copied on place

    :param ext_list:
    :return:
    """
    if ext_list is None or len(ext_list) == 0:
      self.ext_list = [DEFAULT_EXTENSION]
      return
    try:
      ext_list = str(ext_list)
    except ValueError:
      self.ext_list = [DEFAULT_EXTENSION]
      return
    if ext_list.find(',') < 0:
      self.ext_list = [ext_list]
      return
    self.ext_list = []
    extensions = ext_list.split(',')
    for ext in extensions:
      self.ext_list.append(ext)

  def add_str_inbetween(self, name, filename):
    if len(name) < self.pos:
      return None
    before_str = filename[0: self.pos]
    after_str = filename[self.pos:]
    new_name = before_str + self.include_str + after_str
    return new_name

  def prepare_renames_for_filename(self, old_filename):
    """

    if name.endswith(self.include_str) or name.find(self.include_str) > -1:
      print('Filename [%s] has already included the given string to be added.' % name)
      return

    :param old_filename:
    :return:
    """
    name, ext_with_dot = os.path.splitext(old_filename)
    if self.pos == -1:
      new_name = name + self.include_str
    else:
      new_name = self.add_str_inbetween(name, old_filename)
    if new_name is None:
      return
    new_namefilename = new_name  # + ext_with_dot
    rename_pair = (old_filename, new_namefilename)
    self.rename_pairs.append(rename_pair)

  def prepare_renames_for_extension(self, extension):
    """
    # glob_str = '*.' + extension
    # files = glob.glob(glob_str)
    :param extension:
    :return:
    """
    files = os.listdir(self.dir_abspath)
    filenames = extract_filename_from_files(files, extension)
    for old_filename in filenames:
      self.prepare_renames_for_filename(old_filename)

  def prepare_renames(self):
    self.rename_pairs = []
    for extension in self.ext_list:
      self.prepare_renames_for_extension(extension)

  def confirm_renames(self):
    self.is_renames_confirmed = False
    if len(self.rename_pairs) == 0:
      print('No files to rename.')
      return
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      print(seq, 'Rename:')
      old_name, new_name = rename_pair
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
    screen_msg = 'Confirm the %d renames above ? (*Y/n) ([ENTER] means Yes) ' % len(self.rename_pairs)
    ans = input(screen_msg)
    if ans in ['Y', 'y', '']:
      self.is_renames_confirmed = True
      return

  def do_renames(self):
    if not self.is_renames_confirmed:
      print('Renames not confirmed.')
      return
    print('-'*40)
    n_renamed = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      old_filename, new_filename = rename_pair
      old_file_absfile = os.path.join(self.dir_abspath, old_filename)
      new_file_absfile = os.path.join(self.dir_abspath, new_filename)
      if not os.path.isfile(old_file_absfile):
        continue
      if os.path.isfile(new_file_absfile):
        continue
      seq = i + 1
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_filename)
      print('TO:   >>>%s' % new_filename)
      os.rename(old_file_absfile, new_file_absfile)
      n_renamed += 1
    print('-'*40)
    print('Finished %d rename pairs.' % len(self.rename_pairs))
    print('Total renamed:', n_renamed)

  def process_rename(self):
    self.prepare_renames()
    self.confirm_renames()
    if self.is_renames_confirmed:
      self.do_renames()


def get_args():
  pos = 0
  ext_list_as_str = ''
  include_str = None
  folder_abspath = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      ext_list_as_str = arg[len('-e='):]
    elif arg.startswith('-p='):
      pos = arg[len('-p='):]
    elif arg.startswith('-i='):
      include_str = arg[len('-i='):]
    elif arg.startswith('-d='):
      folder_abspath = arg[len('-d='):]
  return include_str, ext_list_as_str, pos, folder_abspath


def process():
  """
  """
  include_str, ext_list_as_str, pos, folder_abspath = get_args()
  renamer = Renamer(include_str, ext_list_as_str, pos, folder_abspath)
  renamer.process_rename()


if __name__ == '__main__':
  process()
