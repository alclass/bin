#!/usr/bin/env python3
"""
moveFilesNameDashConvention

For the time being it works only with a parent-parent basedir from the executing folder.
A CLI parameter defining basedir solves this limitation.
Or both approaches, ie, parent-parent the default and basedir-at-CLI the non-default.
---------------------

The default (for the time being):
running dir should be y-triage that is in:
<mount-dir>/0a0 

"""
import glob
import os
import shutil
from pathlib import Path
files = glob.glob('*.mp4')
sorted(files)
thisdir = os.path.abspath('.')
thisdir = Path(thisdir)
basedir = thisdir.parent.parent


def treat_name_to_move(dashedname):
  """
  Transforms dashed-name to Capitalized first letter words
  """
  newname = ''
  pp = dashedname.split('-')
  for word in pp:
    word = word[0].upper() + word[1:]
    newname += word + ' '
  newname = newname.rstrip(' ')
  print('treat_name_to_move =>', dashedname, '=>', newname)
  return newname


def process_names():
  move_pair_list = []
  for filename in files:
    pp = filename.split(' ')
    firstsupposeddashedname = pp[1]
    capSepName = treat_name_to_move(firstsupposeddashedname)
    move_pair = (filename, capSepName)
    move_pair_list.append(move_pair)
  return move_pair_list


def find_n_get_folder(capSepName):
  if capSepName is None: 
    return None
  firstletter = capSepName[0]
  firstdir = os.path.join(basedir, firstletter)
  if not os.path.isdir(firstdir):
    return None
  print('firstdir =>', firstdir)
  twoletters = capSepName[0:2].upper()
  seconddir = os.path.join(firstdir, twoletters)
  if not os.path.isdir(seconddir):
    return None
  print('seconddir =>', seconddir)
  targetentries = os.listdir(seconddir)
  for entry in targetentries:
    if entry.lower().startswith(capSepName.lower()):
      entrysabspath = os.path.join(seconddir, entry)
      if os.path.isdir(entrysabspath):
        return entrysabspath
  return None

def move_pairs(move_pair_list):
  for i, move_pair in enumerate(move_pair_list):
    filename, capSepName = move_pair
    targetentry = find_n_get_folder(capSepName)
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
  print('basedir =', basedir)
