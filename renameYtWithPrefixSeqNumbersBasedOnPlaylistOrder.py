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
  renametuplelist = []; usedfilenames = []
  n_to_align_left_zeroes = len(str(len(ids))) # another option is to encapsulate a function that uses math.log10()
  for mp4 in mp4s:
    if not os.path.isfile(mp4):
      print('File', mp4, 'not found having an equivalent in ids. Skipping to next one if any...')
      continue
    videoid = get_videoid_from_filename(mp4)
    if not videoid in ids:
      print('File', mp4, 'not found having an equivalent in ids. Skipping to next one if any...')
      continue
    try:
      index = ids.index(videoid)
    except ValueError:
      print('yt-videoid', videoid, 'not found. Skipping next...')
      # this is logically not possible due to previous 'if' (a re-raise is a TODO here)
      raise ValueError
    seqnumber = index + 1
    newName = str(seqnumber).zfill(n_to_align_left_zeroes) + ' ' + mp4
    if mp4 not in usedfilenames:
      renametuplelist.append((mp4, newName))
      usedfilenames.append(mp4)

  nOfRenames = 0
  for i, tupl in enumerate(renametuplelist):
    seqNumber = i + 1
    currentName, newName = tupl
    print('Rename n.', seqNumber)
    print(' => ', currentName)
    print(' => ', newName)
    if doRenameThem:
      os.rename(currentName, newName)
      nOfRenames += 1

  print('doRename with', len(renametuplelist), 'files and', len(ids), 'ids')

  if doRenameThem is True:
      print('nOfRenames = ', nOfRenames) 

  else:  # ie if doRenameThem is False:
    ans = input('Do rename files? [type in y or Y for Yes, anything else for No] ')
    if ans in ['y', 'Y']:
      doRename(mp4s, ids, doRenameThem=True)

charSize = lambda idword: len(idword) == 11 # this lambda is intended to be used in a 'filter', each element is filtered-in if lambda returns True for it (filterOutNon11Char will used this later below)
wordStrip = lambda idword : idword.strip()
def extract_ids():
  text = open(DEFAULT_YTPL_ORDER_TXT_IDS_FILE).read()
  if text is not None:
    ids = text.split('\n')
    stripMap = map(wordStrip, ids)
    ids = [i for i in stripMap]
    filterOutNon11Char = filter(charSize, ids) # only 11-char idwords are allowed, '', '\n' etc. are filtered out
    ids = [i for i in filterOutNon11Char]
    return ids
  return [] # if it has not returned above, text is None

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
