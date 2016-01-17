#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
batchWalkHashingFilesToRootFolderSqliteDB.py
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

def walk_on_up_tree_to_grab_sha1hex():
  '''

  :return:
  '''
  global device_root_abspath
  device_root_abspath = os.path.abspath('.')
  fs_complementer = fsComplementorMod.Sha1FileSystemComplementer(device_root_abspath)
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk(device_root_abspath):
    fs_complementer.db_insert_dirnames(dirnames, dirpath)
    complement_path = dirpath
    if complement_path.startswith('./'):
      complement_path = complement_path[2:]
    current_abs_dirpath = os.path.join(device_root_abspath, complement_path)
    walk_counter += 1
    print walk_counter, 'current path:', current_abs_dirpath
    print 'Files found @', complement_path
    for filename in filenames:
      print filename
    os.chdir(current_abs_dirpath)
    fs_complementer.(current_abs_dirpath, filenames)
    os.chdir(device_root_abspath)
    print '-'*40
    print 'Voltei!', time.ctime(), dirpath, dirnames, current_abs_dirpath
    print '='*40

def main():
  walk_on_up_tree_to_grab_sha1hex()

if __name__ == '__main__':
  # main()
  main()
