#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''


  Written on 2015-01-12 Luiz Lewis
'''
import os
import sys
import shutil
import batchFfmpegConvertDeux as batchConverter

CONVENTIONED_MP3GENERATED_MARK_HIDDENFILE_NAME = '.mp3s_generated_do_not_regenerate_them'
# target_abs_basepath_DEFAULT = '/media/friend/SAMSUNG/TVJus mp3converted/Saber Direito mp3converted/'
extension_DEFAULT = 'mp3'

def walk_dirtree_and_cache_moveables(file_extension):
  move_queue = []
  if file_extension == None:
    raise ValueError, 'file_extension is missing'
  source_abs_basepath = os.path.abspath('.')
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk('.'):
    if 'mp3split' in dirpath:
      continue
    walk_counter += 1
    print walk_counter #, 'current path:', dirpath
    files_to_move = []
    for fichier in filenames:
      if fichier.endswith('.'+file_extension):
        files_to_move.append(fichier)
    if len(files_to_move) > 0:
      target_rel_path = dirpath
      #print 'FOUND %d files to move at [%s]' %(len(files_to_move), target_rel_path)
      move_queue.append({'target_rel_path':target_rel_path, 'files_to_move':files_to_move})
      #print '-'*40
  return move_queue, source_abs_basepath

def move_over_to_target_abs_path(move_queue, source_abs_basepath, target_abs_basepath):
  if source_abs_basepath == None:
    raise ValueError, 'source_abs_basepath is None'
  if target_abs_basepath == None:
    raise ValueError, 'target_abs_basepath is None'
  move_counter = 0
  for move_instance in move_queue:
    target_rel_path = move_instance['target_rel_path']
    print 'Target Rel. Path =', target_rel_path
    if target_rel_path.startswith('./'):
      target_rel_path = target_rel_path[2:]
    target_abs_dirpath = os.path.join(target_abs_basepath, target_rel_path)
    if not os.path.isdir(target_abs_dirpath):
      os.makedirs(target_abs_dirpath)
    print '-'*10
    files_to_move = move_instance['files_to_move']
    source_abs_dirpath = os.path.join(source_abs_basepath, target_rel_path)
    for file_to_move in files_to_move:
      source_abs_filepath = os.path.join(source_abs_dirpath, file_to_move)
      shutil.move(source_abs_filepath, target_abs_dirpath)
      # marker file
      marker_abs_filepath = os.path.join(source_abs_dirpath, CONVENTIONED_MP3GENERATED_MARK_HIDDENFILE_NAME)
      marker_file = open(marker_abs_filepath, 'w')
      marker_file.close()
      move_counter += 1
      print move_counter, 'Moved', file_to_move

def get_args():
  target_abs_basepath = None
  extension           = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[len('-e='):]
    elif arg.startswith('-t='):
      target_abs_basepath = arg[len('-t='):]
      if not os.path.isdir(target_abs_basepath):
        raise OSError, target_abs_basepath + ' is not a directory.'
  if target_abs_basepath == None:
    raise OSError, 'target_abs_basepath must be given as input.'
    # target_abs_basepath = target_abs_basepath_DEFAULT
  if extension == None:
    extension = extension_DEFAULT
  return extension, target_abs_basepath

def main():
  extension, target_abs_basepath = get_args()
  move_queue, source_abs_basepath = walk_dirtree_and_cache_moveables(extension)
  move_over_to_target_abs_path(move_queue, source_abs_basepath, target_abs_basepath)

if __name__ == '__main__':
  main()
