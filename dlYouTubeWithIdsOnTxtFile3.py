#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import sys
import local_settings as ls # local Python (bin) settings
sys.path.insert(0, ls.UTUBEAPP_PATH)
# from shellclients.dlYouTubeWithIdsOnTxtFile import VideoidsGrabberAndDownloader
from uTubeOurApps.shellclients.dlYouTubeWithIdsOnTxtFile import VideoidsGrabberAndDownloader

def process():
  youtubeids_filename = None
  try:
    youtubeids_filename = sys.argv[1]
  except IndexError:
    pass
  VideoidsGrabberAndDownloader(youtubeids_filename)  

if __name__ == '__main__':
  process()
