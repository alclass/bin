#!/usr/bin/env python3
#-*-coding:utf-8-*-
'''
This script renames YouTube videos prefixing them with the 2-digit number
  that is the same as its ordered position in playlist.

Created on 03/jul/2018

@author: friend
'''
import glob, os, sys
from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename        

def doRename(mp4s, ids, doRenameThem=False):
  renametuplelist = [(0,0)]*len(mp4s)
  for mp4 in mp4s:
    if not os.path.isfile(mp4):
      print('File', mp4, 'not found. Skipping next...')
      continue
    videoid = get_videoid_from_filename(mp4)
    if videoid in ids:
      try:
        index = ids.index(videoid)
      except ValueError:
        print('yt-videoid', videoid, 'not found. Skipping next...')
        continue
      seqnumber = index + 1
      newName = str(seqnumber).zfill(2) + ' ' + mp4
      renametuplelist[index] = (mp4, newName)

  for i, tupl in enumerate(renametuplelist):
    seqNumber = i + 1
    currentName, newName = tupl
    print('Rename n.', seqNumber)
    print(' => ', currentName)
    print(' => ', newName)
    if doRenameThem:
      os.rename(currentName, newName)

  if doRenameThem is False:
    ans = input('Do rename files? [type in y or Y for Yes, anything else for No] ')
    if ans in ['y', 'Y']:
      doRename(mp4s, ids, doRenameThem=True)

def extract_ids():
  text = open(DEFAULT_YTPL_ORDER_TXT_IDS_FILE).read()
  if text is not None:
    ids = text.split('\n')
    if '' in ids:
      ids.remove('')
    return ids
  return []

DEFAULT_YTPL_ORDER_TXT_IDS_FILE = 'youtube-ids.txt'
def process():
  files = os.listdir('.')
  if DEFAULT_YTPL_ORDER_TXT_IDS_FILE not in files:
    print('File', DEFAULT_YTPL_ORDER_TXT_IDS_FILE, 'is missing on current folder. Script cannot proceed.')
    sys.exit(1)
  mp4s = glob.glob('*.mp4')
  ids = extract_ids()
  print('doRename with', len(mp4s), 'files and', len(ids), 'ids')
  doRename(mp4s, ids)
          
if __name__ == '__main__':
  process()
  
