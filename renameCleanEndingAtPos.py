#!/usr/bin/env python3
"""
renameCleanEndingAtPos.py
"""
import os
import sys


class Renamer:

  def __init__(self, p_pos_from=None):
    """
    :param p_pos_from:
    """
    self.pos_from = p_pos_from
    self.rename_tuple_list = []
    self.was_renamed_tuple_list = []

  def gather_renamepairs_ifany(self):
    """
    :return:
    """
    local_folder_files = os.listdir('.')
    sorted(local_folder_files)
    for filename_from in local_folder_files:
      ext = ''
      if filename_from.find('.') > -1:
        ext = filename_from.split('.')[-1]
      tam_ext_with_dot = len(ext) + 1
      if self.pos_from >= len(filename_from) - tam_ext_with_dot:
        continue
      filename_to = filename_from[:self.pos_from]
      if ext != '':
        filename_to += '.' + ext
      # attribute source and target to rename_tuple
      rename_tuple = (filename_from, filename_to)
      self.rename_tuple_list.append(rename_tuple)

  def confirm_renames(self):
    """
    :return:
    """
    for rename_tuple in self.rename_tuple_list:
      filename_from, filename_to = rename_tuple
      print('From: ', filename_from)
      print('To: ', filename_to)
    ans = input('Confirm renames above ? (y/N) ')
    if ans in ['y', 'Y']:
      return True
    return False

  def rename_pairs(self):
    """

    :param self:
    :return:
    """
    self.was_renamed_tuple_list = []
    for rename_tuple in self.rename_tuple_list:
      filename_from, filename_to = rename_tuple
      if not os.path.exists(filename_from):  # it may be either a file, a dir or a link
        continue
      os.rename(filename_from, filename_to)
      self.was_renamed_tuple_list.append(rename_tuple)

  def process_rename(self):
    """

    :return:
    """
    self.gather_renamepairs_ifany()
    if self.confirm_renames():
      self.rename_pairs()
    self.print_rename_result()

  def print_rename_result(self):
    """

    :return:
    """

    if len(self.was_renamed_tuple_list) == 0:
      print('No local_folder_files were renamed or they are sized above position', self.pos_from)
      return
    print('='*40)
    print('Files renamed:')
    for i, rename_tuple in enumerate(self.was_renamed_tuple_list):
      seq = i + 1
      filename_from, filename_to = rename_tuple
      print(seq, filename_from, )
      print('To ==>>>', filename_to)


if __name__ == '__main__':
  pos_from = int(sys.argv[1])
  renamer = Renamer(pos_from)
  renamer.process_rename()
