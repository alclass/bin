#!/usr/bin/env python
import glob, os, shutil, sys

kbps = int(sys.argv[1])

startingDir = os.path.abspath('.')
for entry, folders, files in os.walk(startingDir):
    os.chdir(entry)
    print 'entry', entry
    os.system('pylame.py ' + str(kbps))
