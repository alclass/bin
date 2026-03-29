#!/usr/bin/env python3
"""
~/bin/listNamesBeforeYearWhenEqualsInFolderThuDirTree.py
  Reports repeated foldername conventioned names (*) in a folder

(*) the name convention here is the follow:
  => one or more names (words without numbers)
     followed by a 4-digit year number or the string 'yyyy'

"""
import datetime
import os
import re
import sys
from pathlib import Path
yyyy = ' yyyy '
restr = r"^.+?(\d{4}).+$"
recmp = re.compile(restr)


class EqualNamesDirWalker:

  def __init__(self, rootdir_abspath=None):
    self.rootdir_abspath = rootdir_abspath or os.path.abspath('.')
    self.rootdir_abspath = Path(self.rootdir_abspath)
    self.curdir_abspath = None
    self.namechunks = []
    self.n_found_all_dirs = 0

  def find_equals(self):
    pdict = {}
    n_found = 0
    for namechunk in self.namechunks:
      if namechunk in pdict:
        pdict[namechunk] += 1
      else:
        pdict[namechunk] = 1
    for namechunk in pdict:
      if pdict[namechunk] > 1:
        print('-'*40)
        print('FOUND', namechunk, 'occurs', pdict[namechunk])
        # print('-'*40)
        n_found += 1
      else:
        # print(namechunk, 'occurs', pdict[namechunk])
        pass
    # print('repeats n_found', n_found)
    self.n_found_all_dirs += n_found


  def mount_namechunks_per_dir(self, foldernames):
    self.namechunks = []
    for foldername in foldernames:
      namechunk = None
      pos = foldername.find(yyyy)
      if pos > -1:
        namechunk = foldername[ : pos]
        namechunk = namechunk.strip()
        self.namechunks.append(namechunk)
        continue
      match_o = recmp.match(foldername)
      if match_o:
        year = match_o.group(1)
        pos = foldername.find(str(year))
        namechunk = foldername[ : pos ]
        namechunk = namechunk.strip()
        # print('match', match_o, 'namechunk', namechunk)
        self.namechunks.append(namechunk)

  def process(self):
    for self.curdir_abspath, foldernames, _ in os.walk(self.rootdir_abspath):
      # print('In dir', self.curdir_abspath)
      self.mount_namechunks_per_dir(foldernames)
      self.find_equals()
    print('number of conventioned-name repeats found (all walked dirs) =', self.n_found_all_dirs)

def get_args():
  basefolderpath = None
  if len(sys.argv) > 1:
    basefolderpath = sys.argv[1]
  return basefolderpath


def process():
  basefolderpath = get_args()
  finder = EqualNamesDirWalker(rootdir_abspath=basefolderpath)
  finder.process()


if __name__ == '__main__':
  process()

