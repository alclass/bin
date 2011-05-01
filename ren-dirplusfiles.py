#!/usr/bin/env python
import glob, os #, shutil, sys

dirs=os.listdir('.')
dirs.sort()
for aDir in dirs:
    if os.path.isdir(aDir):
        print ' [ Entering directory:', aDir, ']'
        os.chdir(aDir)
        files=os.listdir('.')
        files.sort()
        for fil in files:
            if os.path.isfile(fil):
                newName = aDir + ' ' + fil
                print 'renaming', fil, 'to', newName
                os.rename(fil, newName)
        os.chdir('..')
                
