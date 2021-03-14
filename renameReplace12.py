#!/usr/bin/env python3
"""
This script replaces a given string (s1) to another one (s2) in filenames of a certain extension.

Usage: <this_script> -e="<ext>" -s1="<string1>" -s2="<string2>"
Example: renameReplace12 -e="mp4" -s1="foo" -s2="bar"

In the example above, any file containing the string "foo" in its name will have it changed to string "bar".
Suppose there is a filename "foo bar.mp4". After the example above, its name will become "bar bar.mp4"
"""
import glob
import os
import sys


def fetch_files_on_folder(ext):
  files = glob.glob('*.' + ext)
  return files


class Renamer:

  def __init__(self, ext, piece1, piece2):
    self.rename_pairs = []
    self.ext = ext
    self.piece1 = piece1
    self.piece2 = piece2
    self.files = fetch_files_on_folder(self.ext)

  def prepare_rename(self):
    file_counter = 0
    for eachFile in self.files:
      if eachFile.find(self.piece1) > -1:
        newname = eachFile.replace(self.piece1, self.piece2)
        pair = (eachFile, newname)
        self.rename_pairs.append(pair)
        file_counter += 1
        print('Listing', file_counter, '===============')
        print('FROM:', eachFile)
        print('TO:  ', newname)

  def confirm_rename(self):
    n_to_rename = len(self.rename_pairs)
    if n_to_rename == 0:
      print('No files to rename.')
      return False
    confirm_question = 'Confirm the above %d renames? (*Y/n) ' % n_to_rename
    ans = input(confirm_question)
    if ans not in ['', 'Y', 'y']:
      print('Not renaming', n_to_rename, 'files,')
      return False
    print('To rename', n_to_rename, 'files => ')
    return True

  def do_rename(self):
    n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      oldname, newname = rename_pair
      if not os.path.isfile(oldname):
        print(seq, 'File [' + oldname + '] does not exist.')
        continue
      if os.path.isfile(newname):
        print(seq, 'File [' + newname + '] already exists.')
        continue
      print('Renaming', seq, '===============')
      print('FROM:', oldname)
      print('TO:  ', newname)
      os.rename(oldname, newname)
      n_renames += 1
    print('n_renames', n_renames)

  def process_rename(self):
    self.prepare_rename()
    if self.confirm_rename():
      self.do_rename()


def get_args():
  args = {'ext': None, 'piece1': '', 'piece2': ''}
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-e='):
      ext = arg[len('-e='):]
      args['ext'] = ext
    elif arg.startswith('-s1='):
      piece1 = arg[len('-s1='):]
      args['piece1'] = piece1
    elif arg.startswith('-s2='):
      piece2 = arg[len('-s2='):]
      args['piece2'] = piece2
  return args


def process():
  args = get_args()
  ext, piece1, piece2 = args['ext'], args['piece1'], args['piece2']
  ren = Renamer(ext, piece1, piece2)
  ren.process_rename()


if __name__ == '__main__':
  process()
