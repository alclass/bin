#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
batchWalkFfmpegConvertDeux.py
Explanation:
  This script is a dir-walker that grabs media video files
  (defaulting to mp4; another extension should gitbe given as a cli-parameter),
  then calls batchFfmpegConvertDeux.py to convert them to mp3.

  In a sense, this script is a wrapper around batchFfmpegConvertDeux.py,
  giving it a disk tree wide capability to mp3-convert many files automatically.

  Written on 2015-01-06 Luiz Lewis
'''
import os

def main():
  basepath = os.path.abspath('.')
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk('.'):
    for dirname in dirnames:
      if dirname == 'mp3split':
        complement_path = dirpath
        if complement_path.startswith('./'):
          complement_path = complement_path[2:]
          current_path = os.path.join(basepath, complement_path + '/mp3split')
          walk_counter += 1
          os.chdir(current_path)
          print walk_counter, 'deleting mp3s in:', current_path
          os.system('rm *.mp3')
          os.chdir(basepath)

if __name__ == '__main__':
  main()
