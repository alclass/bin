#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

'''
import sys
import installed_apps_dirs as installed # local Python (bin) settings
sys.path.insert(0, installed.UTUBEAPP_PATH)
#from shellclients.dlYouTubeWithIdsOnTxtFile import VideoidsGrabberAndDownloader
# import uTubeOurApps.shellclients.dlYouTubeWithIdsOnTxtFile.VideoidsGrabberAndDownloader as VideoidsGrabberAndDownloader
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
