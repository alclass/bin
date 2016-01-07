#!/usr/bin/env python
import glob, os, shutil #, shutil, sys

print 'Choose:'
print '1 = 24k'
print '2 = 64k'
n = raw_input('1 or 2 ? ')
n = int(n)
bitRate = '24k'
if n == 2:
    bitRate = '64k'

startingDir = os.path.abspath('.')
for entry, folders, files in os.walk(startingDir):
    absEntry = os.path.abspath(entry)
    if absEntry == startingDir:
        continue
    os.chdir(absEntry)
    globStr = '*.'+ bitRate +'.mp3'
    isThereFiles = glob.glob(globStr)
    if len(isThereFiles) > 0:
        for fil in isThereFiles:
            print 'moving', fil
            shutil.move(fil, startingDir)
