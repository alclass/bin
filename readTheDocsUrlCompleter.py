#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
readTheDocsUrlCompleter.py
'''
#import glob, os, shutil, sys, time
import os, sys

URL_BASE = 'http://media.readthedocs.org/%(format_id)s/%(project_name)s/latest/%(project_name)s.%(file_extension)s'

def get_format_id_from_file_extension(file_extension):
  if file_extension == 'zip':
    return 'htmlzip'
  return file_extension

n_downloads = 0
def go_download(project_name, file_extension):
  global n_downloads

  format_id = get_format_id_from_file_extension(file_extension)
  urldict = {'format_id':format_id, 'project_name':project_name,'file_extension':file_extension}
  url = URL_BASE %urldict
  comm = 'wget -c %s' %url
  n_downloads += 1
  print n_downloads, comm
  os.system(comm)

def download_from_readthedocs(do_download=False):
  n_project = 0; n_total = 0
  for i, project_name in enumerate(project_names):
    n_project = i + 1
    for file_extension in ['pdf', 'zip', 'epub']:
      n_total += 1
      print n_project, n_total, project_name, file_extension
      if do_download:
        go_download(project_name, file_extension)
  if do_download:
    return
  print '='*40
  print 'Please, confirm dowloads above:'
  print '='*40
  ans = raw_input('ok? (if not, break execution with Ctrl-C) ')
  download_from_readthedocs(do_download=True)

project_names = []
def get_args():
  for project_name in sys.argv[1:]:
    project_names.append(project_name)

if __name__ == '__main__':
  get_args()
  download_from_readthedocs()

