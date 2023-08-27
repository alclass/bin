#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
renameBasedOnInputTextfile
  This script is based on renameConservingVideoid.py
  The difference is that this one is simpler and does not take into account a ytvideoid conventioned

Usage:
$renameBasedOnInputTextfile.py [-e=<ext>] [-dp=<'/home/user1/sci_videos'>]
    [-n=<newnames_input_filename>] [-nf]

Arguments:
  -e=<extension> => the file extension: examples: mp4 or webm
  -dp=<dir_path> => the path to the directory where renames should occur
  -n=<newnames_input_filename> => a text file with has the new name for renaming
  -nf => if present it means a sequential numbering (1, 2, 3...) should prefix names

Example:
  $renameConservingVideoid.py -dp='/home/user1/sci_videos'
In this example, two default values will take place:
  default extension will be 'mp4'
  default new names textfile is 'z-titles.txt'
"""
import os
import sys
import math


def check_n_clean_or_none_as_extension_startswithadot(dotextension):
  try:
    dotextension = str(dotextension)
    extension_after_dot = dotextension.split('.')[-1]
    dotextension = '.' + extension_after_dot
    return dotextension
  except IndexError:
    return None


class Renamer(object):
  DEFAULT_DOTEXTENSION = '.mp4'
  DEFAULT_NAMES_FILENAME = 'z-titles.txt'
  VIDEOID_CHARSIZE = 11
  
  def __init__(self, extension=None, names_filename=None, absdirpath=None, numberthem=True):
    self.dotextension = None
    self.names_filename = None
    self.absdirpath = None
    self.numberthem = numberthem
    self.files = []
    self.filenames = []
    self.rename_pairs = []
    self.set_dotextension_or_default(extension)
    self.set_names_filename_or_default(names_filename)
    self.set_absdirpath_or_default(absdirpath)
    self.process()

  @property
  def leftzeroes_zfillsize(self):
    return int(math.log(len(self.files), 10)) + 1

  def set_names_filename_or_default(self, names_filename=None):
    if names_filename is None:
      self.names_filename = self.DEFAULT_NAMES_FILENAME
      return
    try:
      names_filename = str(names_filename)
      self.names_filename = names_filename
    except ValueError:
      self.names_filename = self.DEFAULT_NAMES_FILENAME

  def set_dotextension_or_default(self, dotextension=None):
    if dotextension is None:
      self.dotextension = self.DEFAULT_DOTEXTENSION
      return
    dotextension = check_n_clean_or_none_as_extension_startswithadot(dotextension)
    if dotextension is None:
      self.dotextension = self.DEFAULT_DOTEXTENSION
    else:
      self.dotextension = dotextension

  def set_absdirpath_or_default(self, absdirpath=None):
    self.absdirpath = None
    if absdirpath is None or not os.path.isdir(absdirpath):
      self.absdirpath = os.path.abspath('.')
    else:
      self.absdirpath = os.path.abspath(absdirpath)

  def get_charsize_to_strip_dotextension(self):
    """
    :return:
    """
    trailing_charsize = len(self.dotextension)
    return trailing_charsize

  def do_rename(self):
    if len(self.rename_pairs) == 0:
      return
    for i, rename_pair in enumerate(self.rename_pairs):
      old_file = rename_pair[0]
      new_file = rename_pair[1]
      old_filename = os.path.split(old_file)[1]
      new_filename = os.path.split(old_file)[1]
      seq = i + 1
      print(seq, 'Rename:')
      print('FROM: >>>', old_filename)
      print('TO:   >>>', new_filename)
      os.rename(old_file, new_file)
    print('%d files were renamed.' % len(self.rename_pairs))
    print('In directory:', self.absdirpath)

  def confirm_rename_pairs(self):
    print('='*40)
    for i, rename_pair in enumerate(self.rename_pairs):
      old_file = rename_pair[0]
      new_file = rename_pair[1]
      old_filename = os.path.split(old_file)[1]
      new_filename = os.path.split(new_file)[1]
      seq = i + 1
      print(seq, 'Rename:')
      print('FROM: >>>', old_filename)
      print('TO:   >>>', new_filename)
    print('=' * 40)
    print('In directory:', self.absdirpath)
    ans = input('Confirm the %d renames above (Y*/n)? [Y, y or empty-ENTER] means Yes : ' % len(self.rename_pairs))
    if ans in ['Y', 'y', '']:
      return True
    return False

  def get_names_from_input_textfile_n_generate_renamepairs(self):
    indexseq_old_names = 0
    lines = open(self.names_filename).readlines()
    for indexseq_new_names, new_title in enumerate(lines):
      new_title = new_title.lstrip(' \t').rstrip(' \t\r\n')
      if new_title == '':
        continue
      new_filename = new_title + self.dotextension
      if self.numberthem:
        seq_str = str(indexseq_new_names+1).zfill(self.leftzeroes_zfillsize)
        new_filename = seq_str + ' ' + new_filename
      if indexseq_old_names > len(self.files) - 1:
        return
      abspathfile = self.files[indexseq_old_names]
      old_filename = os.path.split(abspathfile)[1]
      print('checking', old_filename, '||', new_filename, '||', old_filename==new_filename)
      if old_filename == new_filename:
        indexseq_old_names += 1
        continue
      new_abspathfile = os.path.join(self.absdirpath, new_filename)
      rename_pair = (abspathfile, new_abspathfile)
      self.rename_pairs.append(rename_pair)
      indexseq_old_names += 1

  def enlist_files_on_current_folder(self):
    """
    Picks up the files in absdirpath that ends with the class given extension
    The result is stored in instance variable 'files'
    :return:
    """
    entries = os.listdir(self.absdirpath)
    entries = filter(lambda e: e.endswith(self.dotextension), entries)
    fullentries = filter(lambda f: os.path.join(self.absdirpath, f), entries)
    self.files = list(filter(lambda f: os.path.isfile(f), fullentries))
    self.files.sort()
    self.filenames = [os.path.split(abspathfile)[1] for abspathfile in self.files]

  def process(self):
    self.enlist_files_on_current_folder()
    self.get_names_from_input_textfile_n_generate_renamepairs()
    if len(self.rename_pairs) > 0 and self.confirm_rename_pairs():
      self.do_rename()
    else:
      print('No files were renamed.')


def show_help():
  txt = '''
  This script
  1) takes files with a certain extension (defaulted to mp4, use parameter [-e=ext])
  2) sorts them alphabetically
  3) reads the new titles in file [[ z-rename.txt ]]
  4) forms the new filenames using the new titles conserving the videoid plus the extension
  5) ask for renaming confirmation
  6) if confirmed (ie, if n or N is not pressed), rename will occur.
  '''
  print(txt)


def get_args():
  extension = None
  names_filename = None
  dpath = None
  numberthem = False
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[len('-e='):]
    elif arg.startswith('--help') or arg.startswith('-h'):
      show_help()
      sys.exit(0)
    elif arg.startswith('-n='):
      names_filename = arg[len('-n='):]
    elif arg.startswith('-dp='):
      dpath = arg[len('-dp='):]
    elif arg.startswith('-nf'):
      numberthem = True
  return extension, names_filename, dpath, numberthem


def process():
  extension, names_filename, dpath, numberthem = get_args()
  Renamer(extension, names_filename, dpath, numberthem)


if __name__ == '__main__':
  process()
