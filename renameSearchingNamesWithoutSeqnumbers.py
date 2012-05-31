#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script...
'''
import glob, os

def line_filter(line):
  if line.endswith('\n'):
    return line[ : -1]
  return line

def filter_lines(lines):
  outlines = []
  for line in lines:
    outlines.append(line_filter(line))
  return outlines

def generate_rename_pairs():
  mp3s = glob.glob('*.mp3')
  lines = open('course-titles.txt').readlines()
  lines = filter_lines(lines); seq = 0
  tupleRenameList = []
  for mp3 in mp3s:
    title = mp3 [ :  -len('.mp3')]
    if title in lines:
      index = lines.index(title)
      lecture_number = index + 1
      seq += 1
      newFilename = '%02d %s.mp3' %(lecture_number, title)
      tupleRenameList.append((mp3, newFilename))
  return tupleRenameList

def rename_pairs(tupleRenameList, doRename=False):
  seq = 0
  for tupleRename in tupleRenameList:
    oldFilename, newFilename = tupleRename
    seq += 1
    print 'Rename', seq
    print 'From:', oldFilename  
    print 'To:', newFilename
    if doRename:
      os.rename(oldFilename, newFilename)
      print 'renamed'
  if not doRename:
    ans = raw_input(' Rename them above (y or n) ? ')
    if ans in ['Y', 'y']:
      rename_pairs(tupleRenameList, doRename=True)

def process():
  tupleRenameList = generate_rename_pairs()
  rename_pairs(tupleRenameList, doRename=False)
  
if __name__ == '__main__':
  process()
