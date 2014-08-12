#!/usr/bin/env python
#-*-code:utf8-*-
import os, sys #, shutil, sys

def renameFilesOnCurrentFolderStrippingItsEndingAs(endingStr, doRename=False):
  files=os.listdir('.'); files.sort(); seq = 0
  for eachFile in files:
    if not eachFile.endswith(endingStr):
      continue
    newName = eachFile[ : - len(endingStr) ]
    seq += 1
    if doRename:
      print seq, 'Renaming', eachFile, 'to', newName
    else:
      print seq, 'should', eachFile, 'be renamed'
      print '> to:', newName, '?'
    if doRename:
      os.rename(eachFile, newName)
  if len(files)==0 or seq == 0:
    print 'No files on current folder to rename, stripping its ending as', endingStr
  else:
    if not doRename:
      ans = raw_input('Are you sure? (y/N) ')
      if ans in ['y','Y']:
        renameFilesOnCurrentFolderStrippingItsEndingAs(endingStr, doRename=True)

if __name__ == '__main__':
  endingStr = sys.argv[1]
  renameFilesOnCurrentFolderStrippingItsEndingAs(endingStr)
 