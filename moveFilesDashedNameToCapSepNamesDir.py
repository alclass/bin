#!/usr/bin/env python3
"""
moveFilesNameDashConvention

This script moves files into directories that bind to a certain specified convention.

This convention, not "openly general" at this time, is the following:

1) suppose a filename that has a name-dash-surname (or any word dash another),
   and this name-dash-surname exactly after a word and a space (gap),
   e.g.:
    "50' albert-einstein theory of relativity.ext"
   (notice that the pre-string "50' " is a word plus a space)

2) for this example above, this script will move it to the following directory:
  <base-dir>/A/AL

  ie,
  subdirectory "A" is because first name starts with A ([A]lbert)
  subdirectory "AL", inside "A", is because first name starts with AL ([Al]bert)
  resulting in path "<base-dir>/A/AL"
  where <base-dir> is the absolute directory acting as 'base dir path'

How <base-dir> is given
=======================

If <base-dir> is not given, the script will convention it to be "../..",
ie, the second directory above the executing directory
notice also that the files-to-move must be located in the running directory
(this parameter [source folder for the input files] is not available for the time being)


  1) <base-dir> default (when none is given at the command line):
    as said above, if none <base-dir> is given, it's "../..",
    ie the parent of the parent folder

  1) giving <base-dir> in the command line:
    parameter [-b "<base-dir>"] gives a determined chosen <base-dir>

  Where <base-dir> is the directory from where
    the "alphabet folders (A, B, C...)" are placed on.

Examples:
  $<script> -b /this/videodir

Suppose that in the executing directory one has file
    "50' albert-einstein theory of relativity.ext"

The script will move this file to:
    /this/videodir/"50' albert-einstein theory of relativity.ext"

"""
import glob
import os
import shutil
from pathlib import Path
default_dot_ext = '.mp4'


def treat_name_to_move(dashedname):
  """
  Transforms dashed-name to Capitalized first letter words
    E.g.
      input => "albert-einstein"
      output => "Albert Einstein"
  """
  newname = ''
  pp = dashedname.split('-')
  for current_word in pp:
    current_word = current_word[0].upper() + current_word[1:]
    newname += current_word + ' '
  newname = newname.rstrip(' ')
  print('treat_name_to_move =>', dashedname, '=>', newname)
  return newname


def get_childpath_based_on_secondleveldir_n_name(secondlevel_dirpath, cap_sep_name):
  targetentries = os.listdir(secondlevel_dirpath)
  for entry in targetentries:
    if entry.lower().startswith(cap_sep_name.lower()):
      childpath = os.path.join(secondlevel_dirpath, entry)
      if os.path.isdir(childpath):
        return childpath
  return None


class AlphabetFileMover:

  def __init__(self, given_base_dir=None, dot_ext=None):
    self.dot_ext = dot_ext
    self.treat_dot_ext()
    self.filenames = []
    self.move_pair_list = []
    self.basedir = None
    self.given_base_dir = given_base_dir
    self.executing_dir = None
    self.determine_basedir()
    self.process()

  def process(self):
    # 1) gather local dir source files
    self.gather_source_files_to_move_over()
    # 2) deduce target folder paths
    self.deduce_target_folderpaths()
    # 3) find among target folder paths those that do not exist
    self.verify_target_folders_existence()
    # 4) if any target folder paths does not exist, confirm ask it creation
    self.create_target_folders_if_needed()
    # 5) move source files to target folders
    self.move_source_files_to_target_folders()

  def gather_source_files_to_move_over(self):
    os.listdir(self.executing_dir)
    pass

  def deduce_target_folderpaths(self):
    pass

    # 3) find among target folder paths those that do not exist
  def verify_target_folders_existence(self):
    pass

  def create_target_folders_if_needed(self):
    pass

  def move_source_files_to_target_folders(self):


  def treat_dot_ext(self):
    if self.dot_ext is None:
      self.dot_ext = default_dot_ext
    if not self.dot_ext.startswith('.'):
      self.dot_ext = '.' + self.dot_ext

  def determine_basedir(self):
    if self.given_base_dir is None:
      self.position_to_default_basefolder()
    else:
      self.position_to_given_basefolder()
    print('basedir =', self.basedir)

  def position_to_default_basefolder(self):
    self.executing_dir = os.path.abspath('.')
    self.executing_dir = Path(self.executing_dir)
    self.filenames = glob.glob('*.mp4')
    sorted(filenames)
    self.basedir = self.executing_dir.parent.parent

  def gather_names_dir_pair_list(self):
    self.move_pair_list = []
    for filename in self.files:
      pp = filename.split(' ')
      firstsupposeddashedname = pp[1]
      cap_sep_name = treat_name_to_move(firstsupposeddashedname)
      move_pair = (filename, cap_sep_name)
      self.move_pair_list.append(move_pair)

  def find_second_level_dirpath_from_name(self, cap_sep_name):
    get_childpath_based_on_secondleveldir_n_name(secondlevel_dirpath, cap_sep_name)

def find_second_level_dirpath_from_name(self, cap_sep_name):
  if cap_sep_name is None:
    return None
  firstletter = cap_sep_name[0]
  firstdir = os.path.join(self.basedir, firstletter)
  if not os.path.isdir(firstdir):
    return None
  print('firstdir =>', firstdir)
  twoletters = cap_sep_name[0:2].upper()
  second_level_dirpath = os.path.join(firstdir, twoletters)
  if not os.path.isdir(second_level_dirpath):
    return None
  print('seconddir =>', second_level_dirpath)
  return second_level_dirpath


def move_pairs(move_pair_list):
  for i, move_pair in enumerate(move_pair_list):
    filename, cap_sep_name = move_pair
    targetentry = find_n_get_folder(cap_sep_name)
    seq = i + 1
    print(seq)
    print('FROM: ', filename)
    print('TO:   ', targetentry)
    if targetentry is not None:
      print('Moving...')
      shutil.move(filename, targetentry)
  

def process():
  move_pair_list = process_names()
  move_pairs(move_pair_list)


if __name__ == '__main__':
  process()
