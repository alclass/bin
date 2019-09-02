#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
readTheDocsUrlCompleter.py
'''
#import glob, os, shutil, sys, time
import os, sys

URL_BASE = 'http://media.readthedocs.org/%(format_id)s/%(project_name)s/latest/%(project_name)s.%(file_extension)s'
# https://buildmedia.readthedocs.org/media/%(format_id)s/%(project_name)s/latest/%(project_name)s.%(file_extension)s
# https://readthedocs.org/projects/tags/%(tagname)s/

DEFAULT_FILE_EXT_LIST = ['epub']

class RtdocsDownload:
  '''

  '''

  def __init__(self, project_names, file_ext_list):
    '''

    :param project_names:
    :param file_ext_list:
    '''
    self.n_downloads = 0
    self.do_download = True # prove otherwise
    self.set_project_names(project_names)
    self.set_file_ext_list(file_ext_list)
    self.process_download()

  def set_project_names(self, project_names):
    '''

    :param project_names:
    :return:
    '''
    if type(project_names) != list or project_names == []:
      error_msg = 'Project names list either does not exist or is empty.'
      raise ValueError(error_msg)

    self.project_names = list(project_names)

  def set_file_ext_list(self, file_ext_list):
    '''

    :param file_ext_list:
    :return:
    '''
    if type(file_ext_list) != list or file_ext_list == []:
      self.file_ext_list = list(DEFAULT_FILE_EXT_LIST)
      return
    self.file_ext_list = list(file_ext_list)

  def process_download(self):
    '''

    :return:
    '''
    self.list_downloads_from_readthedocs_for_confirmation()
    if self.do_download:
      self.download_from_readthedocs()

  def list_downloads_from_readthedocs_for_confirmation(self):
    '''

    :return:
    '''
    n_total = 0
    for i, project_name in enumerate(self.project_names):
      n_project = i + 1
      for file_extension in self.file_ext_list: # ['pdf', 'zip', 'epub']
        n_total += 1
        print ( n_project, n_total, project_name, file_extension )
    print ('='*40)
    print ('Please, confirm dowloads above:')
    print ('='*40)
    ans = input('Download? (Y/n) ')
    if ans in ['N', 'n']:
      self.do_download = False

  def download_from_readthedocs(self):
    '''

    :return:
    '''

    n_downloads = 0
    if not self.do_download:
      return
    for i, project_name in enumerate(self.project_names):
      i_project = i + 1
      for file_extension in self.file_ext_list: # ['pdf', 'zip', 'epub']
        n_downloads += 1
        print ( i_project, n_downloads, project_name, file_extension )
        self.go_download(n_downloads, project_name, file_extension)

  def go_download(self, n_downloads, project_name, file_extension):
    '''

    :param project_name:
    :param file_extension:
    :return:
    '''

    format_id = get_format_id_from_file_extension(file_extension)
    urldict = {
      'format_id' : format_id,
      'project_name' : project_name,
      'file_extension' : file_extension,
    }
    url = URL_BASE %urldict
    comm = 'wget -c %s' %url
    print ( n_downloads, comm )
    os.system(comm)

def get_format_id_from_file_extension(file_extension):
  if file_extension == 'zip':
    return 'htmlzip'
  return file_extension

def extract_file_ext_list(arg):
  file_ext_list_str = ''
  file_ext_list = []
  try:
    file_ext_list_str = arg[ len('-el=') : ]
  except IndexError:
    pass
  file_ext_list_str = file_ext_list_str.strip(', ')
  if len(file_ext_list_str) > 0:
    file_ext_list = file_ext_list_str.split(',')
  return file_ext_list

def get_args():
  project_names = []
  file_ext_list = list(DEFAULT_FILE_EXT_LIST)
  for arg in sys.argv[1:]:
    if arg.startswith('-el='):
      file_ext_list = extract_file_ext_list(arg)
    else:
      project_names.append(arg)
  return project_names, file_ext_list

def process():
  project_names, file_ext_list = get_args()
  RtdocsDownload(project_names, file_ext_list)

if __name__ == '__main__':
  process()
