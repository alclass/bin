#!/usr/bin/env python3
"""
fillEachFolderWithATextFileContainingItsName
"""
import os


def create_textfile_with_its_name_as_line(currentpath, subdirname):
  subdirpath = os.path.join(currentpath, subdirname)
  filename = subdirname + '.txt'
  filepath = os.path.join(subdirpath, filename)
  if os.path.isfile(filepath):
    print('Cannot create file for it already exists =>', filepath)
    return False
  fp = open(filepath, 'w')
  line = str(subdirname)
  fp.write(line)
  fp.close()
  print('Written file =>', filepath)
  return True
  
  
def sweep_subfolders(currentpath=None):
  if currentpath is None or not os.path.isdir(currentpath):
    currentpath = os.path.abspath('.')
  entries = os.listdir('.')
  for subdirname in entries:
    if os.path.isdir(subdirname):
      _ = create_textfile_with_its_name_as_line(currentpath, subdirname)


def process():
  sweep_subfolders()


if __name__ == '__main__':
  process()
