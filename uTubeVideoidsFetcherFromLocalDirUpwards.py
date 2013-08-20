#!/usr/bin/env python
#-*-coding:utf-8-*-
'''

This script picks up all YouTube video ids on the local directory and downwards from it.
The video ids that can be found are those that end a filename before its extension.

Created on 05/jul/2013

@author: friend
'''

import os, sys # re #, time
binlibdir = '/home/friend/bin/'
sys.path.insert(0, binlibdir)
from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename



class OSWalkerForUTubeVideoIds(object):

  def __init__(self, abs_path = None):
    self.walker_counter = 0
    self.all_video_ids = []
    self.repeated_video_ids = []
    self.set_walk_upwards_root_path(abs_path)
    self.local_root_dir_upwards_walker()
    self.report_totals()
    
  def set_walk_upwards_root_path(self, abs_path):
    if abs_path == None:
      self.local_root_abs_path = os.path.abspath('.')
    else:
      self.local_root_abs_path = abs_path
    
  def form_path_to_print(self):
    path_to_print = self.dirpath
    if self.dirpath.startswith(self.local_root_abs_path): 
      path_to_print = self.dirpath[ len(self.local_root_abs_path) : ]
    return path_to_print 
    
  def find_if_any_videoids_among_files(self):
    path_to_print = self.form_path_to_print()
    for filename in self.filenames:
      videoid = get_videoid_from_filename(filename)
      if videoid != None:
         #all_video_ids.append(videoid)
         if videoid in self.all_video_ids:
           if videoid not in self.repeated_video_ids:
             self.repeated_video_ids.append(videoid)
           continue
         # videoid is not a repeat, append it, print it and move on
         self.all_video_ids.append(videoid)
         self.walker_counter += 1
         print self.walker_counter, videoid, path_to_print, filename
  
  def local_root_dir_upwards_walker(self):
    for self.dirpath, dirnames, self.filenames in os.walk(self.local_root_abs_path):
      videoids_found = self.find_if_any_videoids_among_files()  
        
  def report_totals(self):
    print 'Totals:'
    if len(self.repeated_video_ids) > 0: 
      print 'Repeated Videos', self.repeated_video_ids 
    print 'Total Repeated Videos', len(self.repeated_video_ids) 
    print 'Total Videos', len(self.all_video_ids)

if __name__ == '__main__':
  OSWalkerForUTubeVideoIds()
