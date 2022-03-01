#!/usr/bin/env python3
"""
This script binary-copies a file up to a certain amount of bytes (abondoning a chunk of bytes at its end).

One of its application is when the last bytes of an incomplete downloaded file (within a certain amount) get corrupted
  and the download may be continued from the former incomplete file minus that certain amount of bytes.

One example of when that occurs is when, by mistake, a second "wget -c" download is started
  against a downlaad that is already happening, causing the above mentioned corruption.

Taking away those few bytes will allow for a download restart without having to restart it all over.

Usage:
$rollPartialBinaryCopy.py <source_filepath> <minusbytes>
Meaning:
  <source_filepath> is path to the input file
  <minusbytes> is the integer that represents the ending bytes that should not be copied over to the new file

OBS: the target file (the ending-split file) receives sufix "_COPIED" after name (before extension, if any).

Example:
  $rollPartialBinaryCopy.py /a/b/c/file.mp4 1600
Meaning:
  <source_filepath> is "/a/b/c/file.mp4"
  <minusbytes> is 1600 bytes (*)

1600 bytes is 80KiB/s for 20 seconds.

In this case, the copied file will be: "/a/b/c/file_COPIED.mp4"
"""
import os.path
import sys
BUF_SIZE = 65536
DEFAULT_TEST_FOLDER = '/home/dados/Sw3/SwDv/OSFileSystemSwDv/PyMirrorFileSystemsByHashSwDv/dados/src/d1'


def copy_partially_binary_reading_n_writing(src_filepath, trg_filepath, minusbytes):
  """
  The default to parameter minus_bytes is:
    80kbps for 20 seconds
    80 * 20 = 1600 kilobytes

  :param src_filepath:
  :param trg_filepath:
  :param minusbytes:
  :return:
  """
  if src_filepath is None or trg_filepath is None or minusbytes is None:
    error_msg = 'Either src_filepath is None or trg_filepath is None or minus_bytes is None'
    raise ValueError(error_msg)
  if not os.path.isfile(src_filepath):
    print('src_filepath DOES NOT exist, program cannot continue ::', src_filepath)
    return False
  if os.path.isfile(trg_filepath):
    print('trg_filepath EXISTS, program cannot continue ::', trg_filepath)
    return False
  ongoing_read_bytes = 0
  filesize = os.stat(src_filepath).st_size
  up_to_bytes = filesize - minusbytes
  print('filesize', filesize, 'up_to_bytes', up_to_bytes)
  if up_to_bytes <= 0:
    print('up_to_bytes <= 0 cannot continue')
    return False
  last_write = False
  with open(src_filepath, 'rb') as rf:
    with open(trg_filepath, 'wb') as wf:
      while True:
        try:
          if ongoing_read_bytes + BUF_SIZE >= up_to_bytes:
            buf_size = up_to_bytes - ongoing_read_bytes
            last_write = True
          else:
            buf_size = BUF_SIZE
          data = rf.read(buf_size)
          ongoing_read_bytes += buf_size
          if not data:
            # file has endeded
            break
          wf.write(data)
          if last_write:
            break
        except (IOError, OSError) as e:
          print('IOError | OSError', e)
          return False
      wf.close()
      rf.close()
      return True


def prepare_n_copy_partially(src_filepath=None, minusbytes=None):
  """

  :param filename:
  :param minusbytes:
  :param folderpath:
  :return:
  """
  if src_filepath is None:
    filename = 'test.txt'
    default_folderpath = DEFAULT_TEST_FOLDER
    src_filepath = os.path.join(default_folderpath, filename)
  filesize = os.stat(src_filepath).st_size
  if minusbytes is None:
    minusbytes = int(filesize*0.1)
  if minusbytes < 1:
    print('minusbytes < 1', minusbytes, 'cannot continue')
    return False
  folderpath, src_filename = os.path.split(src_filepath)
  trg_name, trg_ext = os.path.splitext(src_filename)
  trg_name = trg_name + '_COPIED'
  if len(trg_ext) > 0:
    trg_filename = trg_name + trg_ext
  else:
    trg_filename = trg_name
  trg_filepath = os.path.join(folderpath, trg_filename)
  print('='*40)
  print('sourcefile:', src_filepath)
  print('targetfile:', trg_filepath)
  print('minusbytes:', minusbytes)
  bool_res = copy_partially_binary_reading_n_writing(src_filepath, trg_filepath, minusbytes)
  if bool_res:
    print('Operation completed: target file above was partially copied as above.')
  else:
    print('Operation failed: there may have appeared messages above.')


def get_filepath_n_minusbytes():
  filepath = None
  minusbytes = None
  try:
    filepath = sys.argv[1]
    minusbytes = int(sys.argv[2])
  except (IndexError, ValueError):
    pass
  return filepath, minusbytes


def process():
  filepath, minusbytes = get_filepath_n_minusbytes()
  prepare_n_copy_partially(filepath, minusbytes)


if __name__ == '__main__':
  process()
