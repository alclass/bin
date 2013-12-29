#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, re, sys, time
'''
Explanation:  
  This script reads a list of YouTube Video Ids from a text file (default name is 'youtube-ids.txt')
  This file must have the 11-character video id starting each line. 
  (A "#" at the beginning of a line ignores that line.)
  
  Before starting download, a confirmation yes/no is asked in the shell-terminal. 

'''


from dlYouTubeMissingVideoIdsOnLocalDir import VideoIdsComparer # a class

class RepeatedFilesDeleter(object):
  '''
  This class models the processing of a find, confirm and download YouTube video ids.
  '''
  
  DEFAULT_TXT_FILE_WITH_NEW_FILENAMES = 'youtube-map-ids-to-titles.txt'
  MAX_N_TRIES = 3
  
  def __init__(self):
    self.map_id_to_filename_list = {}
    self.list_of_files_to_delete = []
    self.process()
    
  def process(self):
    self.init_map_id_to_filename_list()
    self.find_out_videoids_in_more_than_1_filename()
    self.please_confirm_batch_delete()
    self.batch_delete_one_by_one()

  def init_map_id_to_filename_list(self):
    '''
    '''
    files = glob.glob('*.webm')
    for filename in files:
      try:
        extensionless_name, extension = os.path.splitext(filename)
        videoid = extensionless_name[-11:]
        if videoid not in self.map_id_to_filename_list.keys():
          self.map_id_to_filename_list[videoid] = [filename]
          continue
        filenames = self.map_id_to_filename_list[videoid]
        filenames.append(filename)
      except IndexError:
        pass 

  def find_out_videoids_in_more_than_1_filename(self):
    total_ids_with_repeats = 0
    for videoid in self.map_id_to_filename_list.keys():
      filename_list = self.map_id_to_filename_list[videoid]
      if len(filename_list) > 1:
        total_ids_with_repeats += 1
        print total_ids_with_repeats, videoid, filename_list
        self.put_into_list_of_files_to_delete(videoid, filename_list)

  def put_into_list_of_files_to_delete(self, videoid, filename_list):
    if len(filename_list) > 2:
      raise IndexError, 'There are more than 1 repeat file to delete. Program cannot deal with that yet.'
    if len(filename_list[0]) < len(filename_list[1]):
      self.list_of_files_to_delete.append(filename_list[0])
    else:
      self.list_of_files_to_delete.append(filename_list[1])
  
  def please_confirm_batch_delete(self):
    '''
    To ask the user to confirm or not the download of all taken ids
    '''
    for i, filename in enumerate(self.list_of_files_to_delete):
      print i+1, 'To delete', filename
    print 'Total:', len(self.list_of_files_to_delete)
    ans = raw_input(' Y*/n (Obs: only "n" or "N" will stop renaming.) ')
    if ans in ['n', 'N']:
      sys.exit(0)
  
  def batch_delete_one_by_one(self):
    '''
    '''
    for i, filename in enumerate(self.list_of_files_to_delete):
      print i+1, 'Deleting', filename,
      os.remove(filename)
      print '[done]'

def process():
  RepeatedFilesDeleter()  

if __name__ == '__main__':
  process()
