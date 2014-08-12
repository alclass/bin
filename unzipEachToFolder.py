#!/usr/bin/env python
import glob, os

zips = glob.glob('*.zip')

c=0
for zip in zips:
    folder = zip[:-4]
    if os.path.isdir(folder):
        continue
    comm = 'unzip "'+zip+'" -d "' + folder + '"'
    print c+1, 'unzipping', zip
    retValue = os.system(comm)
    if retValue == 0:
        c += 1
print 'Total unzipped:', c, '||| Total no. of zip files:', len(zips)

