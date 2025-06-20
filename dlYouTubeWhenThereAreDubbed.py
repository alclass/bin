#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

This script uses yt-dlp to download (YouTube) videos in two or more languages if available
  (translations in general are autodubbed)

This script accepts the following input:
  1  it receives as input a youtube-video-id
  2  it also receives the codes for languages (it does not discover them, the user has to enter them)

This script downloads the video part only once and copies it to each new language.
For example:
  1 suppose a video id as <videoid>
  2 suppose also that video code 160 is available
  3 suppose also that audio codes are available in dubbed Italian (as 233-5) and the original English (as 233-9)

Then, this script will:
  1st download the 160 video
  2nd copy it once because one will be used for Italian, the other for English
  3rd download the 160+233-5 video (the dubbed Italian)
  4th download the 160+233-9 video (the original English)

Limitation: This scripts does not do (at least yet):
  1 it doesn't discover the language codes, even less which codes are available at all
    (the user enters those)
  2 it may not be able to check all problems from the command line, but if subprocess returns with 0,
    it's a good sign that the both the network is working and videos are complete
    if subprocess does not return with 0, a message will be printed out indicating the error
"""
import os.path
import shutil
import string
import subprocess
enc64_valid_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + '_-'


def verify_ytid_validity_or_raise(ytid):
  if ytid is None:
    errmsg = 'Error: ytid cannot be empty, please reenter it.'
    raise ValueError(errmsg)
  try:
    if len(str(ytid)) != 11:
      raise ValueError
    should_not_have_falses = list(filter(lambda c: c in enc64_valid_chars, ytid))
    if False in should_not_have_falses:
      raise ValueError
  except ValueError as e:
    errmsg = (f'Error: ytid [{ytid}] should have 11 characters and those as basic ENCODE64, '
              f'please reenter it.\n'
              f'The valid characters (enc64) are "{enc64_valid_chars}"\n'
              f' => {e}')
    raise ValueError(errmsg)


class Downloader:

  DEFAULT_VIDEO_ONLY_CODE = 160
  videodld_tmpdirname = 'videodld_tmpdir'

  def __init__(
      self,
      ytid: str,
      dlddir_abspath: os.path | str = None,
      videoonlycode: int = None,
      audioonlycodes: list = None
    ):
    self.ytid = ytid
    self.dlddir_abspath, self.videoonlycode, self.audioonlycodes = dlddir_abspath, videoonlycode, audioonlycodes
    self.treat_input()
    self.videoonly_filepath = None
    self.audio_first_filepath = None
    self.audioonly_filepaths = []

  comm_line_base = 'yt-dlp -w -f {codecomposite} "{videourl}"'

  def treat_input(self):
    verify_ytid_validity_or_raise(self.ytid)
    if self.dlddir_abspath is None:
      self.dlddir_abspath = os.path.abspath('.')
    if self.videoonlycode is None:
      self.videoonlycode = self.DEFAULT_VIDEO_ONLY_CODE

  @property
  def n_langs(self):
    if self.audioonlycodes is None:
      return 0
    return len(self.audioonlycodes)

  @property
  def videourl(self):
    if self.audioonlycodes is None:
      return 0
    return len(self.audioonlycodes)

  def make_filepath_for_nth_videocopy(self, nth) -> os.path:
    sufix = f'.bk{nth}'
    folderpath, filename = os.path.split(self.audio_first_filepath)
    next_filename = filename + sufix
    return os.path.join(folderpath, next_filename)

  def copy_video_only_n_lang_times(self):
    if self.n_langs < 2:
      return
    for i in range(1, self.n_langs+1):
      targetfilepath = self.make_filepath_for_nth_videocopy(i)
      shutil.copy2(self.videoonly_filepath, targetfilepath)

  @property
  def tmpdir_abspath(self):
    _tmpdir_abspath = os.path.join(self.dlddir_abspath, self.videodld_tmpdirname)
    if not os.path.isdir(_tmpdir_abspath):
      os.makedirs(_tmpdir_abspath)
    return _tmpdir_abspath

  @property
  def dot_f_videocode(self):
    _dot_f_videocode = f'.f{self.videoonlycode}'
    return _dot_f_videocode

  def find_video_filename_after_download(self):
    """
    One looks for a file with a video extension
    (for the time being, code 160 or 602 are mp4 - they will be hardcoded for the time being)
    (a second option might be mkv, but this is a TODO for the time being)
    another one is a checking of the current working directory
    """
    filenames = os.listdir('.')  # notice an os.chdir(<dld_dir>) happened before
    sought_for = list(filter(lambda f: f.endswith('.mp4'), filenames))
    videofilename = sought_for[0]
    name, dot_ext = os.path.splitext(videofilename)
    newname = name + self.dot_f_videocode + dot_ext
    scrnsg = f'Renaming "{videofilename}" to "{newname}"'
    print(scrnsg)
    os.rename(videofilename, newname)

  def download_video_only(self):
    """
    At this point that video filename will be known
    :return:
    """
    comm = self.comm_line_base.format({'codecomposite': self.videoonlycode, 'videourl': self.videourl})
    os.chdir(self.tmpdir_abspath)
    subprocess.call(comm)
    # find its name
    self.find_video_filename_after_download()

  def process(self):
    """
      1st download the 160 video
      2nd copy it once because one will be used for Italian, the other for English
      3rd download the 160+233-5 video (the dubbed Italian)
      4th download the 160+233-9 video (the original English)

    """
    self.download_video_only()
    self.copy_video_only_n_lang_times()


def adhoctest1():
  pass


def process():
  """
  """
  test_ytid = 'test_ytid'
  downloader = Downloader(test_ytid)
  downloader.process()


if __name__ == '__main__':
  """
  adhoctest1()
  """
  process()
