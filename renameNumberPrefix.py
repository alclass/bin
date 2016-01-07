#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys

try:
  startNumber = int(sys.argv[1])
except:
  startNumber = 1
        
files=os.listdir('.')
files.sort()
for i in range(0,2):
    seq = startNumber
    c = 0
    for fil in files:
        newName = str(seq).zfill(2) + ' ' + fil
        seq += 1
        c += 1
        print c, 'renaming', fil
        print '> to:', newName
        if i==1:
            os.rename(fil, newName)
    if i==0 and c > 0:
        ans = raw_input('Are you sure? (y/n) ')
        if ans != 'y':
            break
