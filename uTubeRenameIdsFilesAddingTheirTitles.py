#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, re, sys, time

# import logging
# LOG_FILENAME = 'zlog-uTubeRenameIdsFilesAddingTheirTitles-%s.log' %(time.time())
# logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

'''
Explanation:  

  This script contains the Renamer class
  That models the processing of renaming YouTube videofiles 
  from id-only filenames to title-and-id filenames.
'''

class Renamer(object):
  '''
  This class models the processing of renaming YouTube videofiles 
  from id-only filenames to title-and-id filenames.
  '''
  
  DEFAULT_TXT_FILE_WITH_NEW_FILENAMES = 'youtube-map-ids-to-titles.txt'
  
  def __init__(self):
    self.youtube_target_filenames_with_title_plus_id = self.DEFAULT_TXT_FILE_WITH_NEW_FILENAMES
    self.process()
    
  def process(self):
    self.init_map_current_ids_to_filenames()
    self.init_to_be_map_of_ids_with_newfilenames()
    self.find_those_with_equal_ids_and_fill_in_rename_dict()
    self.please_confirm_batch_rename()
    self.batch_rename_one_by_one()
    
  def init_map_current_ids_to_filenames(self):
    '''
      Initialize dict self.map_current_ids_to_filenames
    '''
    self.map_current_ids_to_filenames = {} 
    files = glob.glob('*.webm')
    for filename in files:
      video_id, extension = os.path.splitext(filename)
      if len(video_id) != 11: # extension.lower() != '.webm' or
        continue
      self.map_current_ids_to_filenames[video_id] = filename
    print 'Found', len(self.map_current_ids_to_filenames), 'webm video files.'
    #logging.info(self.map_current_ids_to_filenames)

  def init_to_be_map_of_ids_with_newfilenames(self):
    '''
      Initialize dict self.map_ids_to_newfilenames
    '''
    self.map_ids_to_newfilenames = {} 
    lines=open(self.youtube_target_filenames_with_title_plus_id).readlines()
    for filename in lines:
      try:
        if filename.endswith('\n'):
          filename = filename.rstrip('\n')
          title_and_id, extension = os.path.splitext(filename)
          if extension != '.mp4':
            continue
          title_and_dash = title_and_id[:-11]
          if not title_and_dash.endswith('-'):
            continue
          video_id = title_and_id[-11:]
          self.map_ids_to_newfilenames[video_id] = title_and_dash
      except IndexError:
        pass 
    print 'Found', len(self.map_ids_to_newfilenames), 'videofiles candidate to rename local id files.'
    #logging.info(self.map_ids_to_newfilenames)

  def find_those_with_equal_ids_and_fill_in_rename_dict(self):
    '''
      Pick up equal ids in:
        dict self.map_current_ids_to_filenames and
        dict self.map_ids_to_newfilenames
      Fill in self.rename_dict having the videoid keying its rename-pair 
    '''
    self.rename_dict = {}
    for videoid in self.map_ids_to_newfilenames.keys():
      if videoid not in self.map_current_ids_to_filenames.keys():
        continue
      oldname = self.map_current_ids_to_filenames[videoid]
      newname = self.map_ids_to_newfilenames[videoid] + oldname
      self.rename_dict[videoid] = (oldname, newname)
    print 'Found', len(self.rename_dict), 'filenames to rename.'

  def please_confirm_batch_rename(self):
    '''
      To ask the user to confirm the renaming
    '''
    total_to_rename = len(self.rename_dict)
    for i, videoid in enumerate(self.rename_dict.keys()):
      n_seq_to_rename = i+1
      print n_seq_to_rename, 'of', total_to_rename, '==>>', videoid
      rename_tuple = self.rename_dict[videoid]
      oldname = rename_tuple[0] 
      newname = rename_tuple[1]
      print '[from:]', oldname 
      print '[to:]',   newname
    print 'Total of videofiles to rename:', total_to_rename
    ans = raw_input(' Y*/n (Obs: only "n" or "N" will stop renaming.) ')
    if ans in ['n', 'N']:
      sys.exit(0)
  
  def batch_rename_one_by_one(self):
    '''
      Loop all video ids, renaming oldname to newname
    '''
    self.n_renamed = 0
    for videoid in self.rename_dict.keys():
      oldname, newname = self.rename_dict[videoid]
      print self.n_renamed + 1, 'Renaming [%s] TO [%s]' %(oldname, newname),
      os.rename(oldname, newname)
      print '[done]'
      self.n_renamed += 1

def process():
  Renamer()  

if __name__ == '__main__':
  process()
