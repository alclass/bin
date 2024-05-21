#!/usr/bin/env python3
"""
outputLastNFoldernames.py

Explanation:
  This script is not yet complete.
  For the time being, it created a "marking" text file, inside a subfolder
    (e.g. mp3s_converted), with the following line inside it:
  mp3s converted: [<name of parent folder>]

  But this script, in the future, should be updated
    so that it can do more things configurably.

  Example for this future mentioned upgrade:
    1) for writing or not writing the marking file
    2) for including or not including the prefix phrase in the marking file
    3) for including the foldername or the whole folderpath
"""
import glob
import os
import sys


def get_arg_from_cli_as_an_abspath_or_currdir_default():
  abspath_as_arg = None
  if len(sys.argv) > 1:
    abspath_as_arg = sys.argv[1]
  if abspath_as_arg is None or not os.path.isdir(abspath_as_arg):
    abspath_as_arg = os. getcwd()
  return abspath_as_arg


class FoldernamesExtractor:

  def __init__(self, curr_abspath=None, last_n_foldernames=2, path_must_exist=True):
    self.curr_abspath = curr_abspath
    self.last_n_foldernames = last_n_foldernames
    self.output_last_foldernames = None
    self.path_must_exist = path_must_exist
    self.treat_curr_abspath()

  def treat_curr_abspath(self):
    if self.curr_abspath is None:
      self.curr_abspath = get_arg_from_cli_as_an_abspath_or_currdir_default()
    if self.path_must_exist:
      if not os.path.isdir(self.curr_abspath):
        errmsg = f"path [{self.curr_abspath}] does not exist."
        raise OSError(errmsg)

  def extract_last_n_foldernames(self):
    pp = self.curr_abspath.split('/')
    if len(pp) < self.last_n_foldernames:
      return self.curr_abspath
    self.output_last_foldernames = '/'.join(pp[-self.last_n_foldernames:])

  def save_marking_file(self):
    try:
      first_foldername = self.output_last_foldernames.split('/')[0]
    except IndexError:
      first_foldername = self.output_last_foldernames
    line = f"mp3s_converted [{first_foldername}]"
    filename = line + '.txt'
    if not os.path.isfile(filename):
      outfile = open(filename, 'w')
      outfile.write(line)
      outfile.close()
      print('Writing file:', filename)
    else:
      print('File already exists:', filename)

  def process(self):
    self.extract_last_n_foldernames()
    self.save_marking_file()


def process():
  extractor = FoldernamesExtractor()
  extractor.process()


if __name__ == '__main__':
  process()
