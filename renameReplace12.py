#!/usr/bin/env python3
"""
This script replaces a given string (s1) to another one (s2) in filenames of a certain extension.

Usage: <this_script> -e="<ext>" -s1="<string1>" -s2="<string2>" [-y] [-dw]

Parameters:
  -e="<ext>" :: example: mp4, webm etc
  -s1="<string1>" :: example: "file"
   -s2="<string2>" :: example: "ficheiro" (ie substitute word ficheiro for the ocorrências of word file)
  -y :: noconfirm ie include -y to command for the Y/n confirmation (it will rename without the confirmation step)
  -dw :: dodirwalk ie include -dw for renaning "up dir tree"
         ie the script will apply the rename command to subdirectories

Examples:
  1) $renameReplace12 -e="mp4" -s1="foo" -s2="bar"
In the example above, any file containing the string "foo" in its name will have it changed to string "bar".
Suppose there is a filename "foo bar.mp4". After the example above, its name will become "bar bar.mp4"

  2) $renameReplace12 -e="mp4" -s1="foo" -s2="bar" -y
Same thing as above without the confirmation step.

  3) $renameReplace12 -e="mp4" -s1="foo" -s2="bar" -y -dw
Same thing as above also renaming files inside subdirectories.
"""
import glob
import os
import sys


def fetch_files_on_folder(ext):
  files = glob.glob('*.' + ext)
  return files


class Renamer:

  def __init__(self, ext, piece1, piece2, noconfirm=False):
    self.rename_pairs = []
    self.ext = ext
    self.piece1 = piece1
    self.piece2 = piece2
    self.noconfirm = noconfirm
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
    if self.noconfirm:
      self.do_rename()
    elif self.confirm_rename():
      self.do_rename()
    else:
      print('No files renamed.')


def get_args():
  args = {'ext': None, 'piece1': '', 'piece2': '', 'noconfirm': False, 'dodirwalk': False}
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
    elif arg.startswith('-y'):
      args['noconfirm'] = True
    elif arg.startswith('-dw'):
      args['dodirwalk'] = True
  return args


def issue_renamer_on_current_folder(ext, piece1, piece2, noconfirm):
  ren = Renamer(ext, piece1, piece2, noconfirm)
  ren.process_rename()


def process_dir_walk(ext, piece1, piece2, noconfirm):
  base_absdir = os.path.abspath('.')
  n_dirwalks = 0
  for current_folder, dirs, files in os.walk(base_absdir):
    n_dirwalks += 1
    print(n_dirwalks, 'Current folder:', current_folder)
    current_dirpath = os.path.join(base_absdir, current_folder)
    os.chdir(current_dirpath)
    issue_renamer_on_current_folder(ext, piece1, piece2, noconfirm)
  print('n_dirwalks =', n_dirwalks)


def adhoc_test():
  base_absdir = os.path.abspath('.')
  n_dirwalks = 0
  for current_folder, dirs, files in os.walk(base_absdir):
    n_dirwalks += 1
    print(n_dirwalks, 'Current folder:', current_folder)
    current_dirpath = os.path.join(base_absdir, current_folder)
    os.chdir(current_dirpath)
  print('n_dirwalks =', n_dirwalks)


def process():
  args = get_args()
  ext, piece1, piece2, noconfirm, dodirwalk = \
      args['ext'], args['piece1'], args['piece2'], args['noconfirm'], args['dodirwalk']
  if dodirwalk:
    process_dir_walk(ext, piece1, piece2, noconfirm)
  else:
    issue_renamer_on_current_folder(ext, piece1, piece2, noconfirm)


if __name__ == '__main__':
  # adhoc_test()
  process()
