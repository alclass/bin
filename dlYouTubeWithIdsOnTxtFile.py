#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, time
'''

This script downloads videoid inside a text file that are (yet) not present on the local folder.

The 3 steps below further explain the functionality of this script:
  
  1) This script reads a list of YouTube Video Ids from a text file (default name is 'youtube-ids.txt')
       This file must have the 11-character video id starting each line. 
       (A "#" at the beginning of a line ignores that line.)
  
  2) The video ids collected from 'youtube-ids.txt' (or a non-default file) are compared with the
       mp4s that have videoids ending the filename before the extension. If this videoid is already present,
       it is discarded.  If not present, it queues up to be downloaded.
  
  3) A confirmation yes/no for the download of the queued-up files, is asked in the shell-terminal,
     ie, download will only begin if the user doesn't say 'no' (n or N).

'''

from dlYouTubeMissingVideoIdsOnLocalDir import VideoIdsComparer # a class

class VideoidsGrabberAndDownloader(object):
  '''
  This class models the processing of a find, confirm and download YouTube video ids.
  '''
  
  DEFAULT_TXT_FILE = 'youtube-ids.txt'
  MAX_N_TRIES = 3
  
  def __init__(self, youtubeids_filename=None):
    self.set_youtubeids_filename(youtubeids_filename)
    self.process()

  def set_youtubeids_filename(self, youtubeids_filename=None):
    if youtubeids_filename == None or not os.path.isfile(youtubeids_filename):
      self.youtubeids_filename = self.DEFAULT_TXT_FILE
      return
    self.youtubeids_filename = youtubeids_filename
    
  def process(self):
    self.read_ids_from_txt_file()
    self.compare_ids_with_mp4s_already_on_localdir()
    self.please_confirm_download()
    self.download_videos_by_their_ids()
    
  def find_alternative(self):
    '''
    Not yet fully implemented
    '''
    files = os.listdir('.')
    print files
    idstr = 'id[=](.+)[.]'
    idstr_re = re.compile(idstr)
    vids = []
    for eachfile in files:
      matchObj = idstr_re.search(eachfile)
      if matchObj:
        vid = matchObj.group(1)
        if vid not in vids:
          print 'Found vid', vid
          vids.append(vid)

  def read_ids_from_txt_file(self):
    '''
    Take the YouTube video ids from a txt file, line by line and ids starting the 11 first characters.
    '''
    self.videoids_to_download = []
    lines=open(self.youtubeids_filename).readlines()
    vids_total = 0
    n_downloaded = 0
    for line in lines:
      try:
        if line[0]=='#':
          continue
        vid = line.rstrip('\n')
        if len(vid) < 11:
          continue
        if len(vid) > 11:
          vid = vid[:11]
        self.videoids_to_download.append(vid)
      except IndexError: # if line[0] above raises it in case line is empty
        pass

  def compare_ids_with_mp4s_already_on_localdir(self):
    video_comparer = VideoIdsComparer()
    mp4_ids_on_localdir = video_comparer.get_all_mp4_videoids_on_local_dir()
    new_video_ids = []
    for vid in self.videoids_to_download:
      if vid not in mp4_ids_on_localdir:
        new_video_ids.append(vid)
    self.videoids_to_download = new_video_ids

  def please_confirm_download(self):
    '''
    To ask the user to confirm or not the download of all taken ids
    '''
    print self.videoids_to_download
    print 'vids_total', len(self.videoids_to_download)
    ans = raw_input(' Y*/n ')
    if ans in ['n', 'N']:
      sys.exit(0)
  
  def download_videos_by_their_ids(self):
    '''
    Loop all video ids, issuing download one by one
    '''
    self.n_downloaded = 0
    for i, vid in enumerate(self.videoids_to_download):
      n_seq = i + 1
      self.issue_download(n_seq, vid)
        
  def issue_download(self, n_seq, vid):
    '''
    Proceed download of passed-on video id
    '''
    n_tries = 1
    while n_tries <= self.MAX_N_TRIES:
      print  n_seq, 'n.of dl. so far', self.n_downloaded, 'of', len(self.videoids_to_download), 'video', vid, 'n_tries', n_tries, '[%s]' %time.ctime()
      comm = 'youtube-dl -f 18 "http://www.youtube.com/?v=%s"' %vid
      print comm
      ret_val = os.system(comm)
      if ret_val == 0:
        self.n_downloaded += 1
        return
      print 'Problem with the download: waiting 3 min.'
      time.sleep(3*60)
      n_tries += 1
    print 'After', self.MAX_N_TRIES, 'tries, given up downloading', vid


def process():
  youtubeids_filename = None
  try:
    youtubeids_filename = sys.argv[1]
  except IndexError:
    pass
  VideoidsGrabberAndDownloader(youtubeids_filename)  

if __name__ == '__main__':
  process()
