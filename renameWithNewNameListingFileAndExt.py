#!/usr/bin/env python3
"""
renameWithNewNameListingFileAndExt.py
  This script renames files with a certain extension (@see default value below) in alphabetical order
    with the names in a text file (whose default filename is also given below)

Usage:
  $renameWithNewNameListingFileAndExt.py [-e=<fileextension>] [-n="<textfilename>"] [-w="<workdir_abspath>"]

Where:
  fileextension => the desired file extension for the files to be renamed (eg '.txt')
  textfilename => the filename that contains the new names for the files to be renamed
  workdir_abspath => the directory where the renaming is to be processed

Example:

  1) $renameWithNewNameListingFileAndExt.py -e="mp3" -n="new-names.txt"
    In this example, the mp3 files, in alphabetical order, will be renamed with the new filenames
      stored in text file "new-names.txt"

  2) $renameWithNewNameListingFileAndExt.py
    This example is when the user wants to apply the two default parameters, ie,
      2-1 default extension is '.mp4'
      2-2 default filename is 'course-titles.txt'
    So, in this example, the mp4 files, in alphabetical order, will be renamed with the new filenames
      stored in text file "course-titles.txt"

Some historical notes:

  On 2025-05-25:
    This script was probably written before 2010 in Python 2
       and finally ported to Python 3

  On 2025-06-02:
    This script was refactored for running with absolute paths
"""
import os
import sys
DEFAULT_EXT = 'mp4'
DEFAULT_NEW_NAME_LISTING_FILE = 'course-titles.txt'


class InputArguments:
  """
  Simple/helper class to organize the two CLI parameters (*) for the renaming

  (*) parameters:
    1 => -e : file extension (default to '.mp4')
    2 => -n : data file's filename that contains the new renaming filenames
  """

  def __init__(self):
    self.should_be_ext = DEFAULT_EXT
    self.new_name_listing_file = DEFAULT_NEW_NAME_LISTING_FILE
    for arg in sys.argv:
      if arg.startswith('-h') or arg.startswith('--help'):
        print(__dict__)
        sys.exit(0)
      elif arg.startswith('-e='):
        self.should_be_ext = arg[len('-e='):]
      elif arg.startswith('-n='):
        self.new_name_listing_file = arg[len('-n='):]
      elif arg.startswith('-w='):
        self.workdir_abspath = arg[len('-w='):]


