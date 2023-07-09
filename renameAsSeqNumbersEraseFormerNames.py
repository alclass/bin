#!/usr/bin/env python3
"""
CAUTION:
  this script will, if prompt-confirmed, "destroy" the former names
  as the new names will be only numbers sequencially augmenting (1, 2, 3, 4...)

Usage:
$this_script.py -e=[<extension>]

Example: suppose the following files are in the current directory:
  "F1 file foo bar.mp4"
  "F2 file bar foo.mp4"
Running this script and confirming the operation, the (renamed) new names will be:
  "1.mp4"
  "2.mp4"

CAUTION AGAIN:
  this operation, if confirmed, can not be undone, so, if possible, make a back-up before running it.
"""
# import glob
import math
import os
import sys
DEFAULT_EXTENSION = '.mp4'


def adjust_front_dot_if_needed(ext):
  if not ext.startswith('.'):
    ext = '.' + ext
  return ext


def return_only_filenames_under_ext(filenames, dir_abspath=None, extension=None):
  """

  absfiles = map(lambda fn: os.path.join(dir_abspath, fn), filenames)
  # remove entries that are not files
  absfiles = filter(lambda filepath: os.path.isfile(filepath), absfiles)
  # split the abspaths getting back the filenames
  filenames = [os.path.split(abspath)[1] for abspath in absfiles]

  :param filenames:
  :param dir_abspath:
  :param extension:
  :return:
  """
  if len(filenames) == 0:
    return []
  if dir_abspath is None:
    dir_abspath = os.path.abspath('.')
  _ = dir_abspath
  if extension is None:
    extension = DEFAULT_EXTENSION
  # ini_size = len(filenames)
  filenames = list(filter(lambda fn: fn.endswith(extension), filenames))
  filenames.sort()
  # join filenames with dir_abspath making a list of file abspaths
  absfiles = map(lambda fn: os.path.join(dir_abspath, fn), filenames)
  # remove entries that are not files
  absfiles = list(filter(lambda filepath: os.path.isfile(filepath), absfiles))
  # split the abspaths getting back the filenames (with Python's list-comprehension)
  filenames = [os.path.split(abspath)[1] for abspath in absfiles]
  filenames.sort()
  # print('len filenames', len(filenames), 'ini_size', ini_size)
  return filenames


class Renamer:
  """

  """
  
  def __init__(self, ext_for_rename=None, dir_abspath=None):
    """
    """
    self.is_renames_confirmed = False
    self.rename_pairs = []
    if ext_for_rename is None:
      self.ext_for_rename = DEFAULT_EXTENSION
    else:
      self.ext_for_rename = ext_for_rename
    self.ext_for_rename = adjust_front_dot_if_needed(self.ext_for_rename)
    if dir_abspath is None or not os.path.isdir(dir_abspath):
      self.dir_abspath = os.path.abspath('.')
    else:
      self.dir_abspath = dir_abspath

  def find_files_from_current_folder(self):
    self.rename_pairs = []
    files = os.listdir(self.dir_abspath)
    files = return_only_filenames_under_ext(files, self.dir_abspath, self.ext_for_rename)
    files.sort()
    total_files = len(files)
    if total_files < 1:
      print('No files to rename.')
      return
    zfill_size = int(math.log(total_files, 10) + 1)
    self.rename_pairs = []
    for i, f in enumerate(files):
      seq = i + 1
      outfilename = '%s' + self.ext_for_rename
      seqstr = str(seq).zfill(zfill_size)
      outfilename = outfilename % seqstr
      rename_pair = f, outfilename
      self.rename_pairs.append(rename_pair)

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
    self.find_files_from_current_folder()
    self.confirm_renames()
    if self.is_renames_confirmed:
      self.do_renames()


def get_argdict():
  argdict = {'ext_for_rename': None}
  for arg in sys.argv:
    if arg.startswith('-o='):
      ext_for_rename = arg[len('-o='):]
      argdict['ext_for_rename'] = ext_for_rename
  return argdict


def process():
  """
  """
  argdict = get_argdict()
  ext_for_rename = argdict['ext_for_rename']
  renamer = Renamer(ext_for_rename)
  renamer.process_rename()


def test_return_only_filenames_under_ext():
  """
  This tests function return_only_filenames_under_ext(filenames, ppath, externsion)
    that receives a list of files and return those that have the extension given and are files
      (instead of the other two types: directories and links [Unix-links])
  :return:
  """
  hardcodedpath = "/home/dados/VideoAudio/Yt videos/Soc Sams vi/Lang Sams vi/Chinese Sams vi/" \
      "Harbin Mandarin yu/BMC 19v 12' 2018 4h Beginning Mandarin Chinese Lessons yu Harbin ytpl/a"
  path_in_arg_if_any = None
  for arg in sys.argv:
    if arg.startswith('-ppath='):
      path_in_arg_if_any = arg[len('-ppath='):]
  if path_in_arg_if_any is None:
    path_in_arg_if_any = hardcodedpath
  ppath = path_in_arg_if_any
  filenames = os.listdir(ppath)
  filenames.sort()
  print(filenames)
  retlist = return_only_filenames_under_ext(filenames, ppath)
  print(retlist)


if __name__ == '__main__':
  # test_return_only_filenames_under_ext()
  process()
