#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys
'''
Explanation

'''
files = os.listdir('.')
print files
idstr = 'id[=](.+)[.]'
idstr_re = re.compile(idstr)
vids = []
for eachfile in files:
  matchObj = idstr_re.search(eachfile)
  if matchObj:
    vid = matchObj.group(1)
    if vid not in vids:
      print 'Found vid', vid
      vids.append(vid)
  
lines=open('youtube-ids.txt').readlines()
vids_total = 0
n_downloaded = 0
for line in lines:
  try:
    if line[0]=='#':
      continue
    vid = line.rstrip('\n')
    if len(vid) < 11:
      continue
    vids_total += 1
    if vid in vids:
      print  n_downloaded+1, '/', vids_total, 'video', vid, 'already exists. Continuing.'
      continue
    comm = 'youtube-dl -f 18 "http://www.youtube.com/?v=%s"' %vid
    print n_downloaded+1, '/', vids_total, comm
    ret_val = os.system(comm)
    if ret_val == 0:
      n_downloaded += 1
  except IndexError: # if line[0] above raises it in case line is empty
    pass


