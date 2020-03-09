#!/usr/bin/env python3
'''
This script extracts a specified string from all files having a chosen extension.

For the time being it only works with the mp4 extension
  TO-DO:  parameter -e=<extension> will be introduced later on and the script will work with any extension.

Example:

=> Suppose there are the 3 following files on the target folder (target folder is the current directory at this version):
    [file1 blah.mp4] [file2 blah.mp4] [file3 blah.mp4]

=> Running the script as:

          prompt$ renameCleanSpecifiedStr.py -s=" blah"

will rename them to (with confirmation (y/n) or without it [not yet implemented, TO-DO with parameter -y]):
    [file1.mp4] [file2.mp4] [file3.mp4]

Ie, the string " blah" will be extracted away from each mp4 file on folder.
'''
import glob, os, sys


DEFAULT_RENAME_EXTENSION = 'mp4'

class Renamer:
  '''
  class Renamer:
  '''
  def __init__(self, specified_str, no_confirm=False, extension=None, abspath=None):
    '''

    :param specified_str:
    :param extension:
    :param abspath:
    '''
    self.specified_str = specified_str
    self.extension     = extension
    if self.extension is None:
      self.extension = DEFAULT_RENAME_EXTENSION
    self.abspath = abspath
    if self.abspath is None or not os.path.isdir(self.abspath):
      self.abspath = os.path.abspath('.')
    self.target_filenames    = []; self.n_target_filenames = 0
    self.rename_pairs = [];        self.n_renames = 0
    self.no_confirm = no_confirm
    self.confirm_rename = False
    self.rename_process()

  def rename_process(self):
    '''

    :return:
    '''
    os.chdir(self.abspath)
    self.target_filenames = glob.glob('*.' + self.extension)
    self.confirm_rename = False
    self.prepare_for_rename()
    if self.confirm_rename:
      self.do_rename()
    self.show_numbers()

  def prepare_for_rename(self):
    '''

    :return:
    '''
    print ("Folder =>", self.abspath)
    print ("Replace str =>", self.specified_str)
    for i, target_filename in enumerate(self.target_filenames):
      if target_filename.find(self.specified_str):
        newname = target_filename.replace(self.specified_str, '')
        if os.path.isfile(newname):
          continue
        rename_pair = (target_filename, newname)
        self.rename_pairs.append(rename_pair)
        seq = i + 1
        print(seq, ' => Rename:')
        print('FROM:', target_filename)
        print('TO:  ', newname)

    if self.no_confirm:
      self.confirm_rename = True
      return

    if len(self.rename_pairs) == 0:
      self.confirm_rename = False
      return

    ans = input('Rename them (y/N) ? ')
    # self.confirm_rename = False
    if ans in ['y', 'Y']:
      self.confirm_rename = True

  def do_rename(self):
    '''

    :return:
    '''
    self.n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      target_filename = rename_pair[0]
      new_namefile  = rename_pair[1]
      if not os.path.isfile(target_filename):
        continue
      if os.path.isfile(new_namefile):
        continue
      self.n_renames += 1
      print('FROM =>', target_filename)
      print('TO   =>', new_namefile)
      os.rename(target_filename, new_namefile)

  def show_numbers(self):
    '''

    :return:
    '''
    print ('Number of rename pairs:', len(self.rename_pairs))
    print ('Number of renamed:',      self.n_renames)

def get_str_arg():
  specified_str = None
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-s='):
      specified_str = arg[ len('-s=') : ]
      break
  if specified_str is None:
    print (__doc__)
    error_msg = 'specified_str is missing. Program cannot continue.'
    raise ValueError(error_msg)
  return specified_str

def process():
  specified_str = get_str_arg()
  Renamer(specified_str)

if __name__ == '__main__':
  process()
