#!/usr/bin/env python3
"""
Explanation

This script renames files with a certain extension (default value below) in alphabetical order
  with the names in a text file (whose default filename is given below)

Limitation Obs:
  This script has not yet been refactored for running with absolute paths,
    so for now it only works running it from the local directory affecting the same folder
  (This script was probably written before 2010 in Python 2
     and finally in 2025 it was ported to Python 3)

Usage:
  $renameWithNewNameListingFileAndExt.py [-e=<fileextension>] [-n="<textfilename>"]

Where:
  fileextension => the desired file extension for the files to be renamed (eg '.txt')
  textfilename => the filename that contains the new names for the files to be renamed

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

"""
import glob
import os
import shutil
import sys
import time
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


def pick_up_new_names(new_name_listing_file=None, should_be_ext=None):
  """
  Reads the new filenames from the given text file

  :param new_name_listing_file: new filenames data filename
  :param should_be_ext: extension that groups the files to be renamed
  :return:
  """
  if new_name_listing_file is None:
    new_name_listing_file = DEFAULT_NEW_NAME_LISTING_FILE
  if should_be_ext is None:
    should_be_ext = DEFAULT_EXT
  new_names = []
  if not os.path.isfile(new_name_listing_file):
    scrmsg = f'{new_name_listing_file} does not exist. Please, inform it via argument -n="<file>".'
    print(scrmsg)
    sys.exit(1)
  names = open(new_name_listing_file).read().split('\n')
  seq = 0
  for name in names:
    if name == '' or name == '\n':
      continue
    seq += 1
    new_name = str(seq).zfill(2) + ' ' + name + '.' + should_be_ext.lower()
    if new_name.find('/') > -1:
      new_name = new_name.replace('/', '_')
    new_names.append(new_name)
  return new_names


def pick_up_current_names(should_be_ext=DEFAULT_EXT):
  """
  Returns folder files with the executing extension

  :param should_be_ext:
  :return:
  """
  current_files = glob.glob('*.' + should_be_ext)
  current_files.sort()
  return current_files


def unite_elements_one_to_one(current_files, new_names):
  """
  Maps files with their new filenames

  :param current_files: list of current filenames
  :param new_names: list of new filenames
  :return:
  """
  tuples_to_rename = []
  for i in range(len(current_files)):
    if i >= len(new_names):
      # raise IndexError, 'current_files and new_names do not have the same size.'
      # instead of raising an Exception as commented above, return tuplesToRename, "cutting" off currentFiles at i
      # this is then the Use Case here, ie, unite_elements_one_to_one until either one set finishes
      return tuples_to_rename
    current_name = current_files[i]
    new_name = new_names[i]
    tuple_to_rename = current_name, new_name
    tuples_to_rename.append(tuple_to_rename)
  return tuples_to_rename


def pick_up_current_and_new_names(new_name_listing_file, should_be_ext):
  """
  Picks up (so to say) the two lists new_names and current_files
    for, in the sequence, calling function unite_elements_one_to_one(current_files, new_names)

  :param new_name_listing_file:
  :param should_be_ext:
  :return:
  """
  new_names = pick_up_new_names(new_name_listing_file, should_be_ext)
  current_files = pick_up_current_names(should_be_ext)
  return unite_elements_one_to_one(current_files, new_names)


def rename(tuples_to_rename, do_rename=False):
  """
  This function, in the first pass, lists the renaming pairs and ask the user a confirmation;
    if the user confirms it, in the second pass it renames the queued pairs
  """
  seq = 0
  for tuple_to_rename in tuples_to_rename:
    current_name, new_name = tuple_to_rename
    seq += 1
    if do_rename:
      os.rename(current_name, new_name)
    else:
      print(seq, 'Rename:')
      print('\t', current_name)
      print('\t', new_name)
  if len(tuples_to_rename) > 0:
    if do_rename:
      print(seq, 'files were renamed.')
      return
    else:
      ans = input('Rename them above ? (y/N) [ENTER] means Yes ')
      if ans in ['y', 'Y', '']:
        rename(tuples_to_rename, True)
  else:
    print('No files to rename.')


def process():
  """
  This is the main process() function:
    1) it finds out the two CLI parameters
    1) it gets the rename pairs
    3) it calls the rename() function with the rename pairs
  """
  args_obj = InputArguments()
  tuples_to_rename = pick_up_current_and_new_names(args_obj.new_name_listing_file, args_obj.should_be_ext)
  rename(tuples_to_rename)
     

if __name__ == '__main__':
  process()
