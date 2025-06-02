#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation

'''

import os

class RenamePair:

  def __init__(self):
    self.rename_pairs = []
    self.current_dir_abspath = None
    
  def set_rename_pair_with_a_tuple_list(self, tuple_list):
    self.rename_pairs = tuple_list

  def set_rename_pair_with_a_dict(self, a_dict):
    self.rename_pairs = []
    for each_key in a_dict.keys():
      self.rename_pairs.append((each_key, a_dict[each_key])

  def set_current_dir_abspath(self, current_dir_abspath):
    if os.path.isdir(current_dir_abspath):
      self.current_dir_abspath = current_dir_abspath
    else:
      error_msg = 'dir %s does not exist.' %current_dir_abspath
      raise OSError, error_msg 
    
  def self.get_abspath_str(self):
    if self.current_dir_abspath == None:
      return '<current folder>'
    else:
      return self.current_dir_abspath 
        
  def adjust_old_and_new_names_with_abspath_if_needed(self):
    if self.current_dir_abspath == None:
      self.old_name_abspath = self.old_name
      self.new_name_abspath = self.new_name
    else:
      self.old_name_abspath = os.path.join(self.current_dir_abspath, self.old_name)
      self.new_name_abspath = os.path.join(self.current_dir_abspath, self.new_name)

  def rename(self, doRename=False):
    seq = 0
    for rename_pair in self.rename_pairs:
      self.old_name = rename_pair[0]
      self.new_name = rename_pair[1]
      self.adjust_old_and_new_names_with_abspath_if_needed()
      if os.path.isfile(self.old_name_abspath):
        if os.path.isfile(self.new_name_abspath):
          error_msg = 'Cannot rename, target [%s] exists.' %self.new_name_abspath
          raise OSError, error_msg
        seq += 1
        print seq,
        if not doRename:
          print ' About to rename (on %s):' %self.get_abspath_str()
        else:
          print ' Now renaming (on %s):' %self.get_abspath_str()
        print 'From >>>', self.old_name
        print 'To   >>>', self.new_name
        if doRename:
          os.rename(self.old_name_abspath, self.new_name_abspath)
          self.n_of_renames += 1
    if doRename:
      print 'Finished. Nº of renames =', self.n_of_renames
      return
    if seq > 0:
      print 'Rename the', seq, 'files above ?'
      ans = raw_input (' (y/n) ' )
      if ans.lower() == 'y':
        self.rename(doRename=True)
    else:
      print 'Nothing to rename.'


class RedHatCloudYoutubeVideosRename:

  def __init__(self):
    self.filenames=[]
    self.titles=[]
    self.n_of_renames = 0
    self.process_flow()

  def process_flow(self):
    self.fetchNames()
    self.renameTupleList = zip(self.filenames, self.titles)
    rename_pair = RenamePair()
    rename_pair.set_rename_pair_by_tuple_list()
  
  def fetchNames(self):
    lines = open('z-info2.txt').readlines()
    seq = 0
    for line in lines:
      line = line.strip(' \n')
      if seq % 2 == 0:
        self.titles.append(line) 
      else:
        self.filenames.append(line) 
      seq += 1
  

def process():
  RedHatCloudYoutubeVideosRename()
  
if __name__ == '__main__':
  process()
