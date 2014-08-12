#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys

beginningStrToWipeOut = string.lower(sys.argv[1])
        
files=os.listdir('.')
files.sort()
for fil in files:
    name = fil.lower()
    if name.startswith(beginningStrToWipeOut):
        newName = name[len(beginningStrToWipeOut):]
        print 'renaming', fil
        print '> to:', newName
        os.rename(fil, newName)
                
