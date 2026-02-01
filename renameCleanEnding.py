#!/usr/bin/env python3
"""
renameCleanEnding.py

On 2025-03-20 updated script with the following main features or corrections:
  1) added a get_args() function (TO-DO: improve it to the getopts library)
  2) included a function to adjust the index position when negative (relative to name size before extension)
     2.1) the function-method gets the new name for renaming and treats the index position
  3) improved some screen outputs (prints)
"""
import glob
import os
import sys


class Renamer:

  DEFAULT_DOT_EXT = '.mp4'

  def __init__(self, p_pos_from=None, p_dot_ext=None):
    """
    This class' constructor needs the cout-out index and the file extension
      to which files the operation will apply
    """
    self.pos_from = p_pos_from
    self.dot_ext = None
    self.set_dot_ext(p_dot_ext)
    self.rename_tuple_list = []
    self.was_renamed_tuple_list = []

  def derive_new_filename_based_on_pos(self, previous_filename):
    """
    This atttribute is necessary because pos may be negative
    :return:
    """
    name, dot_ext = os.path.splitext(previous_filename)
    if self.pos_from > -1:
      localpos = self.pos_from
    else:
      name_len = len(name)
      localpos = name_len + self.pos_from  # notice pos_from is negative here
    if localpos >= len(name):
      return None
    new_filename = name[:localpos] + dot_ext
    new_filename = new_filename.rstrip('.')
    return new_filename

  def set_dot_ext(self, p_dot_ext):
    if p_dot_ext is None or len(p_dot_ext) == 0:
      self.dot_ext = self.DEFAULT_DOT_EXT
    else:
      self.dot_ext = p_dot_ext
    if not self.dot_ext.startswith('.'):
      self.dot_ext = '.' + self.dot_ext

  def gather_renamepairs_ifany(self):
    """
    :return:
    """
    print('@gather_renamepairs_ifany')
    param_for_listdir = '*' + self.dot_ext
    try:
      print('@ dir', os.path.curdir)
      local_folder_files = glob.glob(param_for_listdir)
      i_scrmsg = 'Collecting %d files for renaming' % len(local_folder_files)
      print(i_scrmsg)
    except FileNotFoundError:
      print('no files with extension', param_for_listdir)
      return
    sorted(local_folder_files)
    for filename_from in local_folder_files:
      filename_to = self.derive_new_filename_based_on_pos(filename_from)
      if filename_to is None:
        continue
      rename_tuple = (filename_from, filename_to)
      # add pair to object's pair list
      self.rename_tuple_list.append(rename_tuple)

  def confirm_renames(self):
    """
    :return:
    """
    if len(self.rename_tuple_list) == 0:
      print('No files found for renaming.')
      return
    for i, rename_tuple in enumerate(self.rename_tuple_list):
      seq = i + 1
      filename_from, filename_to = rename_tuple
      print(seq)
      print('From: ', filename_from)
      print('To:   ', filename_to)
    i_scrmsg = ('Confirm %d renames above ? (y/N) [ENTER] means Yes, a non-Y/y means No ' %
                len(self.rename_tuple_list))
    ans = input(i_scrmsg)
    if ans in ['y', 'Y', '']:
      return True
    return False

  def rename_pairs(self):
    """

    :param self:
    :return:
    """
    self.was_renamed_tuple_list = []
    n_of_renames = 0
    for rename_tuple in self.rename_tuple_list:
      filename_from, filename_to = rename_tuple
      if not os.path.exists(filename_from):  # it may be either a file, a dir or a link
        print('file_from', filename_from, 'does not exist, continuing...')
        continue
      if os.path.exists(filename_to):  # cannot rename to name for such already exists
        print('file_to', filename_to, 'already exists, continuing...')
        continue
      n_of_renames += 1
      print(n_of_renames, ':: renaning pair')
      os.rename(filename_from, filename_to)
      self.was_renamed_tuple_list.append(rename_tuple)

  def print_rename_result(self):
    """

    :return:
    """

    if len(self.was_renamed_tuple_list) == 0:
      print('No local_folder_files were renamed or sized to a different position', self.pos_from)
      return
    print('='*40)
    print('Files renamed:')
    for i, rename_tuple in enumerate(self.was_renamed_tuple_list):
      seq = i + 1
      filename_from, filename_to = rename_tuple
      print(seq, filename_from, )
      print('To ==>>>', filename_to)

  def process_rename(self):
    """

    :return:
    """
    print('@confirm_renames')
    self.gather_renamepairs_ifany()
    if self.confirm_renames():
      self.rename_pairs()
    self.print_rename_result()


def get_args():
  pos, ext = None, None
  for arg in sys.argv:
    if arg == '-h' or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-e='):
      ext = arg[len('-e='):]
    elif arg.startswith('-p='):
      try:
        pos = int(arg[len('-p='):])
      except ValueError:
        pass
  return pos, ext


def process():
  pos_from, extension = get_args()
  scrmsg = f'Arguments collected are: pos_from = {pos_from} | ext = {extension}'
  print(scrmsg)
  renamer = Renamer(pos_from, extension)
  renamer.process_rename()


if __name__ == '__main__':
  process()
