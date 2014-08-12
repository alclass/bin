#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys
import getopt

pos1 = int(sys.argv[1])
pos2=-1

'''
Options
'''


try:
    pos2 = int(sys.argv[1])
except IndexError:
    # position should be the end
    pass
    
        
files=os.listdir('.')
files.sort()
for i in range(0,2):
    c=0
    for fil in files:
        ext=''
        if fil.find('.') > -1:
            ext = fil.split('.')[-1]
        tamExt = len(ext) + 1
        if posFrom >= len(fil) - tamExt:
            continue
        newName = fil[posFrom:pos2]
        if ext <> '':
            newName += '.' + ext
        c += 1
        print c, 'renaming', fil
        print '> to:', newName
        if i==1:
            os.rename(fil, newName)
    if c==0:
        print 'No files are sized above position', posFrom
        break
    if i==0 and c > 0:
        ans = raw_input('Are you sure? (y/n) ')
        if ans != 'y':
            break
