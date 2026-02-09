#!/usr/bin/env python3
"""
~/bin/renameFolderInsertingString.py
  Inserts a string to the end of a foldername
    for all subfolders in the working directory.

Usage:
  $renameFolderInsertingString.py -i=<insert_word> [-p=<pos>] [-wd=<workdir>]
    where:
      -i: insert word
          | required, this is the 'word' to be inserted
      -p: the name's index position at which inserting will happen
          | optional, defaults to end of name
      -wd: the working directory path
          | optional, defaults to the current working directory

Example:
  $renameFolderInsertingString.py -i=" audio"
    This example will insert the string " audio" to the names
      of all folders in the working directory.
"""
import os
import sys


class Renamer:
  
  def __init__(self, insertword=None, workdir=None, pos=None):
    """
      Though the rename-process depends on addword not being None,
      it does accept it as None in which case no renames will be gathered.
    """
    self.folders_in_dir = []
    self.total_renamed = 0
    self.rename_pairs = []
    self.renaming_confirmed = False
    self.pos = pos  # if pos is None, insertword is concatenated to 'name'
    self.insertword = insertword if insertword is None else str(insertword)
    self.workdir = workdir  # to be treated ahead
    self.treat_workdir()
    self.process()

  def treat_workdir(self):
    if self.workdir is None or not os.path.isdir(self.workdir):
      self.workdir = os.getcwd()  # default to the current working dir

  def do_renames_if_confirmed(self):
    if not self.renaming_confirmed:
      scrmsg = f"Not confirmed or no renames. Returing."
      print(scrmsg)
      return
    print('-'*40)
    for i, rename_pair in enumerate(self.rename_pairs):
      old_name, new_name = rename_pair
      seq = i + 1
      print(seq, '/', self.total_renamed, 'Rename:')
      print('\tFROM: >>>%s' % old_name)
      print('\tTO:   >>>%s' % new_name)
      full_old_name = os.path.join(self.workdir, old_name)
      full_new_name = os.path.join(self.workdir, new_name)
      os.rename(full_old_name, full_new_name)
      self.total_renamed += 1

  def confirm_renames(self):
    self.renaming_confirmed = False
    for i, rename_pair in enumerate(self.rename_pairs):
      old_name, new_name = rename_pair
      seq = i + 1
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
    scrmsg = 'Confirm the %d renames above ? (y/N) [ENTER] means Yes ' % len(self.rename_pairs)
    ans = input(scrmsg)
    if ans in ['y', 'Y', '']:
      self.renaming_confirmed = True

  def form_pairs(self):
    for foldername in self.folders_in_dir:
      pos = None
      if self.pos is not None:
        if 0 < self.pos < len(foldername):
          pos = self.pos
        elif -len(foldername) < self.pos < 0:
          pos = len(foldername) + self.pos
        newname = foldername[: pos] + self.insertword + foldername[pos:]
      else:  # i.e. it's None
        newname = foldername + self.insertword
      rename_pair = (foldername, newname)
      self.rename_pairs.append(rename_pair)

  def search_renames(self):
    if self.insertword is None:
      scrmsg = f"As insertword is None, no renames can be gathered. Returning."
      print(scrmsg)
      return
    entries = os.listdir(self.workdir)
    for entry in entries:
      fullentry = os.path.join(self.workdir, entry)
      if os.path.isdir(fullentry):
        self.folders_in_dir.append(entry)

  def process(self):
    self.search_renames()
    self.form_pairs()
    self.confirm_renames()
    self.do_renames_if_confirmed()
    self.report()

  def report(self):
    print('-'*40)
    scrmsg = f"Finished {self.total_renamed} of {len(self.rename_pairs)} renames."
    print(scrmsg)


def get_args():
  insword, pos, workdir = None, None, None
  for arg in sys.argv[1:]:
    if arg in ['-h', '--help']:
      print(__doc__)
      sys.exit()
    elif arg.startswith('-i='):
      insword = arg[len('-i='):]
    elif arg.startswith('-p='):
      pos = arg[len('-p='):]
    elif arg.startswith('-wd='):
      workdir = arg[len('-wd='):]
  return insword, pos, workdir


def process():
  """
  """
  insword, pos, workdir = get_args()
  Renamer(insertword=insword, pos=pos, workdir=workdir)


if __name__ == '__main__':
  process()
