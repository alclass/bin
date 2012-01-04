#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation

This script copies files in alphabetic order to a folder (dir / usbDir).
This usbDir variable is found in dirToUsb.py, which must be imported as
  from dirToUsb import *
 to expose the usbDir variable
 
Previously, this script used a different scheme
It used a second variable 'baseFilename'
This variable is a string with a placeholder such as %02d
 so that numbers could be rolled out and filenames with such numbers generated
This scheme was abandoned

This current approach is just to order the mp3's in alphabetic order
 and then copy one after the other
 with a 3-second time interval
 ie, time.sleep(3) 
'''
import glob, os, shutil, sys, time

usbDir = None
if len(sys.argv) > 1 and sys.argv[1]=='-d':
  usbDir = sys.argv[2]
  if not os.path.isdir(usbDir):
    print 'dir', usbDir, 'is not an existing directory.'
    sys.exit(1)
elif not os.path.isfile('dirToUsb.py'):
  print '''***
  Please, create the local dirToUsb.py file (in this folder) 
  with one variable:
    1) (required) usbDir
    It's no longer necessary to create an second:
    2) (optional) baseFilename with a %02d -like placeholder
  '''
  sys.exit(0)

EXTENSION = 'mp3'
argv = sys.argv[:]
while len(argv) > 0:
  arg = argv[0]
  del argv[0]
  if arg.startswith('-ext='):
    EXTENSION = arg[len('-ext='):]
    break

if usbDir == None:
  sys.path.insert(0, '.')
  # importing variables 
  # baseFilename & usbDir
  from dirToUsb import *
    
def copyMp3s():

  mp3s = glob.glob('*.' + EXTENSION)
  mp3s.sort(); nOfMp3 = 0
  for mp3 in mp3s:
    targetMp3 = os.path.join(usbDir, mp3)
    if os.path.isfile(targetMp3):
      continue
    nOfMp3+=1
    print nOfMp3, 'Copying', mp3
    shutil.copy2(mp3, targetMp3)
    # wait 3 seconds
    time.sleep(3)

if __name__ == '__main__':
  # copyToUsb()
  copyMp3s()

sys.exit(0)

# =========================
# legacy code below
# =========================

argMsg = 'Please, enter with the two arguments (fromNumber and toNumber)'

def pickUpArgs():
  if len(sys.argv) < 3:
    print argMsg
    sys.exit(0)
  try:
    fromNumber = int(sys.argv[1])
    toNumber   = int(sys.argv[2])
  except ValueError:
    print argMsg
    sys.exit(0)
  return fromNumber, toNumber

def copyToUsb():
  fromNumber, toNumber = pickUpArgs()
  print '''fromNumber = %d
toNumber = %d
>> Press <Enter> to confirm copying OR Ctrl-C to break out and not continue.''' %(fromNumber, toNumber)
  ans = raw_input('...')
  for i in range(fromNumber, toNumber + 1):
    fil = baseFilename %i
    if not os.path.isfile(fil):
      print fil, 'does not exist. Continuing.'
      continue
    print 'Copying', fil
    print 'To', usbDir
    shutil.copy2(fil, usbDir)
    # wait 3 seconds
    time.sleep(3)
