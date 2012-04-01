#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
...

'''
import glob, os, shutil, sys, time

DEFAULT_EXT = 'm4v'
DEFAULT_NEW_NAME_LISTING_FILE = 'course-titles.txt'

class InputArguments:
  def __init__(self):
    self.shouldBeExt        = DEFAULT_EXT
    self.newNameListingFile = DEFAULT_NEW_NAME_LISTING_FILE
    for arg in sys.argv:
      if arg.startswith('-e='):
        self.shouldBeExt = arg[len('-e='):]
      elif arg.startswith('-n='):
        self.newNameListingFile = arg[len('-n='):]

def pickUpNewNames(newNameListingFile = DEFAULT_NEW_NAME_LISTING_FILE, shouldBeExt = DEFAULT_EXT):
  newNames = []
  if not os.path.isfile(newNameListingFile):
    print newNameListingFile, 'does not exist. Please, inform it via argument -n="<file>".'
    sys.exit(1)
  names = open(newNameListingFile).read().split('\n')
  seq = 0
  for name in names:
    if name == '' or name == '\n':
      continue
    seq += 1
    newName = str(seq).zfill(2) + ' ' + name + '.' + shouldBeExt.lower()
    if newName.find('/') > -1:
      newName = newName.replace('/', '_')
    newNames.append(newName)
  return newNames

def pickUpCurrentNames(shouldBeExt = DEFAULT_EXT):
  currentFiles = glob.glob('*.' + shouldBeExt)
  currentFiles.sort()
  return currentFiles
  
def uniteElementsOneToOne(currentFiles, newNames):
  tuplesToRename = []
  for i in range(len(currentFiles)):
    if i >= len(newNames):
      # raise IndexError, 'currentFiles and newNames do not have the same size.'
      # instead of raising an Exception as commented above, return tuplesToRename, "cutting" off currentFiles at i
      # this is then the Use Case here, ie, uniteElementsOneToOne until either one set finishes
      return tuplesToRename
    currentName = currentFiles[i]
    newName     = newNames[i]
    tupleToRename = currentName, newName
    tuplesToRename.append(tupleToRename)
  return tuplesToRename    
  
def pickUpCurrentAndNewNames(newNameListingFile, shouldBeExt):
  newNames = pickUpNewNames(newNameListingFile, shouldBeExt)
  currentFiles = pickUpCurrentNames(shouldBeExt)
  return uniteElementsOneToOne(currentFiles, newNames)

def rename(tuplesToRename, doRename=False):
  '''
  for i in range(len(currentFiles)):
    if i >= len(newNames):
      return
    currentName = currentFiles[i]
    newName     = newNames[i]
  '''
  seq = 0
  for tupleToRename in tuplesToRename:
    currentName, newName = tupleToRename
    seq+=1
    if doRename:
      os.rename(currentName, newName)
    else:
      print seq, 'Rename:'
      print '\t', currentName 
      print '\t', newName
  if len(tuplesToRename) > 0:
    if doRename:
      print seq, 'files were renamed.'
      return
    else:
      ans = raw_input('Rename them above ? (y/N) ')
      if ans in ['y','Y']:
        rename(tuplesToRename, doRename=True)
  else:
    print 'No files to rename.'

def process():
  argsObj = InputArguments()
  tuplesToRename = pickUpCurrentAndNewNames(argsObj.newNameListingFile, argsObj.shouldBeExt)
  rename(tuplesToRename)
     
if __name__ == '__main__':
  process()
