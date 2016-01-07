#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, re, sys, time

# import logging
# LOG_FILENAME = 'zlog-uTubeRenameIdsFilesAddingTheirTitles-%s.log' %(time.time())
# logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

'''
Explanation:  

  uTubeRenameAddBeforeDashVideoid.py
  This script add a string before the dash-videoid-dot-extension
  Example:  abc-videoid_123.mp4
	prompt>uTubeRenameAddBeforeDashVideoid.py -e=mp4 -s=" (add this) "
  Result:  abc (add this) -videoid_123.mp4
'''

DEFAULT_EXTENSION = 'mp4'


class Renamer(object):
  '''
  '''
  
  def __init__(self, addtext, extension=None):
    """

    :param addtext:
    :param extension:
    :raise ValueError:
    """
    if addtext == None:
      raise ValueError, "Renamer must receive an 'addtext' input parameter. It's been passed as None."
    self.addtext = addtext
    if extension==None:
      self.extension = DEFAULT_EXTENSION
    else:
      self.extension = extension
    self.dot_extension = '.' + extension
    self.filename_ending_size = 12 + len(self.dot_extension)
    self.rename_pairs = []
    self.process()

    
  def process(self):
    glob_param = '*' + self.dot_extension
    files = glob.glob(glob_param)
    print glob_param, files
    if len(files) == 0:
      print 'No files to rename.'
      return
    for eachFile in files:
      if len(eachFile) > self.filename_ending_size:
        midtarget_position = len(eachFile) - self.filename_ending_size
        newFile = eachFile[ : midtarget_position] + self.addtext + eachFile[ midtarget_position : ]
        rename_pair = (eachFile, newFile)
        self.rename_pairs.append(rename_pair)
    if self.please_confirm_batch_rename():
      self.batch_rename_one_by_one()
    
  def please_confirm_batch_rename(self):
    '''
      To ask the user to confirm the renaming
    '''
    total_to_rename = len(self.rename_pairs)
    for i, rename_pair in enumerate(self.rename_pairs):
      n_seq_to_rename = i+1
      print n_seq_to_rename
      oldname = rename_pair[0]
      newname = rename_pair[1]
      print '[from:]', oldname 
      print '[to:]',   newname
    print 'Total of videofiles to rename:', total_to_rename
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
  uTubeRenameAddBeforeDashVideoid.py
  This script add a string before the dash-videoid-dot-extension
  Example:  abc-videoid_123.mp4
	prompt>uTubeRenameAddBeforeDashVideoid.py -e=mp4 -s=" (add this) "
  Result:  abc (add this) -videoid_123.mp4

  '''
  sys.exit(0)
  
def process():
  if 'help' in sys.argv:
    print_usage_and_exit()
  addtext = None; extension = None # DEFAULT_EXTENSION
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[len('-e='):]
    elif arg.startswith('-s='): 
      addtext = arg[len('-s='):]
  if addtext == None:
    print_usage_and_exit()
  Renamer(addtext=addtext, extension=extension)

if __name__ == '__main__':
  process()
