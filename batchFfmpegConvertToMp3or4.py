#!/usr/bin/env python3
"""
Explanation
bin/batchFfmpegConvertToMp3or4.py

TO-DO/OBS:
  this script has its upgrading to Python3 started but yet not finished.

  Batch-converts * video or audio files to audio mp3's.
    (* ie converts files -- as manay there are -- in a directory)

# -*- coding: utf-8 -*-
"""
import glob
import os
import sys


class LocalData:
  comm_dict = {
    'audio' : 'avconv -i "%(mediaFile)s" -acodec libmp3lame "%(mpx)s"',
    'video' : 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mpx)s"'
  }
  EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mkv', 'mov', 'wmv']


class Media:
 
  def __init__(
      self, media_file_from, total_to_process, is_audio=False, extensions=None,
  ):
    self.media_files = []
    self.seq = 0
    self.total = 0
    self.media_filefrom  = mediaFileFrom
    self.total_to_process = totalToProcess
    self.ext = 'mp4'
    audio_or_video = 'video'
    self.extensions = [] if extensions is None else extensions
    if len(extensions) == 0:
      self.extensions = LocalData.EXTENSIONS_DEFAULT
    if is_audio:
      self.ext = 'mp3'
      audio_or_video = 'audio'
    self.comm_base = LocalData.commDict[audio_or_video]

  def issue_command(self):
    file_ext_less = os.path.splitext(self.mediaFileFrom)[0]
    mpx = file_ext_less + '.' + self.ext
    if os.path.isfile(mpx):
      scrmsg = f"{mpx} exists. Jumping to next (if this one is not already the last one)..."
      print(scrmsg) 
      return
    comm = self.commBase % {'mediaFile':self.media_filefrom, 'mpx':mpx}
    issueCommand(comm, self.totalToProcess)


class CommIssuer:

  def __init__(self):
    pass

  def batch_convert_to_either_mp3or4(self):
    self.media_files = []
    for ext in self.extensions:
      self.media_files += glob.glob('*.%s' % ext)
    self.media_files.sort()
    self.total = len(self.media_files)
    for mediaFileFrom in self.media_files:
      self.media_obj = Media(mediaFileFrom, total, isAudio)
      self.issue_command()

  def issue_command(self, comm):
    """
    TO-DO: this formulation with two classes need correctio
    :param comm:
    :return:
    """
    print('='*40)
    self.seq += 1
    print(self.seq, 'of', self.total, '::', comm)
    print('='*40)
    os.system(comm)  


def fetch_extension_arguments():
  is_audio = False
  extensions = []
  for ext in sys.argv[1:]:
    if ext.startswith('-a'):
      is_audio = True
      continue
    extensions.append(ext)
  return extensions, is_audio


def process():
  extensions, is_audio = fetchExtensionArguments()
  batchConvertToEitherMp3or4(extensions, is_audio)


if __name__ == '__main__':
  process()
