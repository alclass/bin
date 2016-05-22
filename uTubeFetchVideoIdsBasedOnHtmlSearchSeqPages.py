#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script forms file youtube-ids.txt which is input for a second script that reuses youtube-dl and download the youtube videos by their id's, one at a time
'''
import glob, os, sys
import bin_local_settings as bls
sys.path.insert(0, os.path.abspath(bls.UTUBEAPP_PATH))
import uTubeOurApps.shellclients.uTubeFetchVideoIdsBasedOnHtmlSearchSeqPages as ytvidsFetcher

def process():
  ytvidsFetcher.process()

if __name__ == '__main__':
  process()
