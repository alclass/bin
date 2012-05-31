#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation

This script ...
'''
import glob, os

mp3s = glob.glob('*.mp3')
mp3s.sort()
def pickUpMp3OfLecture(lectureNStr):
  mp3sForLecture = []
  for mp3 in mp3s:
    if mp3.startswith(lectureNStr):
      mp3sForLecture.append(mp3)
  return mp3sForLecture

def mp3wrap(lectureN):
  lectureNStr = '%02d' %lectureN
  globStr = '%s*.mp3' %lectureNStr
  mp3sForLecture = pickUpMp3OfLecture(lectureNStr)
  name = mp3sForLecture[0]
  name = name [ len('01-1 ') : ]
  name = '%s %s' %(lectureNStr, name)
  comm = 'mp3wrap "%s" ' %name 
  for mp3 in mp3sForLecture:
    comm += '"%s" ' %mp3
  print '-'*30
  print comm
  os.system(comm)
    
def process():
  for lectureN in range(1, 36+1):
    mp3wrap(lectureN)

if __name__ == '__main__':
  process()

