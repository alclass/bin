#!/usr/bin/env python3
"""
dlYouTubeIdsAs278or160.py
This script read a file with youtube-ids and tries to download one by one.
1) The first try issues a 278+249 download attempt (ie a webm video+audio composite)
2) if 'format not available' is detected, a second try issue a 160+140 download attempt (mp4)
3) if 'failure in name resolution' is detected, it waits a little and retries back to 1.
"""
import os
from subprocess import PIPE, Popen
import string
import time


DEFAULT_YTIDS_FILENAME = 'youtube-ids.txt'
YTID_CHARSIZE = 11
FORMAT_NOT_AVAILABLE_MSG = 'requested format not available'
FAILURE_IN_NAME_RESO_MSG = 'failure in name resolution'
basecomm160 = 'youtube-dl -w -f 160+140 {ytid}'
basecomm278 = 'youtube-dl -w -f 278+249 {ytid}'
ENC64 = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_' + '-'
WAIT_TIME_IN_SEC = 30


def download_ytid(ytid):
  comm = basecomm278.format(ytid=ytid)
  print(comm)
  p = Popen(comm, shell=True, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate()
  res = str(stderr)
  print('OS command response: [[', res, ']]')
  if FORMAT_NOT_AVAILABLE_MSG.lower() in res.lower():
    print(FORMAT_NOT_AVAILABLE_MSG, ':: Trying format 160+140')
    comm = basecomm160.format(ytid=ytid)
    print('Retrying with [', comm, ']')
    os.system(comm)
  elif FAILURE_IN_NAME_RESO_MSG.lower() in res.lower():
    print(FAILURE_IN_NAME_RESO_MSG, ':: Wait a little before retrying (', WAIT_TIME_IN_SEC, 'sec)')
    time.sleep(WAIT_TIME_IN_SEC)
    return download_ytid(ytid)
  return


def get_ytid_or_none(supposed_ytid):
  """
  :param supposed_ytid: supposed_ytid is checked to be a 64-encoding string
  :return:
  """
  if supposed_ytid is None:
    return None
  try:
    supposed_ytid = str(supposed_ytid)
    supposed_ytid = supposed_ytid.lstrip(' \t').rstrip(' \t\r\n')
  except ValueError:
    return None
  if len(supposed_ytid) != YTID_CHARSIZE:
    return None
  bool_list = filter(lambda c: c in ENC64, supposed_ytid)
  if False in bool_list:
    return None
  ytid = supposed_ytid
  return ytid


def process_ytids_file(ytids_filename=None):
  ytids_filename = ytids_filename or DEFAULT_YTIDS_FILENAME
  fd = open(ytids_filename)
  lines = fd.readlines()
  total = len(lines)
  for i, line in enumerate(lines):
    line = line.strip('\r\n')
    seq = i + 1
    print(seq, '/', total, 'Checking for ytid in', line)
    ytid = get_ytid_or_none(line)
    if ytid:
      download_ytid(ytid)


def process():
  process_ytids_file()


if __name__ == '__main__':
  process()
