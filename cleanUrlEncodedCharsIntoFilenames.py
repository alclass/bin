#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

SPACE_ENC = '%20'

def runCurrentFolder(doRename=False):
  '''
  runCurrentFolder(doRename=False)
  '''
  files = os.listdir('.')
  for eachFile in files:
    if eachFile.find(SPACE_ENC) > -1:
      newFilename = eachFile.replace(SPACE_ENC, ' ')
      print '[to rename]', eachFile, newFilename,
      if doRename:
        os.rename(eachFile, newFilename)
        if os.path.isfile(newFilename):
          print '[renamed]'
      else: # ie, not renaming, just line feeding former print ending with comma
        print

def processRename():
  '''
  confirm_renames()
  '''
  runCurrentFolder(doRename=False)
  print ' *** QUESTION *** '
  print 'Rename files above ? (s (or y) / n)'
  ans = raw_input(' s/n ')
  if ans in ['y', 'Y', 's', 'S']:
    runCurrentFolder(doRename=True)

if __name__ == '__main__':
  processRename()
