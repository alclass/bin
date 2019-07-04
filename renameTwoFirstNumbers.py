#!/usr/bin/env python3
'''
This rename script is useful for renaming files
with 2 numbers at the beginning separated by
spaces and periods (and other characters)
and reorganizes them like [[n-m]]
ie the two numbers being separated by a '-' (dash).

Eg. ' 3 . 10 bla.mp4' renames to '3-10 bla.mp4'
-----------------------------------------------

If the two files at end are equal, no rename occurs.
'''
import glob, os, string, sys

DEFAULT_FILE_EXTENSION = 'mp4'
DEFAULT_ZFILL = 2


def getBeginningNumber(name):
  '''
  This function could've been implemented with a RegExp.
  The way chosen here was to:
   1) transform a string to a list
   2) reverse the list, so that pop() takes the first character out
   3) keeps on poping until no numbers are taken
   4) returns either a number or None and the remaining string after the number

  Example for tests:
  s = ' 3 blah'
  returns 3, 'blah'

  :param name:
  :return:
  '''
  namelist = list(name.strip())
  namelist.reverse()
  str_n = ''
  while len(namelist) > 0:
    n = namelist.pop()
    if n in string.digits:
      str_n += n
      found_number = True
    else:
      if len(str_n) > 0:
        break
  namelist.reverse()
  remains = ''.join(namelist)
  if len(str_n) > 0:
    return int(str_n), remains
  return None, remains

class Renamer:

  def __init__(self, file_extension=None, zfill=None):
    if file_extension is None:
      file_extension = DEFAULT_FILE_EXTENSION
    if zfill is None:
      self.zfill = DEFAULT_ZFILL
    self.renameList = []
    self.mp4s = glob.glob('*.' + file_extension)
    sorted(self.mp4s)
    self.process()

  def gatherRenames(self):
    for mp4 in self.mp4s:
      oldName = mp4
      mp4 = mp4.strip('')
      n, remains = getBeginningNumber(mp4)
      if n is None:
        continue
      n1 = n
      n, remains = getBeginningNumber(remains)
      if n is None:
        continue
      n2 = n
      newName = str(n1).zfill(self.zfill) + '-' + str(n2).zfill(self.zfill) + ' ' + remains
      # there is a strong assumption here, ie, when the newName is composed, it cannot be too much smaller
      if len(newName) < 4 or len(newName) < len(mp4) - 4:
        continue
      # here, filenames are the same, so do not append it to renamelist
      if newName == mp4:
        continue
      self.renameList.append((oldName, newName))

  def printNConfirmRenames(self):
    if len(self.renameList) == 0:
      print ('No files to rename.')
      return False
    for i, renamePair in enumerate(self.renameList):
      oldName, newName = renamePair
      print (i+1, 'FROM: ', oldName)
      print (i+1, '  TO: ', newName)
      print ('Total renames is', len(self.renameList))
      print ('Total filenames on folder is', len(self.mp4s))
    answer = input('Confirm renames (y/N) ? ')
    if answer in ['y','Y']:
      return True
    return False

  def doRename(self):
    n_of_renames = 0
    for i, renamePair in enumerate(self.renameList):
      oldName, newName = renamePair
      os.rename(oldName, newName)
      n_of_renames += 1
    print ('n_of_renames = ', n_of_renames)

  def process(self):
    self.gatherRenames()
    bool_answer = self.printNConfirmRenames()
    if bool_answer:
      self.doRename()

def print_help_and_exit():
  print(__doc__)
  print ('bla')
  sys.exit(0)

def get_args():
  file_extension = None
  zfill = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      file_extension = arg[len('-e='):]
    if arg.startswith('-zfill='):
      zfill = int(arg[len('-zfill='):])
    if arg in ['-h','--help']:
      print_help_and_exit()
  return file_extension, zfill

if __name__ == '__main__':
  file_extension, zfill = get_args()
  Renamer(file_extension, zfill)
