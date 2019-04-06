#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
'''
import glob, os #, shutil, sys, time
def prepare_pairs():
  pairs = []
  srts = glob.glob('*.srt')
  srts.sort()
  mp4s = glob.glob('*.mp4')
  mp4s.sort()
  for i, srt in enumerate(srts):
    newName, _ = os.path.splitext(srt)
    newName = newName + '.mp4'
    try:
      oldName = mp4s[i]
      print('Rename:')
      print('From:', oldName)
      print('To:  ', newName)
      tupl = (oldName, newName)
      pairs.append(tupl)
    except IndexError:
      continue
  return pairs

def renamePairs(pairs):
  renameCount = 0
  for tupl in pairs:
    oldName, newName = tupl
    os.rename(oldName, newName)
    renameCount += 1
  print('renameCount =', renameCount)

def process():
  pairs = prepare_pairs()
  ans = input('Rename them? (y/Y for Yes) => ')
  if ans in ['y', 'Y']:
    renamePairs(pairs)
  
if __name__ == '__main__':
  process()
