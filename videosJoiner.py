#!/usr/bin/env python3
"""
The "hint" to this script was taken originally from a post in askubuntu.com
The post cited command mkvmerge (from package mkvtoolnix)

Basically this script will autoform a command line such as the following:
$ mkvmerge -o outfile,mkv "file1.mp4" \* "file2.mp4" \+ "file3.mp4"

Usage:
videosJoin.py [<file_extension>]

WHERE
<file_extension> is a video file extension (e.g. mp4|mkv|webm etc)
If no extension is given, mp4 is the default.

A confirmation yes/no question will be asked for running the autoformed command line.
"""
import glob, os, shutil, sys

DEFAULT_EXT = '.mp4'


def find_form_n_get_foldername():
  """
  Extracts the foldername of the executing path.
  Example:
    e1) suppose executing path is '/Sci/Physics/Quantum' (not coinciding with the script's path)
    e2) this function will find 'Quantum'

  Some OBS
  exec_fullpath = 
  Notice that the composition os.path.dirname(os.path.realpath(__file__)), differently from os.getcwd(),
    gives the script's folder (somewhere in PythonPath) not the executing path
  """
  exec_fullpath = os.getcwd()
  foldername = os.path.split(exec_fullpath)[1]
  outfilename = '"joined ' + foldername + '.mkv"'
  return outfilename


def get_arg():
  for arg in sys.argv:
    if arg.startswith('-e='):
      ext = arg[len('-e='):]
      return ext
  return None

def form_n_get_commline(p_ext):
  ext = p_ext or DEFAULT_EXT
  if not ext.startswith('.'):
    ext = '.' + ext
  files = glob.glob('*'+ext)
  files.sort()
  outfilename = find_form_n_get_foldername()
  if os.path.isfile(outfilename):
    error_msg = 'File [%s] already exists.'
    print(error_msg)
    sys.exit(1)
  commline = 'mkvmerge -o ' + outfilename + ' '	
  for f in files:
    commline += '"' + f + '" \+ '
  commline = commline.strip(' \+ ')
  return commline


def confirm_exec_commline(commline):
  print(commline)
  screen_msg = 'Confirm executing the above line? (Y*/n) [ENTER] means Yes '
  ans = input(screen_msg)
  if not ans in ['', 'Y', 'y']:
    return False
  return True


def exec_commline(commline):
  if confirm_exec_commline(commline):
    print('Running command. Please wait.')
    os.system(commline)


def process():
  ext = get_arg() or DEFAULT_EXT
  commline = form_n_get_commline(ext)
  exec_commline(commline)


if __name__ == '__main__':
  process()
