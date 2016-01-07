#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script dir-walks the TTC directory tree recording a md5sum file for files inside TTC courses folder
'''
#import os
import sys #, time

lambda_strip_linefeed_et_al = lambda x : x.rstrip(' \t\r\n')
class File1LinesNotInFile2Shower(object):
  
  def __init__(self, file1_abspath, file2_abspath):
    self.file1_abspath = file1_abspath
    self.file2_abspath = file2_abspath
    self.lines1 = []; self.lines2 = []
    self.lines_in_1_not_in_2 = []
  
  def go_find(self):
    self.load_lines()
    self.find_lines_in_file1_not_in_file2()
    
  def load_lines(self):
    self.lines1 = open(self.file1_abspath).readlines()
    self.lines1 = map(lambda_strip_linefeed_et_al, self.lines1)
    self.lines2 = open(self.file2_abspath).readlines()
    self.lines2 = map(lambda_strip_linefeed_et_al, self.lines2)
    self.lines2.sort()
    
  def find_lines_in_file1_not_in_file2(self):
    for line1 in self.lines1:
      if line1 not in self.lines2:
        #self.lines1_dict[line1]=1
        self.lines_in_1_not_in_2.append(line1)
  
  def show_lines_in_file1_not_in_file2(self):
    for line in self.lines_in_1_not_in_2:
      print line

def print_help_and_exit():
  print '''Usage:
  pickup_lines_in_1_not_in_2.py <file1> <file2>
  '''
  sys.exit(0)
    
def pickup_cli_args():
  try:
    filename_or_abspath1 = sys.argv[1]
    filename_or_abspath2 = sys.argv[2]
    #if __name__ != '__main__':
      #return None
    return filename_or_abspath1, filename_or_abspath2
  except IndexError:
    pass 
  print_help_and_exit()
    
def process():
  if '--help' in sys.argv:
    print_help_and_exit()
  filename_or_abspath1, filename_or_abspath2 = pickup_cli_args()
  shower = File1LinesNotInFile2Shower(filename_or_abspath1, filename_or_abspath2)
  shower.go_find()
  shower.show_lines_in_file1_not_in_file2()

if __name__ == '__main__':
  process()
  #unittest.main()
