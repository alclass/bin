#!/usr/bin/env python3
"""
Usage:
  $uTubeListBatchDeleter.py <filename-with-delete-paths>

Explanation:
  This script reads a textfile filled with paths (full filepaths) to be deleted.
  It will ask for confirmation before batch-deleting.

Example:
 $uTubeListBatchDeleter.py lista-de-arquivos-para-deletar.txt
-------------------------------------------------------------
"""
import os
import sys


class FilesBatchDeleter:

  def __init__(self, filename_with_delpaths):
    self.to_delete_filepaths = []
    self.filename_with_delpaths = None
    self.set_n_check_filename_with_delpaths(filename_with_delpaths)

  def set_n_check_filename_with_delpaths(self, filename_with_delpaths):
    if not os.path.isfile(filename_with_delpaths):
      error_msg = 'Error: File ' + filename_with_delpaths + 'does not exist. Program cannot continue with data.'
      raise OSError(error_msg)
    self.filename_with_delpaths = filename_with_delpaths

  def show_deletes(self):
    for i, fpath in enumerate(self.to_delete_filepaths):
      print(i, '=>', fpath)
    print('='*10, 'Total:', len(self.to_delete_filepaths), '='*10)

  def confirm_deletes(self):
    screen_msg = 'Do you confirm the (%d) deletes above? (*Y/n) ' % len(self.to_delete_filepaths)
    ans = input(screen_msg)
    if ans in ['Y', 'y', '']:
      return True
    return False

  def do_deletes(self):
    n_deletes = 0
    for i, fpath in enumerate(self.to_delete_filepaths):
      print(i+1, '=> [deleting]', fpath)
      os.remove(fpath)
      n_deletes += 1
    print('='*10, 'Total deletes:', n_deletes, '='*10)

  def read_filepaths_to_delete(self):
    print('Reading', self.filename_with_delpaths)
    fd = open(self.filename_with_delpaths)
    line = fd.readline()
    while line:
      filepath = line.rstrip(' \t\r\n')
      if os.path.isfile(filepath):
        self.to_delete_filepaths.append(filepath)
      line = fd.readline()
    fd.close()

  def process(self):
    self.read_filepaths_to_delete()
    self.show_deletes()
    bool_response = self.confirm_deletes()
    if bool_response:
      self.do_deletes()


def get_args():
  if len(sys.argv) < 2:
    print('Please, enter the filename with the filepaths to be delete. Use -h or --help for more info.')
    sys.exit(0)
  filename_with_delpaths = sys.argv[1]
  if filename_with_delpaths == '-h' or filename_with_delpaths.startswith('--help'):
    print(__doc__)
    sys.exit(0)
  if not os.path.isfile(filename_with_delpaths):
    print('File', filename_with_delpaths, 'does not exist. Please retry.')
    sys.exit(0)
  return filename_with_delpaths


def process():
  filename_with_delpaths = get_args()
  deleter = FilesBatchDeleter(filename_with_delpaths)
  deleter.process()


if __name__ == '__main__':
  process()
