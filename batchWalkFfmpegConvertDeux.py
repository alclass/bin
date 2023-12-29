#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batchWalkFfmpegConvertDeux.py
Explanation:
  This script is a dir-walker that grabs media video files
  (defaulting to mp4; another extension should gitbe given as a cli-parameter),
  then calls batchFfmpegConvertDeux.py to convert them to mp3.

  In a sense, this script is a wrapper around batchFfmpegConvertDeux.py,
  giving it a disk tree wide capability to mp3-convert many files automatically.

  Some improvements on 2015-01-06 Luiz Lewis
  A more-than-normal improvement, including the script_help_string composition,on 2015-01-16 Luiz Lewis
"""

script_help_string = '''
      This script converts audio or video to available formats using ffmpeg.
      It walks up the directory structure processing all media files that have required extensions (formats).

      Here follow the parameters that can be used via the command line:
      -a
        Switches conversion to audio-type (otherwise it try to convert a video to a diferent format)
        Conversion to audio is to a mp3 audio (sources can be video or a different than mp3 audio format)

      -te=extension_list
        te means "target extension". When typing the parameter, the extension must be separated by comma and spaces
        are not allowed.
        Example:
         -te=mp4,wmv
         -te=avi,mp4,wmv
         -te=mkv
        If not given, it defaults to only mp4
        These are invalid examples:
         -te=mp4, wmv (there is a blank-space there)
         -te=-a;mp4 (two mistakes, the -a, as parameter, should go alone and separation cannot be done by semicolon

      --process-only-narked-folders
        This parameter tells the program to only process directories that have a certain text mark in their names
        Example:  This mark: ' _i ' (including enclosing blanks) is used for some videocourses folder names.
        So, this mark can be used so that only those named folders will be processed
      -m="the marker string"
        This parameter should be within quotes and there should not be spaces after the = sign and before the first quotation mark
        If not given, it defaults to " _i " which is a sign (or mark) representing a videocourse in many courses which folder we name-conventioned
'''

import os
import sys
import batchFfmpegConvertDeux as batchConverter

DEFAULT_MARKER_ON_FOLDERNAME_ALLOWING_PROCESS = ' _i ' # this is a string-marker that every SabDir course has
MARKER_ON_FOLDERNAME_ALLOWING_PROCESS = None
ALLOW_PROCESS_ONLY_ON_MARKED_FOLDER = False
DEFAULT_TARGET_EXTENSION = 'mp4'
KNOWN_EXTENSIONS = ['avi', 'wmv', 'mp4', 'mkv', 'm4a', 'm4v']

isAudio = False
def process_folder(current_path, files_to_convert):
  if isAudio:
    batchConverter.batchConvertToMp3(files_to_convert)

def does_foldername_have_the_allow_process_mark(abs_dirpath):
  abs_dirpath = abs_dirpath.rstrip('/.')
  pp = abs_dirpath.split('/')
  try:
    on_dirname = pp[-1]
    if on_dirname.find(MARKER_ON_FOLDERNAME_ALLOWING_PROCESS) >= 0:
      return True
  except IndexError:
    pass
  return False

def is_folder_allowed_for_media_file_conversion(dirpath):
  if not ALLOW_PROCESS_ONLY_ON_MARKED_FOLDER:
    return  True
  return does_foldername_have_the_allow_process_mark(dirpath)

def get_args():
  global ALLOW_PROCESS_ONLY_ON_MARKED_FOLDER
  global MARKER_ON_FOLDERNAME_ALLOWING_PROCESS
  global isAudio
  target_extensions = []; extensions_to_verify = []
  was_help_displayed = False
  for arg in sys.argv:
    if arg == '-h' or arg=='--help':
      print(script_help_string)
      was_help_displayed = True
      return [], was_help_displayed
    elif arg == '--process-only-narked-folders':
      ALLOW_PROCESS_ONLY_ON_MARKED_FOLDER = True
    elif arg.startswith('-m='):
      MARKER_ON_FOLDERNAME_ALLOWING_PROCESS = arg[ len('-m=') : ]
    elif arg == '-a':
      isAudio = True
    elif arg.startswith('-te='):
      target_exts_str = arg[ len('-te=') : ]
      if target_exts_str.find(',') > -1:
        extensions_to_verify = target_exts_str.split(',')
  for extension in extensions_to_verify:
    if extension in KNOWN_EXTENSIONS:
      target_extensions.append(extension)
  if len(target_extensions) == 0:
    target_extensions = [DEFAULT_TARGET_EXTENSION]
  if MARKER_ON_FOLDERNAME_ALLOWING_PROCESS is None:
    MARKER_ON_FOLDERNAME_ALLOWING_PROCESS = DEFAULT_MARKER_ON_FOLDERNAME_ALLOWING_PROCESS
  print('isAudio =', isAudio)
  print('target_extensions = ', target_extensions)
  print('ALLOW_PROCESS_ONLY_ON_MARKED_FOLDER', ALLOW_PROCESS_ONLY_ON_MARKED_FOLDER)
  print('MARKER_ON_FOLDERNAME_ALLOWING_PROCESS', MARKER_ON_FOLDERNAME_ALLOWING_PROCESS)
  return target_extensions, was_help_displayed

def process_walk_updirtree(target_extensions):
  basepath = os.path.abspath('.')
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk('.'):
    complement_path = dirpath
    abs_dirpath = os.path.join(basepath, dirpath)
    if not is_folder_allowed_for_media_file_conversion(abs_dirpath):
      print('-'*10)
      print('Not converting dir', abs_dirpath, 'because it does not have the MARKER_ON_FOLDERNAME_ALLOWING_PROCESS =[%s]' %MARKER_ON_FOLDERNAME_ALLOWING_PROCESS)
      continue
    if complement_path.startswith('./'):
      complement_path = complement_path[2:]
    current_path = os.path.join(basepath, complement_path)
    walk_counter += 1
    print(walk_counter, 'current path:', current_path, 'number of filenames =', len(filenames))
    files_to_convert = []
    for filename in filenames:
      for target_extension in target_extensions:
        if filename.endswith('.'+target_extension):
          files_to_convert.append(filename)
    if len(files_to_convert) > 0:
      print('FOUND @', complement_path)
      for filename in files_to_convert:
        print(filename)
      os.chdir(current_path)
      process_folder(current_path, files_to_convert)
      os.chdir(basepath)
      print('-'*40)
      print('Voltei!', dirpath, dirnames, current_path)
      print('='*40)


def main():
  target_extensions, help_displayed = get_args()
  if help_displayed:
    return
  process_walk_updirtree(target_extensions)


if __name__ == '__main__':
  main()
