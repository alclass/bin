#!/usr/bin/env python3
"""
dlYouTubeIdsAs278or160.py  (@see also alternative dlYouTubeIdsLookingUpFormats.py)
This script reads a text file with youtube-ids and
  tries to download the videos one by one. Three formats are tried, in the following order:

1) The first download try issues a 278+249 composite-format attempt
   (ie a webm video+audio composite)
2) if the above fails (ie, if 'format not available' is detected),
   the script falls back to a second download try and
   issues a 160+139 composite-format attempt
    (ie a mp4 video+audio composite)
3) if the above fails (ie, if 'format not available' is detected)
   a third download try issues a 160+140 download attempt (mp4)
    (ie a mp4 video+audio observing that audio 140 is larger than 139)
4) if none of the above downloads, it prints out a message informing
   'format <if-any> not recognized.
In a nutshell, the following formats are tried in this order:
  V278_249 = 278 video + 249 audio
  V160_139 = 160 video + 139 audio
  V160_140 = 160 video + 140 audio
TO-DO:
  The script might find out all available formats and
  issue the first one coinciding to a top one in a priority queue
  * in this strategy, no fall-back would happen for
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

  known_vacomposite_tuples = [
    '278+249',
    '160+139',
    '160+140',
  ]

  def __init__(self):
    pass

  @classmethod
  def get_interpolcomm_with_compositeformat(cls, vacompositeformat):
    if vacompositeformat in cls.known_vacomposite_tuples:
      interpolcomm = 'youtube-dl -w -f ' + vacompositeformat + ' {ytid}'
      return interpolcomm

  @classmethod
  def list_vacomposite_formats(cls):
    print('-'*40)
    print('Trying downloading formats in order:')
    for vacompositeformat in cls.known_vacomposite_tuples:
      print(vacompositeformat)
    print('-'*40)


class YtIdDownloader:

  def __init__(self, ytid):
    self.ytid = ytid
    self.formats_tried = []

  def download_ytid_with_vacompositeformat(self, vacompositetype):
    basecomm = VType.get_interpolcomm_with_compositeformat(vacompositetype)
    comm = basecomm.format(ytid=self.ytid)
    print(comm)
    p = Popen(comm, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    res = str(stderr)
    print('OS command response stderr: [[', res, ']]')
    if FORMAT_NOT_AVAILABLE_MSG.lower() in res.lower():
      print(
        FORMAT_NOT_AVAILABLE_MSG, ':: Tried format', vacompositetype,
        'formats_tried', self.formats_tried
      )
      print('=' * 40)
      return False
    res = str(stdout)
    res = res[:40] if len(res) > 40 else res
    print('Downloaded', self.ytid, res)
    return True


  def download(self, seq=1):
    """
    TO-DO: it's feasable/viable to refactor this function to method classes
           where videotype is kept as an instance variable
    """
    for vacompositetype in VType.known_vacomposite_tuples:
      print(seq, 'Trying downloading', self.ytid, 'with format', vacompositetype)
      downloaded = self.download_ytid_with_vacompositeformat(vacompositetype)
      if downloaded:
        break


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


def get_ytids_as_list(ytids_filename=None):
  ytids = []
  ytids_filename = ytids_filename or DEFAULT_YTIDS_FILENAME
  fd = open(ytids_filename)
  lines = fd.readlines()
  total = len(lines)
  for i, line in enumerate(lines):
    line = line.strip('\r\n')
    seq = i + 1
    print(seq, '/', total, 'extracting ytid', line)
    ytid = get_ytid_or_none(line)
    ytids.append(ytid)
  return ytids


def process_ytids_file(ytids_filename=None):
  ytids_filename = ytids_filename or DEFAULT_YTIDS_FILENAME
  VType.list_vacomposite_formats()
  ytids = get_ytids_as_list(ytids_filename)
  for i, ytid in enumerate(ytids):
    ytdownloader = YtIdDownloader(ytid)
    seq = i + 1
    ytdownloader.download(seq)


def process():
  process_ytids_file()


if __name__ == '__main__':
  process()
