#!/usr/bin/env python3
#-*-coding:utf-8-*-
import glob, os, sys #, time

def touchFiles(extension = None):
  globparam = '*'
  if extension != None:
    globparam += '.' + extension
  files = glob.glob(globparam)

  totaltotouch = 0
  for existingfile in files:
    if os.path.isdir(existingfile):
      continue
    filename, _ = os.path.splitext(existingfile)
    totaltotouch += 1
    comm = 'touch "' + filename + '.empty"'
    print(comm)
    os.system(comm)
  print('Total touched:', totaltotouch)
  

def process():
  extension = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[ len('-e=') : ]
  touchFiles(extension)

if __name__ == '__main__':
  process()
