#!/usr/bin/env python
#-*-code:utf8-*-
'''
This script renames files having one given extension (eg. .txt) to another given extension (eg .abap)
The files affected are those having source extension on the current folder
  The default source and target extensions are, respectively, .txt and .abap
  The script accepts different extensions from arguments to the command line
    Eg. prompt > python renameFromOneExtensionToAnotherOnFolder.py -c=doc -n=odt
    The above example will set the source extension to doc and the target extension to odt

As informed above, this script intends to perform a folder-batch-rename, but it will do so upon confirmation

A reversal situation is logically possible if there were no files with the target extension before the renaming took place
  Eg. the user issued and confirmed:
    python renameFromOneExtensionToAnotherOnFolder.py -c=doc -n=odt
  if no .odt files existed before, a reversal is possible, issuing the command:
    python renameFromOneExtensionToAnotherOnFolder.py -c=odt -n=doc

'''
import glob, os, sys

# global variables (the user may change them via sys.argv, ie, args are -c=source_ext and -n=target_ext :: c stands for "current" and n for "new")
CURRENT_EXTENSION = 'txt'
currentExtension  = CURRENT_EXTENSION
NEW_EXTENSION     = 'abap'
newExtension      = NEW_EXTENSION

def printNothingToDoMessageAndExit():
  print '-'*50
  print "No .%s files on current folder to rename their extensions to .%s." %(currentExtension, newExtension)
  print '-'*50
  sys.exit(0)

def getListOfFilesTupleForRename(sourceFiles):
  '''
  Business Logic:
    only one: swap .source_ext to .target_ext in filenames
    How this is done: a pp = filename.split('.')[:-1] followed by '.'.join(pp)
    If more dots are found, no problem for we need the last one
  '''
  listOfFilesTupleForRename = []
  for eachFile in sourceFiles:
    # if eachFile.endswith('.txt'): # ok, no need, for files were picked up by 'glob'
    pp = eachFile.split('.')[:-1]
    extLessFilename = '.'.join(pp)
    newExtFilename =  extLessFilename + '.' + newExtension
    filesTupleForRename = eachFile, newExtFilename
    listOfFilesTupleForRename.append(filesTupleForRename)
  return listOfFilesTupleForRename

def doRenameAskingConfirmation(listOfFilesTupleForRename, doRename=False):
  total = len(listOfFilesTupleForRename); seq = 0
  for filesTupleForRename in listOfFilesTupleForRename:
    currentName, newName = filesTupleForRename
    seq += 1; renameLine = '%(seq)d of %(total)d Rename: "%(currentName)s" to "%(newName)s"' %{'seq':seq, 'total':total, 'currentName':currentName, 'newName':newName}
    print renameLine
    if doRename:
      os.rename(eachFile, abapExtName)
      print 'Renamed'
  if not doRename:
    ans = raw_input('Rename the above files ? (y/N) ')
    if ans in ['y', 'Y']:
      # call itself back, now with doRename as True
      doRenameAskingConfirmation(listOfFilesTupleForRename, doRename=True)
   
def checkIfThereAreExtensionSuffixesInArgs():
  global currentExtension, newExtension
  if len(sys.argv) < 2:
    return
  for arg in sys.argv[1:]:
    if arg.startswith('-c'):
      currentExtension = arg.split('=')[-1]
    elif arg.startswith('-n'):
      newExtension = arg.split('=')[-1]

def processRename():
  checkIfThereAreExtensionSuffixesInArgs()
  # extension suffixes are GLOBAL here
  print '-'*50
  print 'Rename current folder files from extension .%s to extension .%s'  %(currentExtension, newExtension)
  print '-'*50
  txts = glob.glob('*.' + currentExtension); total = len(txts)
  if total == 0:
    printNothingToDoMessageAndExit()
  listOfFilesTupleForRename = getListOfFilesTupleForRename(txts)
  doRenameAskingConfirmation(listOfFilesTupleForRename)

if __name__ == '__main__':
  processRename()
