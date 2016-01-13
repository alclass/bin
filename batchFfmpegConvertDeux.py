#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
'''
import glob
import os
import sys

bitrate_in_kbps_DEFAULT        = 32  # ie, 32 kbps (kilobits per second the bitrate)
resampling_freq_in_khz_DEFAULT = 22.05  # ie, 22 kHz (kiloHertz the sampling frequency)

class LocalData:
  commDict = {'audio' : 'ffmpeg  -i "%(mediaFile)s" -acodec libmp3lame -b:a %(bitrate_in_kbps)dk -ar %(resampling_freq_in_khz)fk "%(mpx)s"', \
              'video' : 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mpx)s"'}
  EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mkv', 'mov', 'wmv']
 
class Media:
  def __init__(self, mediaFileFrom, totalToProcess, isAudio=False):
    self.mediaFileFrom  = mediaFileFrom
    self.totalToProcess = totalToProcess
    self.ext = 'mp4'; audioOrVideo = 'video'
    self.bitrate_in_kbps        = bitrate_in_kbps_DEFAULT
    self.resampling_freq_in_khz = resampling_freq_in_khz_DEFAULT
    if isAudio:
      self.ext = 'mp3'; audioOrVideo = 'audio'
    self.commBase = LocalData.commDict[audioOrVideo]
  def set_bitrate_in_kbps(self, bitrate_in_kbps):
    if bitrate_in_kbps < 16 or bitrate_in_kbps > 256:
      return
    self.bitrate_in_kbps = int(bitrate_in_kbps)
  def set_resampling_freq_in_khz(self, resampling_freq_in_khz):
    if resampling_freq_in_khz < 22 or resampling_freq_in_khz > 44:
      return
    self.resampling_freq_in_khz = float(resampling_freq_in_khz)
  def issueCommand(self):
    fileExtLess = os.path.splitext(self.mediaFileFrom)[0]
    mpx = fileExtLess + '.' + self.ext
    if os.path.isfile(mpx):
      print mpx, 'exists. Jumping to next (if this one is not already the last one)...'
      return
    comm = self.commBase %{'mediaFile':self.mediaFileFrom, 'bitrate_in_kbps':self.bitrate_in_kbps, 'resampling_freq_in_khz':self.resampling_freq_in_khz, 'mpx':mpx}
    issueCommand(comm, self.totalToProcess)

seq = 0
def issueCommand(comm, total):
  global seq
  print '='*40
  seq += 1; print seq, 'of', total, '::', comm
  print '='*40
  os.system(comm)  

def batchConvertToEitherMp3or4(extensions=[], isAudio=False, bitrate_in_kbps=None, resampling_freq_in_khz=None):
  if len(extensions) == 0:
    extensions = LocalData.EXTENSIONS_DEFAULT
  mediaFiles = []
  for ext in extensions:
    mediaFiles += glob.glob('*.%s' %ext)
  mediaFiles.sort(); total = len(mediaFiles)
  for mediaFileFrom in mediaFiles:
    mediaObj = Media(mediaFileFrom, total, isAudio)
    if bitrate_in_kbps != None:
      print 'bitrate_in_kbps', bitrate_in_kbps
      mediaObj.set_bitrate_in_kbps(bitrate_in_kbps)
    if resampling_freq_in_khz != None:
      print 'resampling_freq_in_khz', resampling_freq_in_khz
      mediaObj.set_resampling_freq_in_khz(resampling_freq_in_khz)
    mediaObj.issueCommand()

def batchConvertToMp3(files_to_convert):
  '''
  :param files_to_convert: media video filenames that will be mp3-converted
  :return:void

   This method/function was programmed to suit an external call,
   from another scripting, receiving a list (files_to_convert) of
   media video files to be mp3-converted.

   The first "client" called is batchWalkFfmpegConvertDeux.py
   Added on 2015-01-06 Luiz Lewis
  '''
  total = len(files_to_convert)
  for mediaFileFrom in files_to_convert:
    isAudio = True
    mediaObj = Media(mediaFileFrom, total, isAudio)
    mediaObj.issueCommand()

def fetchExtensionArguments():
  isAudio = False
  extensions = []
  bitrate_in_kbps = None
  resampling_freq_in_khz = None
  for arg in sys.argv[1:]:
    if arg.startswith('-a'):
      isAudio = True
      continue
    elif arg.startswith('-b='):
      bitrate_in_kbps = int( arg[ len('-b=') : ] )
      continue
    elif arg.startswith('-s='):
      resampling_freq_in_khz = float( arg[ len('-s=') : ] )
      continue
    extensions.append(arg)
  return extensions, isAudio, bitrate_in_kbps, resampling_freq_in_khz

def main():
  extensions, isAudio, bitrate_in_kbps, resampling_freq_in_khz = fetchExtensionArguments()
  batchConvertToEitherMp3or4(extensions, isAudio, bitrate_in_kbps, resampling_freq_in_khz)

if __name__ == '__main__':
  main()
