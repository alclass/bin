#!/usr/bin/env python
#-*-code:utf8-*-
'''
This script renames...
'''
import glob, os, sys

def doRenameAskingConfirmation(listOfFilesTupleForRename, doRename=False):
  total = len(listOfFilesTupleForRename); seq = 0
  for filesTupleForRename in listOfFilesTupleForRename:
    currentName, newName = filesTupleForRename
    seq += 1; renameLine = '%(seq)d of %(total)d Rename: "%(currentName)s" to "%(newName)s"' %{'seq':seq, 'total':total, 'currentName':currentName, 'newName':newName}
    print renameLine
    if doRename:
      os.rename(currentName, newName)
      print 'Renamed'
  if not doRename:
    ans = raw_input('Rename the above files ? (y/N) ')
    if ans in ['y', 'Y']:
      # call itself back, now with doRename as True
      doRenameAskingConfirmation(listOfFilesTupleForRename, doRename=True)
   
def processRename():
  # extension suffixes are GLOBAL here
  print '-'*50
  print 'Rename current folder files'
  print '-'*50
  files = os.listdir('.'); listOfFilesTupleForRename = []
  files.sort()
  for eachFile in files:
    if eachFile.find('-') < 0 and eachFile.find('_') < 0:
      if eachFile.find('  ') < 0:
        continue
    newFilename = eachFile
    newFilename = newFilename.replace('-', ' ')
    newFilename = newFilename.replace('_', ' ')
    newFilename = newFilename.replace('  ', ' ')
    listOfFilesTupleForRename.append((eachFile, newFilename))
  doRenameAskingConfirmation(listOfFilesTupleForRename)

if __name__ == '__main__':
  processRename()
