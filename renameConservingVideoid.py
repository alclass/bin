#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
'''
import glob, os, shutil, sys, time

class Renamer(object):
  
  DEFAULT_EXTENSION      = 'mp4'
  DEFAULT_NAMES_FILENAME = 'z-titles.txt'
  VIDEOID_CHARSIZE = 11
  
  def __init__(self, extension=None, names_filename=None):
    self.extension = None
    self.names_filename = None
    self.set_extension(extension)
    self.files = []
    self.rename_pairs = []
    self.set_names_filename(names_filename)
    self.process()

  def set_names_filename(self, names_filename=None):
    if names_filename == None:
      self.names_filename = self.DEFAULT_NAMES_FILENAME
      return
    self.names_filename = names_filename

  def set_extension(self, extension=None):
    if extension == None:
      extension = self.DEFAULT_EXTENSION
    self.extension = extension 

  def get_dot_extension(self):
    return '.%s' %self.extension
    
  def process(self):
    self.enlist_files_on_current_folder()
    self.grab_names_from_rename_file()
    self.do_rename()
    
  def enlist_files_on_current_folder(self):
    self.files = glob.glob('*%s' %self.get_dot_extension())
    self.files.sort()

  def get_filename_ending_charsize(self):
    return self.VIDEOID_CHARSIZE + len(self.get_dot_extension()) + 1
    
  def get_videoid_plus_ext_ending(self, filename):
    if len(filename) < self.get_filename_ending_charsize(): # 1 (-) + 11 (videoid) + 4 (.filename)
      return None
    if not filename.endswith('%s' %self.get_dot_extension()):
      return None
    retro_pos = self.get_filename_ending_charsize()
    if filename[-retro_pos] != '-': # it's -16 with .mp4, ie, it's = 11 + 4 + 1
      return None
    return filename[-retro_pos:]

  def grab_names_from_rename_file(self):
    lines = open(self.names_filename).readlines()
    for i, new_title in enumerate(lines):
      new_title = new_title.lstrip(' \t').rstrip(' \t\r\n')
      if new_title == '':
        continue
      try: # IndexError may happen here
        old_name = self.files[i]
      except IndexError:
        continue
      ending = self.get_videoid_plus_ext_ending(old_name)
      if ending == None:
        continue
      new_name = new_title + ending
      if new_name == old_name:
        continue
      rename_pair = (old_name, new_name)
      self.rename_pairs.append(rename_pair)

  def confirm_rename_pairs(self):
    print '='*40
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      print seq, 'Rename:'
      print 'FROM: >>>', rename_pair[0]
      print 'TO:   >>>', rename_pair[1]
    print '='*40
    ans = raw_input('Confirm the %d renames above (Y*/n)? ' %len(self.rename_pairs))
    if ans in ['n', 'N']:
      return False
    return True

  def do_rename(self):
    if not self.confirm_rename_pairs():
      print 'No files were renamed.'
      return
    for i, rename_pair in enumerate(self.rename_pairs):
      print i+1, 'Renaming', rename_pair[1], 'TO', rename_pair[1]
      os.rename(rename_pair[0], rename_pair[1])
    print '%d files were renamed.' %len(self.rename_pairs)

def show_help():
  print '''
  This script
  1) takes files with a certain extension (defaulted to mp4, use parameter [-e=ext])
  2) sorts them alphabetically
  3) reads the new titles in file [[ z-rename.txt ]]
  4) forms the new filenames using the new titles conserving the videoid plus the extension
  5) ask for renaming confirmation
  6) if confirmed (ie, if n or N is not pressed), rename will occur.
  '''

def process():
  if 'help' in sys.argv:
    show_help()
    return
  extension = None; names_filename = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[len('-e='):]
    if arg.startswith('-n='):
      names_filename = arg[len('-n='):]
  # print '-e=%s' %extension, '-n=%s' %names_filename
  Renamer(extension, names_filename)

if __name__ == '__main__':
  process()
