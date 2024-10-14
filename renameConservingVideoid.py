#!/usr/bin/env python3
"""
Usage:
$renameConservingVideoid.py [-e=<ext>] [-n=<newnames_input_filename>] [-dp=<'/home/user1/sci_videos'>]

Arguments:
  -e=<extension> => the file extension: examples: mp4 or webm
  -n=<newnames_input_filename> => a text file with has the new name for renaming
  -dp=<dir_path> => the path to the directory where renames should occur

Example:
  $renameConservingVideoid.py -dp='/home/user1/sci_videos'
In this example, two default values will take place:
  default extension will be 'mp4'
  default new names textfile is 'z-titles.txt'
"""
import os
import sys


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
  
  def __init__(self, extension=None, names_filename=None, absdirpath=None):
    self.dotextension = None
    self.names_filename = None
    self.absdirpath = None
    self.files = []
    self.filenames = []
    self.rename_pairs = []
    self.set_dotextension_or_default(extension)
    self.set_names_filename_or_default(names_filename)
    self.set_absdirpath_or_default(absdirpath)
    self.process()

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

  def get_filename_conventioned_ending_charsize(self):
    """
    The youtube filename this script aims at follows the following convention:
      name + '-' + a-11-char-enc64-string + '.ext'
    In the above case, integer 11 should be attributed to constant VIDEOID_CHARSIZE

    Obs: if a different convention is followed, this script will not work (or work partially).

    In the example:
      filename = "this-is-a-videotitle-abc1-2_3def.mp4"
      This function should return "this-is-a-videotitle"
    :return:
    """
    trailing_charsize = self.VIDEOID_CHARSIZE + len(self.dotextension) + 1
    return trailing_charsize
    
  def get_videoid_plus_ext_ending(self, old_filename):
    # example => 1 [ie the - (dash)]  + 11 (the 11-char ytvideoid) + 4 (.mp4 ie dotextension)]
    if len(old_filename) < self.get_filename_conventioned_ending_charsize():
      return None
    if not old_filename.endswith('%s' % self.dotextension):
      return None
    retro_pos = self.get_filename_conventioned_ending_charsize()
    if old_filename[-retro_pos] != '-':  # it's -16 with .mp4, ie, it's = 11 + 4 + 1
      return None
    return old_filename[-retro_pos:]  # this will be appended after the "new name" under renaming

  def confirm_rename_pairs(self):
    print('='*40)
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      old_file = rename_pair[0]
      new_file = rename_pair[1]
      old_filename = os.path.split(old_file)[1]
      new_filename = os.path.split(new_file)[1]
      print(seq, 'Rename:')
      print('FROM: >>>', old_filename)
      print('TO:   >>>', new_filename)
    print('='*40)
    print('In directory:', self.absdirpath)
    ans = input('Confirm the %d renames above (Y*/n)? [ENTER] means Yes' % len(self.rename_pairs))
    if ans in ['Y', 'y', '']:
      return True
    return False

  def do_rename(self):
    if not self.confirm_rename_pairs():
      print('No files were renamed.')
      return
    for i, rename_pair in enumerate(self.rename_pairs):
      old_file = rename_pair[0]
      new_file = rename_pair[1]
      old_filename = os.path.split(old_file)[1]
      new_filename = os.path.split(new_file)[1]
      print(i+1, 'Renaming', old_filename, 'TO', new_filename)
      os.rename(old_file, new_file)
    print('%d files were renamed.' % len(self.rename_pairs))

  def get_names_from_input_textfile_n_generate_renamepairs(self):
    lines = open(self.names_filename).readlines()
    for i, new_title in enumerate(lines):
      new_title = new_title.lstrip(' \t').rstrip(' \t\r\n')
      if new_title == '':
        continue
      try:  # IndexError may happen here
        old_name = self.filenames[i]
      except IndexError:
        continue
      ending = self.get_videoid_plus_ext_ending(old_name)
      if ending is None:
        continue
      new_name = new_title + ending
      if new_name == old_name:
        continue
      abspathfile = self.files[i]
      new_abspathfile = os.path.join(self.absdirpath, new_name)
      if abspathfile == new_abspathfile:
        continue
      rename_pair = (abspathfile, new_abspathfile)
      self.rename_pairs.append(rename_pair)

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
    self.do_rename()


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
  return extension, names_filename, dpath


def process():
  extension, names_filename, dpath = get_args()
  print('-e=%s' % extension, '-n=%s' % names_filename, '-dp=%s' % dpath)
  print('-e=%s' % extension, '-n=%s' % names_filename, '-dp=%s' % dpath)
  Renamer(extension, names_filename, dpath)


if __name__ == '__main__':
  process()
