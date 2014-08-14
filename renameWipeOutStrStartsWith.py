#!/usr/bin/env python
'''
Rename entries on a local directory, be they files or subdirectories, that starts with the incoming parameter string
  renameWipeOutStrStartsWith.py "<string as file-or-directory beginning>"
'''
import glob, os, string, sys #, shutil, sys

class Renamer(object):
  '''
  '''
  def __init__(self, beginningStrToWipeOut):
    """
    :param addtext:
    :param extension:
    :raise ValueError:
    """
    if beginningStrToWipeOut == None:
      raise ValueError, "Renamer must receive an 'beginningStrToWipeOut' input parameter. It's been passed as None."
    self.beginningStrToWipeOut = beginningStrToWipeOut
    self.rename_pairs = []
    self.process()

  def process(self):
    self.prepare_renames()
    if self.please_confirm_batch_rename():
      self.batch_rename_one_by_one()

  def prepare_renames(self):
    files_or_subdirs = os.listdir('.')
    files_or_subdirs.sort()
    for file_or_subdir in files_or_subdirs:
      if len(file_or_subdir) <= len(self.beginningStrToWipeOut):
        continue
      if file_or_subdir.startswith(self.beginningStrToWipeOut):
        newName = name[len(self.beginningStrToWipeOut):]
        rename_pair = (file_or_subdir, newName)
        self.rename_pairs.append(rename_pair)

  def please_confirm_batch_rename(self):
    '''
      To ask the user to confirm the renaming
    '''
    total_to_rename = len(self.rename_pairs)
    if total_to_rename == 0:
      print 'No files or subdirectories to rename.'
      return False
    for i, rename_pair in enumerate(self.rename_pairs):
      n_seq_to_rename = i+1
      print n_seq_to_rename
      oldname = rename_pair[0]
      newname = rename_pair[1]
      print '[from:]', oldname
      print '[to:]  ', newname
    print 'Total of files/directories to rename:', total_to_rename
    ans = raw_input(' Y*/n (Obs: only "n" or "N" will stop renaming.): ')
    if ans in ['n', 'N']:
      print 'No renaming.'
      return False # sys.exit(0)
    return True

  def batch_rename_one_by_one(self):
    '''
      Loop all video ids, renaming oldname to newname
    '''
    self.n_renamed = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      n_seq_to_rename = i+1
      print n_seq_to_rename
      oldname = rename_pair[0]
      newname = rename_pair[1]
      print '[from:]', oldname
      print '[to:]',   newname
      print self.n_renamed + 1, 'Renaming [%s] TO [%s]' %(oldname, newname),
      os.rename(oldname, newname)
      print '[done]'
      self.n_renamed += 1
    print 'n_renamed =', self.n_renamed

def print_usage_and_exit():
  print '''Usage:
  renameWipeOutStrStartsWith.py "<string as file-or-directory beginning>"
  '''
  sys.exit(0)

def process():
  if 'help' in sys.argv:
    print_usage_and_exit()
  if len(sys.argv) < 2:
    print_usage_and_exit()
  beginningStrToWipeOut = string.lower(sys.argv[1])
  Renamer(beginningStrToWipeOut)

if __name__ == '__main__':
  process()
