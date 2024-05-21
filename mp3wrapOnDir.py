#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation

This script ...
'''
import glob, os

mp3s = glob.glob('*.mp3')
mp3s.sort()

def mp3wrap(lectureN):
  lecturePrefix = 'Lecture %02d_' %lectureN
  globStr = '%s*.mp3' %lecturePrefix
  mp3sForLectureN = glob.glob(globStr)
  mp3sForLectureN.sort()
  name = '%02d.mp3' %lectureN
  comm = 'mp3wrap "%s" ' %name 
  for mp3 in mp3sForLectureN:
    comm += '"%s" ' %mp3
  print '-'*30
  print comm
  os.system(comm)

def process():
  for lectureN in range(1, 36+1):
    mp3wrap(lectureN)

if __name__ == '__main__':
  process()

