#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
'''
import glob
import os
import sys

commBase = 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mp4)s"'
EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mov']

def batchConvertToMp4(extensions=[]):
  if len(extensions) == 0:
    extensions = EXTENSIONS_DEFAULT
  mediaFiles = []
  for ext in extensions:
    mediaFiles += glob.glob('*.%s' %ext)
  mediaFiles.sort(); seq = 0; total = len(mediaFiles)
  for mediaFile in mediaFiles:
    fileExtLess = os.path.splitext(mediaFile)[0]
    mp4 = fileExtLess + '.mp4'
    if os.path.isfile(mp4):
      print mp4, 'exists. Jumping to next...'
      continue
    comm = commBase %{'mediaFile':mediaFile, 'mp4':mp4}  
    print '='*40
    seq += 1; print seq, 'of', total, '::', comm
    print '='*40
    os.system(comm)

def fetchExtensionArguments():
  extensions = []
  for ext in sys.argv[1:]:
    extensions.append(ext)
  return extensions

def main():
  extensions = fetchExtensionArguments()
  batchConvertToMp4(extensions)

if __name__ == '__main__':
  main()
