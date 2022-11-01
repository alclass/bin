#!/usr/bin/env python3
"""
dlYouTubeIdsLookingUpFormats.py

This script reads a text file with youtube-ids and
  tries to download the listed video-ids one by one.

Differently from dlYouTubeIdsAs278or160.py
  it will try to download a YouTube video following a format order
  under a format order FIFO queue.

The first format is previously suggested (to become a parameter in the future)
  and if it does not exist, the script will fetch from YouTube
  all available formats and queuing them up using a comparison
  known list (@see also the TO-DO below).

The format order is the following:

1) the first video+audio code-tuple come from the suggested one
  obs: at the moment, the first suggested one is the hardcoded 278+249

2) if the first suggested format does not exist,
   it fetches all formats available to the video queued to be downloaded

3) then it loops thru the available formats.
   (It's expected that the first available will be downloaded.)

Important: though the available format codes are linear, the script
  organized a 2D tuple list with previously known combinations,
  ie video+audio composites.
  (TO-DO: it's possible to go beyond the previously known combinations,
  this may be improved in the future.)
"""
from subprocess import PIPE, Popen
import string
import os


DEFAULT_YTIDS_FILENAME = 'youtube-ids.txt'
YT_VID_AUD_FORMAT_CODES_FILENAME = 'yt_video_audio_format_codes.txt'
YTID_CHARSIZE = 11
FORMAT_NOT_AVAILABLE_MSG = 'requested format not available'
FAILURE_IN_NAME_RESO_MSG = 'failure in name resolution'
basedldcomm = 'youtube-dl -w -f {vcode}+{acode} {ytid}'
basevercomm = 'youtube-dl -F {ytid}'
ENC64 = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_' + '-'
WAIT_TIME_IN_SEC = 30
PREFERENCE_VA_CODES_LIST = [
  (278, 249),
  (160, 139),
  (160, 140),
  (394, 139),
  (394, 250),
  (395, 139),
  (395, 140),
]
FIRST_PREF_VA_CODES_TUPLE = PREFERENCE_VA_CODES_LIST[0]


def get_format_code_example_list():
  """
  There is a txt file in the same directory as this script's
  Its filename is  yt_video_audio_format_codes
  The above text file contains an example got from "youtube-dl -F <ytid-example>"
  :return:
  """
  folderpath = os.path.realpath(os.path.dirname(__file__))
  filepath = os.path.join(folderpath, YT_VID_AUD_FORMAT_CODES_FILENAME)
  format_code_example_list = open(filepath).read()
  return format_code_example_list


def get_available_video_audio_combinations(format_codes, preference_double_codes_list=None):
  if preference_double_codes_list is None:
    preference_double_codes_list = PREFERENCE_VA_CODES_LIST
  filtered_doubles = []
  for double_code in preference_double_codes_list:
    vcode = double_code[0]
    acode = double_code[1]
    if vcode in format_codes:
      if acode in format_codes:
        tupl = (vcode, acode)
        filtered_doubles.append(tupl)
  return filtered_doubles


def extract_available_format_codes_from_text(text):
  """
  This function extracts the leading number in each line in text
  Example: The input:
137          mp4        1920x1080  1080p 1314k , mp4_dash container, avc1.640028@1314k, 30fps, video only, 102.16MiB
140          m4a        audio only tiny  129k , m4a_dash container, mp4a.40.2@129k (44100Hz), 10.07MiB
160          mp4        256x144    144p   48k , mp4_dash container, avc1.4d400c@  48k, 30fps, video only, 3.74MiB
  Should output:
    [137, 148, 160]

  :param text: string
  :return: format_codes: list
  """
  format_codes = []
  lines = text.split('\n')
  for line in lines:
    pp = line.split(' ')
    try:
      format_code = int(pp[0])
      format_codes.append(format_code)
    except ValueError:
      continue
  return format_codes


class YtIdDownloader:

  def __init__(self, ytid):
    self.ytid = ytid
    self.format_codes_from_yt = None
    self._ordered_suggested_vacodes_tuplelist = None
    self._ordered_available_vacodes_tuplelist = None
    # init up front the "suggested" vacodes tuplelist,
    # the available in YouTube should be lazyly-got, ie upon need
    _ = self.ordered_suggested_vacodes_tuplelist
    # _ = self.ordered_available_vacodes_tuplelist

  @property
  def ordered_suggested_vacodes_tuplelist(self):
    if self._ordered_suggested_vacodes_tuplelist is not None:
      return self._ordered_suggested_vacodes_tuplelist
    self._ordered_suggested_vacodes_tuplelist = PREFERENCE_VA_CODES_LIST
    return self._ordered_suggested_vacodes_tuplelist

  @property
  def first_suggested_va_codes_tuple(self):
    return self.ordered_suggested_vacodes_tuplelist[0]

  @property
  def first_option_va_codes_tuple(self):
    """
        self.first_option_va_codes_tuple = (278, 249)
    :return:
    """
    if len(self.ordered_suggested_vacodes_tuplelist) < 1:
      return None
    return self.ordered_suggested_vacodes_tuplelist[0]

  @property
  def ordered_available_vacodes_tuplelist(self):
    """
      Fetches the available va formats for video in YouTube
    """
    if self._ordered_available_vacodes_tuplelist is not None:
      return self._ordered_available_vacodes_tuplelist
    format_codes_comm = basevercomm.format(ytid=self.ytid)
    p = Popen(format_codes_comm, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    format_code_text = str(stdout)
    self.format_codes_from_yt = extract_available_format_codes_from_text(format_code_text)
    self._ordered_available_vacodes_tuplelist = get_available_video_audio_combinations(
      self.format_codes_from_yt, self.ordered_suggested_vacodes_tuplelist
    )
    return self._ordered_available_vacodes_tuplelist

  def dld_with_video_audio_code_tuple(self, vcode, acode):
    """
    """
    dld_comm = basedldcomm.format(vcode=vcode, acode=acode, ytid=self.ytid)
    print('First try with', self.ytid)
    print(dld_comm)
    p = Popen(dld_comm, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stderr = str(stderr)
    if len(stderr) > 5:  # when no error happens, it should be b" "
      print(stderr)
      return False
    print('Downloaded', self.ytid, ':: Continuing if any')
    return True

  def download(self):
    """
    basedldcomm = 'youtube-dl -w -f {vformat}+{aformat} {ytid}'
    basevercomm = 'youtube-dl -F {ytid}'
    """
    vcode, acode = self.first_suggested_va_codes_tuple
    succeeded = self.dld_with_video_audio_code_tuple(vcode, acode)
    if succeeded:
      return
    if len(self.ordered_available_vacodes_tuplelist) < 1:
      return
    for vacodetuple in self.ordered_available_vacodes_tuplelist:
      if vacodetuple == self.first_suggested_va_codes_tuple:
        continue
      vcode, acode = vacodetuple
      succeeded = self.dld_with_video_audio_code_tuple(vcode, acode)
      if succeeded:
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
  ytids = get_ytids_as_list(ytids_filename)
  for i, ytid in enumerate(ytids):
    seq = i + 1
    print('-'*40)
    print(seq, 'processing ytid', ytid)
    ytid_downloader = YtIdDownloader(ytid)
    ytid_downloader.download()


def process():
  process_ytids_file()


if __name__ == '__main__':
  process()
