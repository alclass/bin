#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pyMirrorFileSystemByHashComm.py (former batchWalkHashingFilesToRootFolderSqliteDB.py)
Explanation:
  This script walks all files and folders up the directory tree.
  As it encounters files it sha1-hashes them and store sha1hex on a database.
  As for now, this database is a SQLite file staged on the device's root folder.

  In a nutshell, it keeps a database of hashes so that it can be used
    for external back-up programs that need to know
    whether or not a file exists and, if so, where it is located.

  From a longer scripts, this program has been refactored down. The system has a business class, so to say,
    and a db-accessor helper class. Some test modules have been created.

  This script now links to the code, importing it from the refactored-resulted PyMirrorFileSystemByHash system.

  Written on 2015-01-13 Luiz Lewis
'''
import hashlib
import os
import sqlite3
import sys
import time
import string

import  bin_local_settings as bls
sys.path.insert(0, bls.PyMirrorFileSystemsByHash_PATH) # the PATH to this lib is placed (configured) in bin_local_settings.py
import Sha1FileSystemComplementer as fsComplementorMod

def walk_on_up_tree_to_grab_sha1hex(DEVICE_ROOT_ABSPATH, FURTHER_ABOVE_ON_DEVICE_PATH=None):
  '''

  :return:
  '''
  if FURTHER_ABOVE_ON_DEVICE_PATH == None:
    start_abspath = os.path.abspath('.')
  else:
    start_abspath = os.path.abspath(FURTHER_ABOVE_ON_DEVICE_PATH)
  if not start_abspath.startswith(DEVICE_ROOT_ABSPATH):
    raise Exception, 'Inconsistency: the device root path is not beginning the starting path for dirwalk, the point from the mirroring traversal will begin.'
  fs_complementer = fsComplementorMod.Sha1FileSystemComplementer(DEVICE_ROOT_ABSPATH) # instantiation uses the DEVICE_ROOT_ABSPATH not the start_abspath
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk(start_abspath):
    fs_complementer.db_insert_dirnames(dirnames, dirpath)
    walk_counter += 1
    print walk_counter, 'current path:', dirpath
    n_of_files = len(filenames)
    if n_of_files > 0:
      print 'Files found:'
      for filename in filenames:
        print filename
      print 'Total of files :', n_of_files
    n_of_dirs = len(dirnames)
    if n_of_dirs > 0:
      print 'Folders found:'
      for dirname in dirnames:
        print dirname
      print 'Total of folders :', n_of_dirs
    # insert or update the sha1hex on the sqlite-db on the device's root folder
    fs_complementer.p(current_abs_dirpath, filenames)
    print time.ctime(), dirpath, dirnames
    print '='*40

def get_args():
  DEVICE_ROOT_ABSPATH = None
  for arg in sys.argv:
    if arg.startswith('-d='):
      given_device_root_abspath = arg[ len('-d=') : ]
      if os.path.isdir(given_device_root_abspath):
        DEVICE_ROOT_ABSPATH = given_device_root_abspath
  return DEVICE_ROOT_ABSPATH

def main():
  DEVICE_ROOT_ABSPATH = get_args()
  walk_on_up_tree_to_grab_sha1hex(DEVICE_ROOT_ABSPATH)

if __name__ == '__main__':
  # main()
  main()
