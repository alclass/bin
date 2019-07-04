#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob, os, re, sys, time

# import logging
# LOG_FILENAME = 'zlog-uTubeRenameIdsFilesAddingTheirTitles-%s.log' %(time.time())
# logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

'''
Explanation:  

  uTubeRenameAddBeforeDashVideoid.py
  This script add a string before the dash-videoid-dot-extension
  Example:  abc-videoid_123.mp4
	prompt>uTubeRenameAddBeforeDashVideoid.py -e=mp4 -s=" (add this) "
  Result:  abc (add this) -videoid_123.mp4
'''

YOUTUBE_VIDEOID_CHARSIZE = 11
DEFAULT_EXTENSION = 'mp4'
FORBIDDEN_CHARS_IN_VIDEOID = \
  ['!', '@', '#', '$', '¨', '&', '%', '*', '(', ')', '[', ']', '{', '}',
   '+', '=', ';', ',', ';', '?', '<', '>',
   ]
DLD_COMM_TEMPLATE = 'youtube-dl --write-auto-sub --sub-lang en --skip-download https://www.youtube.com/watch?v=%s'

lambda_forbidden_chars = lambda c : c not in FORBIDDEN_CHARS_IN_VIDEOID
def pass_ytvideoid_thru_probable_filter(supposed_videoid):
  return list(filter(lambda_forbidden_chars, supposed_videoid))

def extract_video_id(filename):
  name, extension = os.path.splitext(filename)
  if len(name) < YOUTUBE_VIDEOID_CHARSIZE + 2: # if 'title-name' has at least 1 char plus '-' (dash)
    return None
  supposed_videoid = name[ -YOUTUBE_VIDEOID_CHARSIZE : ]
  filtered_supposed_videoid = pass_ytvideoid_thru_probable_filter(supposed_videoid)
  # print ('filtered', filtered_supposed_videoid)
  if len(supposed_videoid) == len(filtered_supposed_videoid):
    return supposed_videoid
  else:
    return None

class SubtitleProcessor:

  def __init__(self, extension=DEFAULT_EXTENSION):
    self.extension = extension
    sorted(self.extension)
    self.videoids = []
    self.subtitleurls_dict = {}
    self.filenames_dict = {}
    self.process()

  def gather_videoids(self):
    '''

    :return:
    '''
    files = glob.glob('*.'+self.extension)
    for eachFile in files:
      videoid = extract_video_id(eachFile)
      if videoid is None:
        continue
      self.filenames_dict[videoid] = eachFile
      self.videoids.append(videoid)

  def form_dld_comm_list(self):
    for videoid in self.videoids:
      dld_comm = DLD_COMM_TEMPLATE %videoid
      self.subtitleurls_dict[videoid] = dld_comm

  def printout_dld_commands(self):
    for videoid in self.subtitleurls_dict:
      print (videoid, '=>', self.subtitleurls_dict[videoid])

  def download_subtitles(self):
    for videoid in self.subtitleurls_dict:
      comm = self.subtitleurls_dict[videoid]
      print (videoid, ' => downloading =>', comm)
      os.system(comm)

  def rename_subtitles(self):
    files = glob.glob('*.'+'.vtt')
    for eachSubtitle in files:
      videoid = extract_video_id(eachSubtitle)
      if videoid is None:
        continue
      media_filename = self.filenames_dict[videoid]
      extensionless_media_name, _ = os.path.splitext(media_filename)
      _, subtitle_ext = os.path.splitext(eachSubtitle)
      newSubtitleName = media_filename + '.' + subtitle_ext
      print ('rename')
      print ('from', eachSubtitle)
      print ('to', newSubtitleName)

  def process(self):
    '''
    Process chain here:

    1) gather the videoids from current folder
    2) form the subtitle urls (iterate thru each videoid)
    3) download each subtitle
    4) check each file downloaded and rename it accordingly

    :return:
    '''
    self.gather_videoids()
    self.form_dld_comm_list()
    self.printout_dld_commands()
    ans = input('Accept the above retrievals? (y/N) ')
    if ans in ['y','Y']:
      # self.download_subtitles()
      pass
    else:
      return None
    print ('Renames =====>>>>>>>>>>>>')
    self.rename_subtitles()


def test_ids():
  names = [
    "09 23' Documentário - A indústria da delação premiada na Lava Jato-NHAxHyz3-dQ.mp4",
    "3 28' Login & Access Control-QEMtSUxtUDY.mp4",
    "Vue Vixens Workshop-7-tcLvyaEBM.mp4",
  ]
  for filename in names:
    print ( extract_video_id(filename) )


if __name__ == '__main__':
  #test_ids()
  SubtitleProcessor()
