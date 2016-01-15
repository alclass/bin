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

  Written on 2015-01-13 Luiz Lewis
'''
import hashlib
import os
import sqlite3
import sys
import time

class SHA1_NOT_OBTAINED(Exception):
  pass

SQLITE_DB_TABLENAME_DEFAULT     = 'hashes_of_uptree_files'
SQLITE_ROOTDIR_FILENAME_DEFAULT = 'hashed_files_thru_dir_tree.sqlite'
CONVENTIONED_DIR_ID_FOR_FILES = -1
CONVENTIONED_ROOT_DIR_ID      =  0
CONVENTIONED_ROOT_DIR_NAME    =  'ROOT'

def get_sqlite_connection():
  conn = sqlite3.connect(SQLITE_ROOTDIR_FILENAME_DEFAULT)
  return conn

device_root_abspath = None

def find_dir_id_for_dirpath(current_abs_path):
  minus_device_abspath = current_abs_path[ len( device_root_abspath ) : ]
  if minus_device_abspath.startswith('/'):
    raise Exception, 'abs path not starting with / : '+ minus_device_abspath
  if not os.path.isdir(current_abs_path):
    raise Exception, 'path does not exist : ' + current_abs_path
  pp = minus_device_abspath.split('/')
  if pp == ['','']:
    return CONVENTIONED_ROOT_DIR_ID
  if len(pp) < 2:
    raise Exception, 'inconsistency in internal list manipulation for finding root abs dir'
  conn = get_sqlite_connection()
  parent_dir_id = CONVENTIONED_ROOT_DIR_ID  # it starts its traversal at 'root'
  pp = pp[1:] # shift left 1 position
  for dirname in pp[1:]:
    sql = 'SELECT dir_id FROM %(tablename)s WHERE ' \
          'entryname     = "%(dirname)s" AND'        \
          'parent_dir_id = "%(parent_dir_id)s"' \
          %{ \
            'tablename'     : SQLITE_DB_TABLENAME_DEFAULT, \
            'dirname'       : dirname,
            'parent_dir_id' : parent_dir_id,
          }
    curr = conn.execute(sql)
    record = curr.fetchone()
    dir_id = record['dir_id']
    parent_dir_id = dir_id # in case, it'll loop on
  conn.close()
  return dir_id

def process_folder(current_abs_dirpath, filenames):
  print 'current_path:', current_abs_dirpath
  parent_dir_id = find_dir_id_for_dirpath(current_abs_dirpath)
  conn = sqlite3.connect()
  for filename in filenames:
    sha1obj = hashlib.sha1()
    try:
      f = open(filename, 'r')
      sha1obj.update(f.read())
      sha1hex = sha1obj.hexdigest()
    except Exception:
      raise SHA1_NOT_OBTAINED, 'SHA1_NOT_OBTAINED'
    # verify previous record existence and check equality
    sql = 'SELECT entryname, parent_dir_id FROM %(tablename)s WHERE ' \
          'sha1hex = "%(sha1hex)s"'      \
          %{ \
            'tablename': SQLITE_DB_TABLENAME_DEFAULT, \
            'sha1hex'  : sha1hex, \
          }
    curr = conn.execute(sql)
    record = curr.fetchone()
    other_parent_id = record['parent_dir_id']
    other_entryname = record['entryname']
    if other_parent_id == parent_dir_id and other_entryname == filename:
      # nothing needs be done
      continue
    sql = 'INSERT INTO %(tablename)s ' \
          '(parent_dir_id,dir_id, entryname, sha1hex) VALUES ' \
          '(%(parent_dir_id)d, %(dir_id)d, %(entryname)s, %(sha1hex)s)' \
          %{
            'tablename'     : SQLITE_DB_TABLENAME_DEFAULT, \
            'parent_dir_id' : parent_dir_id,
            'dir_id'        : CONVENTIONED_DIR_ID_FOR_FILES,
            'entryname'     : filename,
            'sha1hex'       : sha1hex,
            }
    retVal = conn.execute(sql)
    if retVal <> 0:
      print 'retVal NOT ZERO', retVal, 'for', sql
    conn.commit()
    conn.close()

def create_sqlite_db_file_on_root_folder():
  '''
  Convention:
  Root Folder has dir_id = 0 and name is ROOT
    if a ROOT named dir exists on ROOT, it will have the same name,
    but not the same dir_id
  Another special case is that ROOT's parent_id is also 0 (code will have to "see" it)
  A file has dir_id equals to -1
  :return:
  '''
  sql = '''
  CREATE TABLE %(tablename)s (
    dir_id        INT  NOT NULL,
    entryname     TEXT NOT NULL,
    parent_dir_id INT  NOT NULL,
    sha1hex CHAR(40) );''' \
      %{'tablename' : SQLITE_DB_TABLENAME_DEFAULT}
  conn = get_sqlite_connection()
  retVal = conn.execute(sql)
  if retVal <> 0:
    print 'retVal <> 0 ', retVal, 'on', sql
  else:
    print 'OK\n', sql, '\nOK'
  sql = '''INSERT INTO %(tablename)s (parent_dir_id, dir_id, entryname)
    VALUES ("%(conventioned_root_dir_id)d", "%(conventioned_root_dir_id)d", "%(conventioned_root_name)s");
  ''' %{
    'tablename'               : SQLITE_DB_TABLENAME_DEFAULT,
    'conventioned_root_dir_id': CONVENTIONED_ROOT_DIR_ID,
    'conventioned_root_dir_id': CONVENTIONED_ROOT_DIR_ID,
    'conventioned_root_name'  : CONVENTIONED_ROOT_DIR_NAME,
  }
  conn.execute(sql)
  conn.commit()
  '''
  if retVal <> 0:
    print 'retVal <> 0 ', retVal, 'on', sql
  else:
    print 'OK\n', sql, '\nOK'
  '''

def get_dirnames_on_db_with_same_parent_id(parent_dir_id):
  sql = 'SELECT entryname FROM %(tablename)s WHERE '         \
        'parent_dir_id = "%(parent_dir_id)d" AND '             \
        'dir_id        <> "%(conventioned_dir_id_for_files)d"' \
        %{ \
          'tablename'                     : SQLITE_DB_TABLENAME_DEFAULT,   \
          'parent_dir_id'                 : parent_dir_id,                 \
          'conventioned_dir_id_for_files' : CONVENTIONED_DIR_ID_FOR_FILES, \
        }
  conn = get_sqlite_connection()
  curr = conn.execute(sql)
  dirnames = []
  for record in curr.fetchall():
    dirname = record['dirname']
    dirnames.append(dirname)
  conn.close()
  return dirnames

def db_insert_dirnames(dirnames, dirpath):
  global next_dir_id
  parent_dir_id = find_dir_id_for_dirpath(dirpath)
  dirnames_on_db = get_dirnames_on_db_with_same_parent_id(parent_dir_id)
  if len(dirnames) > 0:
    conn = get_sqlite_connection()
  for dirname in dirnames:
    if dirname in dirnames_on_db:
      continue
    next_dir_id += 1
    sql = 'INSERT INTO %(tablename)s ' \
          '(parent_dir_id,dir_id, entryname) VALUES ' \
          '(%(parent_dir_id)d, %(dir_id)d, %(entryname)s)' \
          %{
            'tablename'     : SQLITE_DB_TABLENAME_DEFAULT, \
            'parent_dir_id' : parent_dir_id,
            'dir_id'        : next_dir_id,
            'entryname'     : dirname,
            }
    retVal = conn.execute(sql)
    if retVal <> 0:
      print 'retVal <> 0 ', retVal, 'on', sql
    else:
      print 'OK\n', sql, '\nOK'
  conn.commit()
  conn.close()

def walk_on_up_tree_to_grab_sha1hex():
  global device_root_abspath
  device_root_abspath = os.path.abspath('.')
  if not os.path.isfile(SQLITE_ROOTDIR_FILENAME_DEFAULT):
    create_sqlite_db_file_on_root_folder()
  sqlite3.connect(SQLITE_ROOTDIR_FILENAME_DEFAULT)
  walk_counter = 0
  for dirpath, dirnames, filenames in os.walk(device_root_abspath):
    db_insert_dirnames(dirnames, dirpath)
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
    process_folder(current_abs_dirpath, filenames)
    os.chdir(device_root_abspath)
    print '-'*40
    print 'Voltei!', time.ctime(), dirpath, dirnames, current_abs_dirpath
    print '='*40

def get_biggest_dir_id():
  sql = 'SELECT max(dir_id) FROM %(tablename)s' \
        %{'tablename': SQLITE_DB_TABLENAME_DEFAULT}
  try:
    conn = get_sqlite_connection()
    curr = conn.execute(sql)
    result = curr.fetchone()
    print result[0], result
    max_dir_id = int(result[0])
    conn.close()
  except sqlite3.OperationalError:
    create_sqlite_db_file_on_root_folder()
    return get_biggest_dir_id()
  return max_dir_id

next_dir_id = 0
def main():
  global next_dir_id
  next_dir_id = get_biggest_dir_id() + 1
  walk_on_up_tree_to_grab_sha1hex()

if __name__ == '__main__':
  main()
