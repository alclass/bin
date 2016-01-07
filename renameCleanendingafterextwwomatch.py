#!/usr/bin/env python
import os, sys #, shutil, sys

nOfCharsToChopOffAtEnding = int(sys.argv[1])
if nOfCharsToChopOffAtEnding < 1:
  print nOfCharsToChopOffAtEnding, 'should be 1 or more.'
  sys.exit(0)

matchStr = ''	
if len(sys.argv) > 2:
  matchStr = sys.argv[2]

startDir = os.path.abspath('.')
for i in [0,1]:
  c=0
  for this, folder, files in os.walk(startDir):
    dirNow = os.path.join(startDir, this)
    os.chdir(dirNow)
    print ' [NOW FOLDER]', dirNow
    files.sort()
    for fil in files:
      if len(fil) - nOfCharsToChopOffAtEnding < 1:
        continue
      if len(matchStr) > 0 and fil[-nOfCharsToChopOffAtEnding:] <> matchStr:
        continue
      newName = fil[:-nOfCharsToChopOffAtEnding]
      c += 1
      if i==0:
        print c, 'Renaming', fil
        print '> to:', newName
      if i==1:
        print ' [RENAMING]', newName
        os.rename(fil, newName)
  if c==0:
    print 'No files match for renaming'
    break
  if i==0 and c > 0:
    print 'Parameters used:'
    print '* nOfCharsToChopOffAtEnding =', nOfCharsToChopOffAtEnding
    print '* startDir', startDir
    if len(matchStr) == 0:
      print '* no ending string match'
    else:
      print '* ending string match', matchStr
    ans = raw_input('Are you sure to rename these ' + str(c) + ' files? (y/n) ')
    if ans != 'y':
      break
