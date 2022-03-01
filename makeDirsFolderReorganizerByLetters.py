#!/usr/bin/env python3
"""
Obs 2022-02-18 this script has a bug that "strangely" does not complete the move of some folders
   (files are left on the parent dir). TO-DO: devise a test context to find this bug.

makeDirsFolderReorganizerByLetters.py

This script sweeps the A to Z letter-folders and creates AA, AB, AC etc folder as necessary.
Example:
    Suppose these is a directory tree such as

A (folder) with subfolders:
    "Air Nouveau" | "Air Supply" | "ABC method"

M (folder) with subfolders:
    "Mère de Tous" "Maths for All" "Meilleur de Mondes"

This script will create dirs AB, AD, MA, ME and MY and move the subfolders
  into the new letter-folders according to their initials, ie:
    "ABC method" -> AB
    "Air Nouveau" -> AI
    "Air Supply" -> AI
    "Maths for All" -> MA
    "Meilleur de Mondes" -> ME
    "Mère de Tous" -> ME
Notice: "Mére" has the accute accent è but the 2-letter folder is ME (with the accent).
"""
import glob
import os
import shutil
import string
import sys   # shutil, sys


ALPHABET_CAPITAL_LETTERS = string.ascii_uppercase


class FolderSweeperMakerFileMover:

  def __init__(self, basedir_abspath):
    self.basedir_abspath = basedir_abspath
    self.tomove_triples_list = []
    self.cap_letters_processed = []
    self.cap_letters_inexisting = []
    self.n_dirs_moved = 0
    self.n_folder_not_apply = 0
    self.n_not_moved_by_existing = 0
    self.n_not_moved_by_error = 0

  def move_folders_after_confirm(self):
    total_to_move = len(self.tomove_triples_list)
    for i, triple in enumerate(self.tomove_triples_list):
      foldername_to_move, folderpath_to_move, target_second_level_abspath = triple
      print(i + 1, '='*50)
      print('FROM: ', foldername_to_move, folderpath_to_move)
      print('TO:   ', target_second_level_abspath)
      try:
        shutil.move(folderpath_to_move, target_second_level_abspath)
        self.n_dirs_moved += 1
        print('Moved', self.n_dirs_moved, '/', total_to_move)
      except (IOError, OSError):
        self.n_not_moved_by_error += 1
        print('Error in folder move', self.n_not_moved_by_error, '/', total_to_move)

  def confirm_moves(self):
    total_to_move = len(self.tomove_triples_list)
    if total_to_move == 0:
      print('-+-' * 10)
      print('No folders to move.')
      print('-+-' * 10)
      return False
    screen_msg = 'Are you sure to move the %d folders above? (*Y/n) [ENTER] means Yes!' % len(self.tomove_triples_list)
    ans = input(screen_msg)
    if ans in ['Y','y','']:
      return True
    return False

  def show_movables(self):
    for i, triple in enumerate(self.tomove_triples_list):
      foldername_to_move, folderpath_to_move, target_second_level_abspath = triple
      print(i + 1, '='*50)
      print('FROM: ', foldername_to_move, folderpath_to_move)
      print('TO:   ', target_second_level_abspath)

  def append_move_file_to_second_level(self, foldername_to_move, folderpath_to_move, target_second_level_abspath):
    triple_fn_fp_n_target_2ndleveldirpath = foldername_to_move, folderpath_to_move, target_second_level_abspath
    projected_moved_folder = os.path.join(target_second_level_abspath, foldername_to_move)
    if os.path.exists(projected_moved_folder):
      self.n_not_moved_by_existing += 1
      return False
    self.tomove_triples_list.append(triple_fn_fp_n_target_2ndleveldirpath)
    return True

  def treat_files_abspath_for_move(self, folder_abspaths):
    for folderpath_to_move in folder_abspaths:
      basedir, foldername_to_move = os.path.split(folderpath_to_move)
      try:
        if len(foldername_to_move) < 3:
          self.n_folder_not_apply += 1
          continue
        second_level_2letter_dirname = foldername_to_move[:2]
        second_level_2letter_dirname = second_level_2letter_dirname.upper()
        second_level_abspath = os.path.join(basedir, second_level_2letter_dirname)
        _ = self.append_move_file_to_second_level(foldername_to_move, folderpath_to_move, second_level_abspath)
      except (AttributeError, IndexError):
          continue

  def treat_first_level_dir(self, cap_letter):
    first_level_dir = self.get_first_level_dir_abspath_with(cap_letter)
    entrynames = os.listdir(first_level_dir)
    entrypaths = map(lambda fn: os.path.join(first_level_dir, fn), entrynames)
    folder_abspaths = filter(lambda fp: os.path.isdir(fp), entrypaths)
    self.treat_files_abspath_for_move(folder_abspaths)

  def get_first_level_dir_abspath_with(self, cap_letter):
    return os.path.join(self.basedir_abspath, cap_letter)

  def sweep_first_level_dirs(self):
    for cap_letter in ALPHABET_CAPITAL_LETTERS:
      print('Sweeping letter', cap_letter,)
      if os.path.isdir(self.get_first_level_dir_abspath_with(cap_letter)):
        self.cap_letters_processed.append(cap_letter)
        # print('letter does exist as second level folder')
        self.treat_first_level_dir(cap_letter)
      else:
        self.cap_letters_inexisting.append(cap_letter)
        # print('letter', cap_letter, 'does not exist as second level folder')
        pass

  def process(self):
    self.sweep_first_level_dirs()
    self.show_movables()
    if self.confirm_moves():
      self.move_folders_after_confirm()
    self.report()

  def report(self):
    print('FolderSweeperMakerFileMover')
    print('n_dirs_moved', self.n_dirs_moved)
    print('n_folder_not_apply', self.n_folder_not_apply)
    print('n_not_moved_by_existing', self.n_not_moved_by_existing)
    print('n_not_moved_by_error', self.n_not_moved_by_error)
    print('cap_letters_processed', self.cap_letters_processed)
    print('cap_letters_inexisting', self.cap_letters_inexisting)
    print('quant letters processed', len(self.cap_letters_processed))
    print('quant tomove_triples_list', len(self.tomove_triples_list))


def process(folderpath):
  mover = FolderSweeperMakerFileMover(folderpath)
  mover.process()


def get_folderpath_arg():
  p_folderpath = os.path.abspath('.')
  try:
    arg = sys.argv[1]
    if os.path.isfile(arg):
      p_folderpath = arg
  except IndexError:
    pass
  return p_folderpath


if __name__ == '__main__':
  folderpath = get_folderpath_arg()
  process(folderpath)
