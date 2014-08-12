#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys

sufix = sys.argv[1]
        
files=os.listdir('.')
files.sort()
for i in range(0,2):
    c=0
    for fil in files:
        newName = fil + sufix
        c += 1
        print c, 'renaming', fil
        print '> to:', newName
        if i==1:
            os.rename(fil, newName)
    if i==0 and c > 0:
        ans = raw_input('Are you sure? (y/n) ')
        if ans != 'y':
            break
