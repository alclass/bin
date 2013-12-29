#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil, sys

def copying(source, target):
    msg = '''Do you want copy:
 source: %s
 target: %s'''
    print msg %(source, target)
    answer = raw_input(' (y/n) ? ')
    if answer in ['y','Y']:
      print 'Copying now.'
      shutil.copy2(source, target)

abspath=os.path.abspath('.')
'''
if abspath.find('ami7') > -1:
  print 'This case yet to implement. Bye.'
  sys.exit(0)
if abspath.find('ami3') > -1:
  print 'This case yet to implement. Bye.'
  sys.exit(0)
'''


otherMachine = sys.argv[1]
targetPath = '/net/' + otherMachine + abspath
files = os.listdir('.')
for eachFile in files:
  if os.path.isdir(eachFile):
    continue
  if eachFile[-1]=='~':
    continue
  if eachFile[-4:]=='.pyc':
    continue
  absSource = os.path.join(abspath, eachFile)
  copySituation = False
  absTarget = os.path.join(targetPath, eachFile)
  if not os.path.isfile(absTarget):
    print 'Target does not exist.'
    copying(absSource, absTarget)
  if not os.path.isfile(absTarget):
    # ok, user did not want to copy it, moving on
    continue
  statsSource = os.stat(absSource)
  statsTarget = os.stat(absTarget)
  print absSource
  print absTarget
  print 'statsSource', statsSource
  print 'statsTarget', statsTarget
  # size 7th element, 6 in index
  # modified date 9th element, 8 in index
  sizeSource = statsSource[6]
  sizeTarget = statsTarget[6]
  if sizeSource != sizeTarget:
    copySituation = True
    print 'Sizes differ',
    if sizeSource > sizeTarget:
      print 'Source is bigger'
    else:
      print 'Target is bigger'
  modifiedDateSource = statsSource[8]
  modifiedDateTarget = statsTarget[8]
  if modifiedDateSource != modifiedDateTarget:
    copySituation = True
    print 'ModifiedDates differ',
    if modifiedDateSource > modifiedDateTarget:
      print 'Source is later'
    else:
      print 'Target is later'
  if copySituation:
    copying(absSource, absTarget)

if __name__ == '__main__':
  pass
