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
import sys
import batchFfmpegConvertDeux as batchConverter

def process_folder(current_path, files_to_convert):
  print 'where am I:', os.path.curdir
  print 'current_path:', current_path
  isAudio=True
  batchConverter.batchConvertToMp3(files_to_convert)

def main():
  target_ext = 'mp4'
  extensions = []
  if len(sys.argv) > 1:
    target_ext = sys.argv[1]
    extensions = [target_ext]
  basepath = os.path.abspath('.')
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk('.'):
    complement_path = dirpath
    if complement_path.startswith('./'):
      complement_path = complement_path[2:]
    current_path = os.path.join(basepath, complement_path)
    walk_counter += 1
    print walk_counter, 'current path:', current_path
    files_to_convert = []
    for fichier in filenames:
      if fichier.endswith('.'+target_ext):
        files_to_convert.append(fichier)
    if len(files_to_convert) > 0:
      print 'FOUND @', complement_path
      for each in files_to_convert:
        print each
      os.chdir(current_path)
      process_folder(current_path, files_to_convert)
      os.chdir(basepath)
      print '='*40
      print 'Voltei!', dirpath, dirnames, current_path
      print '='*40



if __name__ == '__main__':
  main()
