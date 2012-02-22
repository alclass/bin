#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
'''
import glob
import os
import sys

class LocalData:
  commDict = {'audio' : 'ffmpeg -i "%(mediaFile)s" -acodec libmp3lame "%(mpx)s"', \
              'video' : 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mpx)s"'}
  EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mkv', 'mov', 'wmv']
 
class Media:
  def __init__(self, mediaFileFrom, totalToProcess, isAudio=False):
    self.mediaFileFrom  = mediaFileFrom
    self.totalToProcess = totalToProcess
    self.ext = 'mp4'; audioOrVideo = 'video'
    if isAudio:
      self.ext = 'mp3'; audioOrVideo = 'audio'
    self.commBase = LocalData.commDict[audioOrVideo]
  def issueCommand(self):
    fileExtLess = os.path.splitext(self.mediaFileFrom)[0]
    mpx = fileExtLess + '.' + self.ext
    if os.path.isfile(mpx):
      print mpx, 'exists. Jumping to next (if this one is not already the last one)...'
      return
    comm = self.commBase %{'mediaFile':self.mediaFileFrom, 'mpx':mpx}
    issueCommand(comm, self.totalToProcess)

seq = 0
def issueCommand(comm, total):
  global seq
  print '='*40
  seq += 1; print seq, 'of', total, '::', comm
  print '='*40
  os.system(comm)  

def batchConvertToEitherMp3or4(extensions=[], isAudio=False):
  if len(extensions) == 0:
    extensions = LocalData.EXTENSIONS_DEFAULT
  mediaFiles = []
  for ext in extensions:
    mediaFiles += glob.glob('*.%s' %ext)
  mediaFiles.sort(); total = len(mediaFiles)
  for mediaFileFrom in mediaFiles:
    mediaObj = Media(mediaFileFrom, total, isAudio)
    mediaObj.issueCommand()

def fetchExtensionArguments():
  isAudio = False
  extensions = []
  for ext in sys.argv[1:]:
    if ext.startswith('-a'):
      isAudio = True
      continue
    extensions.append(ext)
  return extensions, isAudio

def main():
  extensions, isAudio = fetchExtensionArguments()
  batchConvertToEitherMp3or4(extensions, isAudio)

if __name__ == '__main__':
  main()
