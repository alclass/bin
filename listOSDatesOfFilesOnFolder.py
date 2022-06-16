#!/usr/bin/env python3
import datetime
import os


def list_os_dates(filepaths):
  for i, filepath in enumerate(filepaths):
    filestat = os.stat(filepath)
    a_date = filestat.st_atime
    c_date = filestat.st_ctime
    m_date = filestat.st_mtime
    folderpath, filename = os.path.split(filepath)
    print(i, filename, '@', folderpath)
    print('a_date', a_date, datetime.datetime.fromtimestamp(a_date))
    print('c_date', c_date, datetime.datetime.fromtimestamp(c_date))
    print('m_date', m_date, datetime.datetime.fromtimestamp(m_date))
    

def prep_filepaths(folderpath=None):
  if folderpath is None:
    folderpath = os.path.abspath('.')
  if not os.path.isdir(folderpath):
    error_msg = 'Error: director does not exist [%s]' %folderpath
    raise OSError(error_msg)
  filepaths = []
  entries = os.listdir(folderpath)
  for entry in entries:
    supposedfile = os.path.join(folderpath, entry)
    if os.path.isfile(supposedfile):
      filepaths.append(supposedfile)
  return filepaths


if __name__ == '__main__':
  filepaths = prep_filepaths()
  list_os_dates(filepaths)
