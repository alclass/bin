#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  This script aims to renumber files in a directory.
  The renumbering occurs for files having 2-digit numbers from 00 to 99, but it, when renaming, it will start at 01
  There are TWO species of renaming here. One with truncation, the other with preprending.

  In practice, suppose there are these files:

03 filename X.ext
05 filename Y.ext
41 filename Z.ext

  After running this script, they will become

01 filename X.ext
02 filename Y.ext
03 filename Z.ext

 The '-a' CLI parameter only prepends numbers to the filenames.
 Usage is: comm -a [<optional start number>]

  IMPORTANT: this script does not take into account file numbers above 99, and 00 is left as is
'''
import os, sys

def processRename(filDict, doRename=False):
  nOfFiles=len(filDict)
  print 'nOfFiles', nOfFiles
  numbers=filDict.keys()
  numbers.sort()
  nToRename = 0; nOfRenamed = 0
  for number in numbers:
    seqFil = filDict[number][0]
    print number, seqFil
    if number <> seqFil:
      fil = filDict[number][1]
      newName = str(number).zfill(2) + ' ' + fil[3:]
      if os.path.isfile(newName):
	print 'file', newName, 'exists.  Jumping off this one.'
	continue
      nToRename += 1
      print number, 'Renaming:'
      print 'FROM: ', fil
      print 'TO:   ', newName
      if doRename:
	os.rename(fil, newName)
	if os.path.isfile(newName):
	  nOfRenamed+=1

  if doRename:
    print 'nOfRenamed =', nOfRenamed
  return nToRename, nOfRenamed

def collectFilDict():
  files=os.listdir('.')
  files.sort()
  filDict= {}; c=0; seq=0
  for fil in files:
    if os.path.isfile(fil):
      c+=1
      print c, fil
      if len(fil) > 3:
	pp = fil.split(' ')
	try:
	  n = int(pp[0])
	except ValueError:
	  #print 'fil', fil, 'not starting with a 2-digit number plus space. Continuing.'
	  #continue
	  pass
	except IndexError:
	  pass
	seq+=1
	filDict[seq] = (1,fil)
  return filDict

def doPrependNumbers(n_rename_start, doRename=False):
  files = os.listdir('.')
  if len(files) > 99:
    print 'There are more than 99 files. Giving up.'
    return
  files.sort(); nToRename = n_rename_start
  for filename in files:
    preprend_str = '%02d ' %nToRename
    newfilename = preprend_str + filename
    if doRename:
      print nToRename, 'renaming [%s] TO [%s]' %(filename, newfilename)
      os.rename(filename, newfilename)
    else:
      print nToRename, 'To rename [%s] TO [%s]' %(filename, newfilename)
    nToRename += 1
  if not doRename:
    print 'ATTENTION:'
    print 'Do you really want to rename those', nToRename, 'files above ? '
    ans = raw_input(' y/N ? ')
    if ans in ['y','Y']:
      doPrependNumbers(n_rename_start, doRename=True)



def main():
  try:
    if sys.argv[1] == '-a':
      n_rename_start = 1
      if len(sys.argv) > 2:
        try:
          n_rename_start = int(sys.argv[2])
        except ValueError:
          pass
      doPrependNumbers(n_rename_start)
      return
  except IndexError:
    pass
  filDict = collectFilDict()
  nToRename, nOfRenamed = processRename(filDict, False)
  if nToRename == 0:
    print 'No files to rename. Bye.'
    sys.exit(0)
  print 'ATTENTION:'
  print 'Do you really want to rename those', nToRename, 'files above ? '
  ans = raw_input(' y/n ? ')
  if ans in ['y','Y']:
    nToRename, nOfRenamed = processRename(filDict, True)
    print nOfRenamed, 'files renamed of', nToRename, 'to rename.'

if __name__ == '__main__':
  main()
