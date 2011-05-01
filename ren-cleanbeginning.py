#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys

posFrom = int(sys.argv[1])
        
files=os.listdir('.')
files.sort()
for i in range(0,2):
    c=0
    for fil in files:
        ext=''
        if fil.find('.') > -1:
            ext = fil.split('.')[-1]
            tamNameWithoutExt = len(fil) - (len(ext) + 1)
            if posFrom >= tamNameWithoutExt:
                continue
        elif posFrom >= len(fil):
            continue
        newName = fil[posFrom:]
        c += 1
        print c, 'renaming', fil
        print '> to:>>>'+newName
        if i==1:
            os.rename(fil, newName)
    if c==0:
        print 'No files are sized above position', posFrom
        break
    if i==0 and c > 0:
        ans = raw_input('Are you sure? (y/n) ')
        if ans != 'y':
            break
