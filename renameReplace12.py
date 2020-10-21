#!/usr/bin/env python3
import glob
import os
import sys


def fetchFilesOnFolder(ext):
  files = glob.glob('*.' + ext)
  return files


class Renamer:

  def __init__(self, ext, piece1, piece2):
    self.rename_pairs = []
    self.ext = ext
    self.piece1 = piece1
    self.piece2 = piece2
    self.files = fetchFilesOnFolder(self.ext)

  def prepare_rename(self):
    file_counter = 0
    for eachFile in self.files:
      if eachFile.find(self.piece1) > -1:
        newname = eachFile.replace(self.piece1, self.piece2)
        pair = (eachFile, newname)
        self.rename_pairs.append(pair)
        file_counter += 1
        print('Listing', file_counter, '===============')
        print ('FROM:', eachFile)
        print ('TO:  ', newname)

  def do_rename(self):
    n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      oldname, newname = rename_pair 
      print('Renaming', i+1, '===============')
      print ('FROM:', oldname)
      print ('TO:  ', newname)
      os.rename(oldname, newname)
      n_renames += 1
    print('n_renames', n_renames)

  def process_rename(self):
    self.prepare_rename()
    n_to_rename = len(self.rename_pairs)
    if n_to_rename == 0:
      print('No files to rename.')
      return
    confirm_question = 'Confirm the above %d renames? (Y/n) ' %n_to_rename
    ans = input(confirm_question)
    if ans not in ['', 'Y', 'y']:
      print('Not renaming', n_to_rename, 'files,')
      return
    print('To rename', n_to_rename, 'files => ')
    self.do_rename()


def get_args():
  args = {'ext':None, 'piece1':'', 'piece2':''}
  for arg in sys.argv:
    if arg.startswith('-e='):
      ext = arg[len('-e=') : ] 
      args['ext'] = ext
    elif arg.startswith('-s1='):
      piece1 = arg[len('-s1=') : ] 
      args['piece1'] = piece1
    elif arg.startswith('-s2='):
      piece2 = arg[len('-s2=') : ] 
      args['piece2'] = piece2
  return args


def process():
  args = get_args()
  ext, piece1, piece2 = args['ext'], args['piece1'], args['piece2']
  ren = Renamer(ext, piece1, piece2)
  ren.process_rename()


if __name__ == '__main__':
  process()
