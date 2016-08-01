#!/usr/bin/env python
import os, sys

class Renamer:

  def __init__(self, chars_list):
    '''

    :param posFrom:
    '''
    self.chars_list = chars_list
    self.rename_tuple_list = []
    self.was_renamed_tuple_list = []
    self.processRename()

  def processRename(self):
    '''

    :return:
    '''
    self.gatherRenamePairsIfAny()
    if self.doesUserConfirmRenames():
      self.renamePairsConfirmed()
    self.printRenameResult()

  def gatherRenamePairsIfAny(self):
    '''

    :return:
    '''
    local_folder_files = os.listdir('.')
    local_folder_files.sort()
    for filename_from in local_folder_files:
      filename_from_orig = filename_from
      for specific_char in self.chars_list:
        if filename_from.find(specific_char) > -1:
          filename_from = filename_from.replace(specific_char, '')

      if filename_from <> filename_from_orig and len(filename_from) > 0:
        filename_to = filename_from
        filename_from = filename_from_orig
        rename_tuple = (filename_from, filename_to)
        self.rename_tuple_list.append(rename_tuple)

  def doesUserConfirmRenames(self):
    '''

    :param self:
    :return:
    '''

    if len(self.rename_tuple_list) == 0:
      return False

    for i, rename_tuple in enumerate(self.rename_tuple_list):
      seq = i + 1
      filename_from, filename_to = rename_tuple
      print str(seq).zfill(2), 'From: ', filename_from
      print 'To:      '  , filename_to
    msg = 'Confirm the %02d renames above ? (y/N) ' %(len(self.rename_tuple_list))
    ans = raw_input(msg)
    if ans in ['y', 'Y']:
      return True
    return False

  def renamePairsConfirmed(self):
    '''

    :param self:
    :return:
    '''
    self.was_renamed_tuple_list = []
    for rename_tuple in self.rename_tuple_list:
      filename_from, filename_to = rename_tuple
      if not os.path.exists(filename_from): # it may be either a file, a dir or a link
        continue
      os.rename(filename_from, filename_to)
      self.was_renamed_tuple_list.append(rename_tuple)

  def printRenameResult(self):
    '''

    :return:
    '''

    if len(self.was_renamed_tuple_list) == 0:
      print 'No local_folder_files were renamed or they did not contain the chars:', self.chars_list
      return

    print '='*40
    print 'Files renamed:'
    for i, rename_tuple in enumerate(self.was_renamed_tuple_list):
      seq = i + 1
      filename_from, filename_to = rename_tuple
      print seq, filename_from,
      print 'To ==>>>', filename_to

if __name__ == '__main__':
  if len(sys.argv) > 1:
    chars_list = int(sys.argv[1])
  else:
    chars_list = ':'
  renamer = Renamer(chars_list)
