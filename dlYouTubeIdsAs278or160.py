#!/usr/bin/env python3
"""
dlYouTubeIdsAs278or160.py
This script reads a text file with youtube-ids and
  tries to download one by one. Three formats are tried, in the following order:

1) The first download try issues a 278+249 format attempt
   (ie a webm video+audio composite)
2) if the above fails (ie, if 'format not available' is detected),
   the script falls back to a second download try and
   issues a 160+139 format attempt
    (ie a mp4 video+audio composite)
3) if the above fails (ie, if 'format not available' is detected)
   a third download try issues a 160+140 download attempt (mp4)
    (ie a mp4 video+audio observing that audio 140 is larger than 139)
4) if none of the above downloads, it prints out a message informing
   'format <if-any> not recognized.
In a nutshell, the following formats are tried in this order:
  V160_139 = 160 video + 139 audio
  V160_140 = 160 video + 140 audio
  V278_249 = 278 video + 249 audio
TO-DO:
  The script might find out all available formats and
  issue the first one coinciding in a priority queue
  * in this strategy, no fall-back would happend for
    in this case the available ones are known.
  This can be achieved by $youtube-dl -F <ytid>
    which lists all available formats.
"""
from subprocess import PIPE, Popen
import string


DEFAULT_YTIDS_FILENAME = 'youtube-ids.txt'
YTID_CHARSIZE = 11
FORMAT_NOT_AVAILABLE_MSG = 'requested format not available'
FAILURE_IN_NAME_RESO_MSG = 'failure in name resolution'
ENC64 = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_' + '-'
WAIT_TIME_IN_SEC = 30


class VType:
  def __init__(self):
    pass
  V160_139 = '160+139'
  basecomm160_139 = 'youtube-dl -w -f 160+139 {ytid}'
  V160_140 = '160+140'
  basecomm160_140 = 'youtube-dl -w -f 160+140 {ytid}'
  V278_249 = '278+249'
  basecomm278_249 = 'youtube-dl -w -f 278+249 {ytid}'


def download_ytid(ytid, videotype=None, formats_tried=()):
  formats_tried = tuple(list(formats_tried) + [videotype])
  if videotype is None or videotype == VType.V278_249:
    comm = VType.basecomm278_249.format(ytid=ytid)
    print(comm)
    p = Popen(comm, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    res = str(stderr)
    print('OS command response stderr: [[', res, ']]')
    if FORMAT_NOT_AVAILABLE_MSG.lower() in res.lower():
      print(FORMAT_NOT_AVAILABLE_MSG, ':: Trying format', VType.V160_139)
      return download_ytid(ytid, VType.V160_139)
    res = str(stdout)
    print('OS command response stdout: [[', res, ']]')
  elif videotype == VType.V160_139:
    comm = VType.basecomm160_139.format(ytid=ytid)
    print(comm)
    p = Popen(comm, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    res = str(stderr)
    print('OS command response stderr: [[', res, ']]')
    if FORMAT_NOT_AVAILABLE_MSG.lower() in res.lower():
      print(FORMAT_NOT_AVAILABLE_MSG, ':: Trying format', VType.V160_140)
      return download_ytid(ytid, VType.V160_140)
    res = str(stdout)
    print('OS command response stdout: [[', res, ']]')
  elif videotype == VType.V160_140:
    comm = VType.basecomm160_140.format(ytid=ytid)
    print(comm)
    p = Popen(comm, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    res = str(stderr)
    print('OS command response stderr: [[', res, ']]')
    if FORMAT_NOT_AVAILABLE_MSG.lower() in res.lower():
      print(FORMAT_NOT_AVAILABLE_MSG, ':: formats_tried', formats_tried)
      return download_ytid(ytid, VType.V160_140)
    res = str(stdout)
    print('OS command response stdout: [[', res, ']]')
  else:
    print('Videotype', videotype, 'not recognized')
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
