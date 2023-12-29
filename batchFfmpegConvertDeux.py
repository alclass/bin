#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batchFfmpegConvertDeux.py
  Explanation
"""
import glob
import os
import sys

bitrate_in_kbps_DEFAULT = 32  # ie, 32 kbps (kilobits per second the bitrate)
resampling_freq_in_khz_DEFAULT = 22.05  # ie, 22 kHz (kiloHertz the sampling frequency)


class LocalData:
  commDict = {
    'audio': 'ffmpeg  -i "%(mediaFile)s" -acodec libmp3lame -b:a %(bitrate_in_kbps)dk'
    ' -ar %(resampling_freq_in_khz)fk "%(mpx)s"',
    'video': 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mpx)s"'
  }
  EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mkv', 'mov', 'wmv']


class Media:
  def __init__(self, media_file_from, total_to_process, is_audio=False):
    self.media_file_from = media_file_from
    self.total_to_process = total_to_process
    self.ext, audio_or_video = 'mp4', 'video'
    self.bitrate_in_kbps = bitrate_in_kbps_DEFAULT
    self.resampling_freq_in_khz = resampling_freq_in_khz_DEFAULT
    if is_audio:
      self.ext, audio_or_video = 'mp3', 'audio'
    self.comm_base = LocalData.commDict[audio_or_video]

  def set_bitrate_in_kbps(self, bitrate_in_kbps):
    if bitrate_in_kbps < 16 or bitrate_in_kbps > 256:
      return
    self.bitrate_in_kbps = int(bitrate_in_kbps)

  def set_resampling_freq_in_khz(self, resampling_freq_in_khz):
    if resampling_freq_in_khz < 22 or resampling_freq_in_khz > 44:
      return
    self.resampling_freq_in_khz = float(resampling_freq_in_khz)

  def issue_command(self):
    file_ext_less = os.path.splitext(self.media_file_from)[0]
    mpx = file_ext_less + '.' + self.ext
    if os.path.isfile(mpx):
      print(mpx, 'exists. Jumping to next (if this one is not already the last one)...')
      return
    comm = self.comm_base % {
      'mediaFile': self.media_file_from, 'bitrate_in_kbps': self.bitrate_in_kbps,
      'resampling_freq_in_khz': self.resampling_freq_in_khz, 'mpx': mpx
    }
    issue_command(comm, self.total_to_process)


seq = 0


def issue_command(comm, total):
  global seq
  print('='*40)
  seq += 1
  print(seq, 'of', total, '::', comm)
  print('='*40)
  os.system(comm)  


def batch_convert_to_either_mp3or4(
    extensions=None, is_audio=False, bitrate_in_kbps=None, resampling_freq_in_khz=None
):
  extensions = [] if extensions is None else extensions
  if len(extensions) == 0:
    extensions = LocalData.EXTENSIONS_DEFAULT
  media_files = []
  for ext in extensions:
    media_files += glob.glob('*.%s' % ext)
  media_files.sort()
  total = len(media_files)
  for mediaFileFrom in media_files:
    media_obj = Media(mediaFileFrom, total, is_audio)
    if bitrate_in_kbps is not None:
      print('bitrate_in_kbps', bitrate_in_kbps)
      media_obj.set_bitrate_in_kbps(bitrate_in_kbps)
    if resampling_freq_in_khz is not None:
      print('resampling_freq_in_khz', resampling_freq_in_khz)
      media_obj.set_resampling_freq_in_khz(resampling_freq_in_khz)
    media_obj.issue_command()


def batch_convert_to_mp3(files_to_convert):
  """
  :param files_to_convert: media video filenames that will be mp3-converted
  :return:void

   This method/function was programmed to suit an external call,
   from another scripting, receiving a list (files_to_convert) of
   media video files to be mp3-converted.

   The first "client" called is batchWalkFfmpegConvertDeux.py
   Added on 2015-01-06 Luiz Lewis
  """
  total = len(files_to_convert)
  for mediaFileFrom in files_to_convert:
    is_audio = True
    media_obj = Media(mediaFileFrom, total, is_audio)
    media_obj.issueCommand()


def fetch_extension_arguments():
  is_audio = False
  extensions = []
  bitrate_in_kbps = None
  resampling_freq_in_khz = None
  for arg in sys.argv[1:]:
    if arg.startswith('-a'):
      is_audio = True
      continue
    elif arg.startswith('-b='):
      bitrate_in_kbps = int(arg[len('-b='):])
      continue
    elif arg.startswith('-s='):
      resampling_freq_in_khz = float(arg[len('-s='):])
      continue
    extensions.append(arg)
  return extensions, is_audio, bitrate_in_kbps, resampling_freq_in_khz


def main():
  extensions, is_audio, bitrate_in_kbps, resampling_freq_in_khz = fetch_extension_arguments()
  batch_convert_to_either_mp3or4(extensions, is_audio, bitrate_in_kbps, resampling_freq_in_khz)


if __name__ == '__main__':
  main()
