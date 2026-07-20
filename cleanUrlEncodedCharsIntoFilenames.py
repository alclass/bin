#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

SPACE_ENC = '%20'

def run_current_folder(do_rename= False):
  """
  runCurrentFolder(doRename=False)
  """
  files = os.listdir('.')
  for eachFile in files:
    if eachFile.find(SPACE_ENC) > -1:
      new_filename = eachFile.replace(SPACE_ENC, ' ')
      print('[to rename]', eachFile, new_filename,)
      if do_rename:
        os.rename(eachFile, new_filename)
        if os.path.isfile(new_filename):
          print('[renamed]')
      else: # ie, not renaming, just line feeding former print ending with comma
        print()


def process_rename():
  """
  confirm_renames()
  """
  run_current_folder(do_rename=False)
  print(' *** QUESTION *** ')
  print('Rename files above ? (s (or y) / n)')
  ans = input(' s/n ')
  if ans in ['y', 'Y', 's', 'S']:
    run_current_folder(do_rename=True)


if __name__ == '__main__':
  process_rename()
