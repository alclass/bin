#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import sys
import bin_local_settings as bls # local bin settings
sys.path.insert(0, bls.UTUBEAPP_PATH)
from shellclients.dlYouTubeWithIdsOnTxtFile import VideoidsGrabberAndDownloader 

def process():
  youtubeids_filename = None
  try:
    youtubeids_filename = sys.argv[1]
  except IndexError:
    pass
  VideoidsGrabberAndDownloader(youtubeids_filename)  

if __name__ == '__main__':
  process()
