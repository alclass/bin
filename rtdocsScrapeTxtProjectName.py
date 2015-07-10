#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys
import getopt

'''
Options
'''
#import renameCleanBeginning as rcb

SEARCH_PREFIX = ' href="/projects/'
def scrapeTxt(filename):
  '''
  '''
  print 'scrapeTxt(',filename,')'
  project_names = []
  text = open(filename).read()
  while len(text) > 0:
    pos = text.find(SEARCH_PREFIX)
    if pos > -1:
      text = text[ pos+len(SEARCH_PREFIX) : ]
      bar_pos = text.find('/')
      if bar_pos > -1:
        project_name = text[ : bar_pos ]
        # print project_name
        project_names.append(project_name)
        text = text[ bar_pos : ]
      else:
        project_names.append(text)
        break
    else:
      break
  return  project_names

def printProjectNames(project_names):
  os.system('ls > z_all_project_names_on_folder.txt')
  lines = open('z_all_project_names_on_folder.txt').readlines()
  project_names_on_folder_dict = {}
  for line in lines:
    dot_pos = line.find('.')  # there is no dot within a project name !!!
    if dot_pos < 0:
      continue
    project_name = line [ : dot_pos ]
    project_names_on_folder_dict[project_name] = 1
  missing_names = []
  for project_name in project_names:
    if project_name not in project_names_on_folder_dict:
      missing_names.append(project_name)
  print 'Total project_names_on_folder', len(project_names_on_folder_dict)
  print 'Total project_names_on z-projnames', len(project_names)
  print 'Total project_names_on missing names', len(missing_names)
  for project_name in missing_names:
    print project_name,
  print


def process():
  filename = sys.argv[1]
  if not os.path.isfile(filename):
    print 'File', filename, 'does not exist on running folder.'
    return
  project_names = scrapeTxt(filename)
  printProjectNames(project_names)

if __name__ == '__main__':
  process()
  # unittest.main()
