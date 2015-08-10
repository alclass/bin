#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys
import getopt

'''
Options
'''
#import renameCleanBeginning as rcb

SEARCH_PREFIX = ' href="/projects/'
def get_project_names_on_folder():
  '''
  '''
  filenames = os.listdir('.')
  project_names_on_folder = []
  for fil in filenames:
    pp = fil.split('.')
    try:
      before_dot = pp[0]
      before_dot = before_dot.lstrip().rstrip()
      pos = before_dot.find(' ')
      if  pos > -1:
        before_dot = before_dot[ : pos]
    except IndexError:
      continue
    project_names_on_folder.append(before_dot)
  return project_names_on_folder

def get_project_names_from_file(filename):
  text = open(filename).read()
  words = text.split(' ')
  bulk_project_names_to_be_filtered_out = []
  for word in words:
    word = word.lstrip().lstrip()
    bulk_project_names_to_be_filtered_out.append(word)
  return  bulk_project_names_to_be_filtered_out

def filter_out_existing_ones(existing_project_names, bulk_project_names_to_be_filtered_out):
  yet_to_download_project_names = []
  for word in bulk_project_names_to_be_filtered_out:
    if word in existing_project_names:
      continue
    yet_to_download_project_names.append(word)
  return yet_to_download_project_names

def process():
  existing_project_names = get_project_names_on_folder()
  filename = sys.argv[1]
  bulk_project_names_to_be_filtered_out = get_project_names_from_file(filename)
  yet_to_download_project_names = filter_out_existing_ones(existing_project_names, bulk_project_names_to_be_filtered_out)
  print 'Size existing_project_names = ', len(existing_project_names)
  print 'Size those to be filtered out = ', len(bulk_project_names_to_be_filtered_out)
  print 'Size yet_to_download_project_names = ', len(yet_to_download_project_names)
  yet_to_download_project_names.sort()
  for project_name in yet_to_download_project_names:
    print project_name,
  print

if __name__ == '__main__':
  process()
  # unittest.main()
