#!/usr/bin/env python3
"""
renameBulkCleanSpecifiedStr.py
@see renameCleanSpecifiedStr.py for the renaming with a string-pattern

This script reads a text file * with "string items" and executes batch-renamings using script renameCleanSpecifiedStr.py

* each line in the text file must end with '#'

As of 2022-11-25 The default input text filename is [z-string-list.txt]
Check source code for (constant) variable DEFAULT_RENAME_EXTENSION
"""
import glob
import os
import sys


DEFAULT_RENAME_EXTENSION = 'mp4'


extensions = ['mp4', 'srt']
DEFAULT_INPUT_TEXT_FILENAME = 'z-string-list.txt'


def run_renames(stritems):
  basecomm = 'renameCleanSpecifiedStr.py -e=%(ext)s -s="%(stritem)s"'
  for stritem in stritems:
    for ext in extensions:
      dict_item = {'ext': ext, 'stritem': stritem}
      comm = basecomm % dict_item
      os.system(comm)


def read_string_list_from_textfile():
  lines = open(DEFAULT_INPUT_TEXT_FILENAME).readlines()
  stritems = []
  for line in lines:
    stritem = line.rstrip(' \r\n')
    if stritem[-1] == '#':
      stritem = stritem[:-1]
      stritems.append(stritem)
  for stritem in stritems:
    print(stritem)
  ans = input('Continue ')
  
  return stritems


def process():
  stritems = read_string_list_from_textfile()
  run_renames(stritems)


if __name__ == '__main__':
  process()
