#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys
import getopt
'''
Options
'''
#import renameCleanBeginning as rcb

INPUT_DATA_FILE_WITH_RENAME_PAIRS = 'renameZebraStripedInputPairs.txt'

def print_explanation_and_exit():
  print '''
  Info: This scripts takes no arguments.
  It expects the existence of a local data file named 'renameZebraStripedInputPairs.txt'.
  This is file has new filename in one line and current filename, the one to be renamed, on the following line. 
  '''
  sys.exit(0)

def gatherRenameTuples():
  lines = open(INPUT_DATA_FILE_WITH_RENAME_PAIRS).readlines()
  filenames = []; newFilenames = []
  for i, line in enumerate(lines):
    line = line.rstrip(' \t\r\n')
    if i % 2 == 0:
      # rename-to
      newFilenames.append(line)
    else:
      # rename-from
      filenames.append(line)
  renameTuples = zip(filenames, newFilenames)
  return renameTuples 
   
def rename(renameTuples, doRename=False):
  for i, renameTuple in enumerate(renameTuples):
    filename = renameTuple[0]
    if not os.path.isfile(filename):
      print filename, 'does not exist. Continuing.'
      continue
    newFilename = renameTuple[1] + ' ' + filename
    print i+1, ': Renaming:', filename
    print '> to: [' + newFilename + ']'
    if doRename:
      os.rename(filename, newFilename)
      print 'Renamed!'
  if not doRename:
    ans = raw_input('Are you sure? (y/N) ')
    if ans.lower() == 'y':
      return rename(renameTuples, doRename=True)
    else:
      return

def process():
  for arg in sys.argv:
    if arg in ['-h', '--help']:
      print_explanation_and_exit()
  renameTuples = gatherRenameTuples()
  rename(renameTuples)

if __name__ == '__main__':
  process()
  # unittest.main()
