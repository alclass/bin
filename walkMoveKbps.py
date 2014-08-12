#!/usr/bin/env python
import glob, os #, shutil, sys

startingDir = os.path.abspath('.')
for entry, folders, files in os.walk(startingDir):
    absEntry = os.path.abspath(entry)
    folderEntered = absEntry.split('/')[-1]
    print '>>> Entering', folderEntered
    os.chdir(absEntry)
    kbpsList = []
    for fil in files:
        pp = fil.split('.')
        if len(pp) > 2:
            kbps = pp[-2]
            if folderEntered.find(kbps) > -1:
                # this is to avoid pushing files one level further
                # when they're correctly placed
                continue
            if kbps not in kbpsList:
                kbpsList.append(kbps)
    for kbps in kbpsList:
        folderName = folderEntered + ' ' + kbps
        if not os.path.isdir(folderName):
            print 'making dir', folderName
            os.mkdir(folderName)
        globPatt = '*.' + kbps + '.*'
        comm = 'mv ' + ' ' + globPatt + ' "./' + folderName + '"'
        print comm
        os.system(comm)
