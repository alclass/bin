#!/usr/bin/env python
import glob, os, shutil, sys

def doKuickShow(entry, fil):
    global entryFolders
    entryFolders += 1
    print entryFolders, entry, 'kuickshow *'
    os.chdir(entry)
    os.system('kuickshow "'+fil+'"')

entryFolders = 0
extList = ['jpg','jpeg','bmp','png','gif']
startingDir = os.path.abspath('.')
for entry, folders, files in os.walk(startingDir):
    files.sort()
    for fil in files:
        if fil[-3:] in extList:
            doKuickShow(entry, fil)
            break
        elif fil[-4:] in extList:
            doKuickShow(entry, fil)
            break
print 'Total entryFolders', entryFolders