class Renamer:

  def __init__(self, workdir_abspath=None, new_name_listing_file=None, should_be_ext=None):
    self.confirmed_renames = False
    self.workdir_abspath = workdir_abspath
    self.current_filenames = []
    self.new_filenames = []
    self.n_renames = 0
    # self.rename_pairs is a dynamic property that zips current_files with new_names "on-the-fly"
    self.new_name_listing_file = new_name_listing_file
    self.should_be_ext = should_be_ext
    self.treat_workdir_inputfilename_n_ext()

  def treat_workdir_inputfilename_n_ext(self):
    if self.new_name_listing_file is None:
      self.new_name_listing_file = DEFAULT_NEW_NAME_LISTING_FILE
    if self.should_be_ext is None:
      self.should_be_ext = DEFAULT_EXT
    if self.workdir_abspath is None:
      self.workdir_abspath = os.path.abspath('.')

  def pick_up_n_set_new_filenames(self):
    """
    Reads the new filenames from the given text file
    """
    self.new_filenames = []
    if not os.path.isfile(self.new_name_listing_file):
      scrmsg = f'{self.new_name_listing_file} does not exist. Please, inform it via argument -n="<file>".'
      print(scrmsg)
      sys.exit(1)
    names = open(self.new_name_listing_file).read().split('\n')
    seq = 0
    for name in names:
      if name == '' or name == '\n':
        continue
      seq += 1
      new_name = str(seq).zfill(2) + ' ' + name + '.' + self.should_be_ext.lower()
      if new_name.find('/') > -1:
        new_name = new_name.replace('/', '_')
      self.new_filenames.append(new_name)

  def pick_up_n_set_current_filenames(self):
    """
    Returns folder files with the executing extension
    """
    filenames = os.listdir(self.workdir_abspath)
    self.current_filenames = list(filter(lambda e: e.endswith(self.should_be_ext), filenames))
    self.current_filenames.sort()

  def get_srcfile_abspath(self, srcfilename):
    return os.path.join(self.workdir_abspath, srcfilename)

  def get_trgfile_abspath(self, trgfilename):
    return os.path.join(self.workdir_abspath, trgfilename)

  @property
  def rename_pairs(self):
    """
    Zips current_files with new_names "on-the-fly" returns a list of tuples representing the rename pairs

    Zip Explanation:
      Zip joins each element of one list to each element of another
    Example:
      list1 = [1, 2, 3]
      list2 = [11, 22, 33]
    list(zip(list1, list2)) results in:
      [(1, 11), (2, 22), (3, 33)]
    without function list() zip() returns an iterator-like object
    """
    n_curr_files = len(self.current_filenames)
    n_new_names = len(self.new_filenames)
    if n_curr_files != n_new_names:
      errmsg = (f"Error: number of files to/from should be the same, but isn't: "
                f"len(self.current_files={n_curr_files}) != len(self.new_names={n_new_names})")
      raise ValueError(errmsg)
    return list(zip(self.current_filenames, self.new_filenames))

  def pick_up_n_set_current_and_new_filenames(self):
    """
    Picks up (so to say) the two lists new_names and current_files
      for, in the sequence, calling function unite_elements_one_to_one(current_files, new_names)
    """
    self.pick_up_n_set_new_filenames()
    self.pick_up_n_set_current_filenames()

  def confirm_renames(self):
    self.confirmed_renames = False
    if len(self.rename_pairs) == 0:
      print('No renames')
      return False
    scrmsg = f"In directory: [{self.workdir_abspath}]"
    print(scrmsg)
    for i, tuple_to_rename in enumerate(self.rename_pairs):
      seq = i + 1
      current_name, new_name = tuple_to_rename
      scrmsg = f"""{seq} => rename pair:
        current_name=[{current_name}]
        new_name=[{new_name}]"""
      print(scrmsg)
    ans = input('Rename them above ? (y/N) [ENTER] means Yes ')
    if ans in ['y', 'Y', '']:
      self.confirmed_renames = True
    return self.confirmed_renames

  def rename(self):
    """
    Finally, it does the renaming
    """
    if len(self.rename_pairs) == 0 or not self.confirmed_renames:
      print('No files to rename')
      return False
    scrmsg = f"In directory: [{self.workdir_abspath}]"
    print(scrmsg)
    for i, tuple_to_rename in enumerate(self.rename_pairs):
      seq = i + 1
      srcfilename, trgfilename = tuple_to_rename
      srcfile_abspath = self.get_srcfile_abspath(srcfilename)
      trgfile_abspath = self.get_trgfile_abspath(trgfilename)
      if not os.path.isfile(srcfile_abspath):
        scrmsg = f"file {srcfile_abspath} does not exist. Continuing."
        print(scrmsg)
        continue
      if os.path.isfile(trgfile_abspath):
        scrmsg = f"file {srcfile_abspath} does exist, cannot rename pair. Continuing."
        print(scrmsg)
        continue
      os.rename(srcfile_abspath, trgfile_abspath)
      scrmsg = f"""{seq} => renamed pair:
        srcfile_abspath=[{srcfilename}]
        trgfile_abspath=[{trgfilename}]"""
      print(scrmsg)
      self.n_renames += 1
    scrmsg = f"{self.n_renames} files were renamed."
    print(scrmsg)
    return True

  def process(self):
    self.pick_up_n_set_current_and_new_filenames()
    self.confirm_renames()
    self.rename()


def process():
  """
  This is the main process() function:
    1) it finds out the two CLI parameters
    1) it gets the rename pairs
    3) it calls the rename() function with the rename pairs
  """
  print()
  args_obj = InputArguments()
  workdir_abspath = args_obj.workdir_abspath
  new_name_listing_file = args_obj.new_name_listing_file
  should_be_ext = args_obj.should_be_ext
  renamer = Renamer(workdir_abspath, new_name_listing_file, should_be_ext)
  renamer.process()


if __name__ == '__main__':
  process()
