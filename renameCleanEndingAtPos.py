#!/usr/bin/env python
import os, sys

class Renamer:

  def __init__(self, posFrom):
    '''

    :param posFrom:
    '''
    self.posFrom = posFrom
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
      ext=''
      if filename_from.find('.') > -1:
        ext = filename_from.split('.')[-1]
      tamExt = len(ext) + 1
      if self.posFrom >= len(filename_from) - tamExt:
        continue
      filename_to = filename_from[:self.posFrom]
      if ext <> '':
        filename_to += '.' + ext
      # attribute source and target to rename_tuple
      rename_tuple = (filename_from, filename_to)
      self.rename_tuple_list.append(rename_tuple)

  def doesUserConfirmRenames(self):
    '''

    :param self:
    :return:
    '''
    for rename_tuple in self.rename_tuple_list:
      filename_from, filename_to = rename_tuple
      print 'From: ', filename_from
      print 'To: '  , filename_to
    ans = raw_input('Confirm renames above ? (y/N) ')
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
      print 'No local_folder_files were renamed or they are sized above position', self.posFrom
      return

    print '='*40
    print 'Files renamed:'
    for i, rename_tuple in enumerate(self.was_renamed_tuple_list):
      seq = i + 1
      filename_from, filename_to = rename_tuple
      print seq, filename_from,
      print 'To ==>>>', filename_to

if __name__ == '__main__':
  posFrom = int(sys.argv[1])
  renamer = Renamer(posFrom)
