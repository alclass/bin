#!/usr/bin/env python
"""
~/bin/batchWalkDeleteMp3split.py

Explanation:
  This script is a dir-walker that grabs media video files
  (defaulting to mp4; another extension should gitbe given as a cli-parameter),
  then calls batchFfmpegConvertDeux.py to convert them to mp3.

  In a sense, this script is a wrapper around batchFfmpegConvertDeux.py,
  giving it a disk tree wide capability to mp3-convert many files automatically.

  Written on 2015-01-06 Luiz Lewis
  Updated (to Python3) on 2024-02-20 Luiz Lewis
  # -*- coding: utf-8 -*-
"""
import os


def batch_walk_delete_mp3split():
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
          scrmsg = f"{walk_counter} deleting mp3s in: [{current_path}]"
          print(scrmsg)
          os.system('rm *.mp3')
          os.chdir(basepath)


def process():
  batch_walk_delete_mp3split()


if __name__ == '__main__':
  process()
