#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, os, sys
#pys = glob.glob('*.py')
#pys.sort()
fileIn = sys.argv[1]
pys = [fileIn]
for py in pys:
  text = open(py).read()
  text = text.replace('\t','  ')
  os.rename(fileIn, fileIn + '.bak')
  print 'Writing', fileIn, 'without tabs'
  outFile = open(fileIn, 'w')
  outFile.write(text)
  outFile.close()
  