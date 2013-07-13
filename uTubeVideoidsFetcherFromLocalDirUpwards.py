#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 05/jul/2013

@author: friend
'''

import os, sys # re #, time
binlibdir = '/home/friend/bin/'
sys.path.insert(0, binlibdir)
from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename



class OSWalkerForUTubeVideoIds(object):

  def __init__(self, abs_path = None):
    all_video_ids = []
    self.set_walk_upwards_root_path(abs_path)
    self.local_root_dir_upwards_walker()
    
  def set_walk_upwards_root_path(self, abs_path):
    if abs_path == None:
      self.local_root_abs_path = os.path.abspath('.')
    else:
      self.local_root_abs_path = abs_path
    
        
  def find_if_any_videoids_among_files(self):
    for filename in self.filenames:
      videoid = get_videoid_from_filename(filename)
      if videoid != None:
         #all_video_ids.append(videoid)
         print videoid
  
  def local_root_dir_upwards_walker(self):
    for dirpath, dirnames, self.filenames in os.walk(self.local_root_abs_path):
      videoids_found = self.find_if_any_videoids_among_files()  
        
if __name__ == '__main__':
  OSWalkerForUTubeVideoIds()
