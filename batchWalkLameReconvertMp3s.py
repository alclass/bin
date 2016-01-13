#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
batchWalkLameReconvertMp3s.py
Explanation:
  This script is a dir-walker that runs lame in order to reconvert mp3s
  It has a parameter that allows for checking whether or not dirname has
    some text mark (a string piece) on it. If it has, mp3s in folder will
    be processed. If not, those mp3s, if any, won't be reconverted.

  To do:
    A check of bitrate and sample-frequency is in order to be implemented in the future.
    This is so that if the target file is already the source file, no processing
      is necessary.

  Written on 2015-01-13 Luiz Lewis
'''
import os
import sys
import batchFfmpegConvertDeux as batchConverter

def process_folder(current_path, files_to_convert):
  print 'current_path:', current_path
  for filename in files_to_convert:
    comm = 'lame --mp3input -b 32 --resample 22.50 "%(filename)s" "%(filename)s-32k.mp3"' %{'filename':filename}
    os.system(comm)
    print 'Rename', filename
    comm = 'mv "%(filename)s-32k.mp3" "%(filename)s"' %{'filename':filename}
    os.system(comm)

PROCESS_DIRNAME_WITH_THIS_STRPIECE = ' _i ' # this is a string-marker that every SabDir course has
def go_ahead_on_dirname_allowance_check(dirpath):
  pp = dirpath.split('/')
  try:
    on_dirname = pp[-1]
    if on_dirname.find(PROCESS_DIRNAME_WITH_THIS_STRPIECE) >= 0:
      return True
  except IndexError:
    pass
  return False

process_dirname_based_on_determined_strpiece = False
def check_param_process_dirname_based_on_determined_strpiece():
  for arg in sys.argv:
    if arg == '--process-on-strpiece':
      process_dirname_based_on_determined_strpiece = True
      return

def main():
  # check_param_process_dirname_based_on_determined_strpiece()
  process_dirname_based_on_determined_strpiece = True
  basepath = os.path.abspath('.')
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk('.'):
    complement_path = dirpath
    if process_dirname_based_on_determined_strpiece:
      if not go_ahead_on_dirname_allowance_check(dirpath):
        print 'Not converting dir', dirpath
        continue
    if complement_path.startswith('./'):
      complement_path = complement_path[2:]
    current_path = os.path.join(basepath, complement_path)
    walk_counter += 1
    print walk_counter, 'current path:', current_path
    files_to_convert = []
    for fichier in filenames:
      if fichier.endswith('.mp3'):
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
