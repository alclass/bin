#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys, time

import __init__
#import  bin_local_settings as bls
#sys.path.insert(0, bls.UTUBEAPP_PATH)
import local_settings as ls # local Python (bin) settings
sys.path.insert(0, ls.UTUBEAPP_PATH)

#from shellclients import extractVideoidsFromATextFileMod as extract_script
import uTubeOurApps.shellclients.extractVideoidsFromATextFileMod as extract_script

def process():
  extract_script.process()

if __name__ == '__main__':
  process()
