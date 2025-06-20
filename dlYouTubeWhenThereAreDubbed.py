#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

This script uses yt-dlp to download (YouTube) videos in two or more languages if available
  (translations in general are autodubbed)

This script accepts the following input:
  1  it receives as input a youtube-video-id (ytid)
  2  it also receives the codes for languages (it does not discover them, the user has to enter them)
     obs: as far as we've observed, these codes are not standardized,
          for example, in general, a video that is dubbed into English
            has a sufix "-0" added to its audiocode, but if the original audio is English,
              it seems undeterminate what sufix will be given to it

This script downloads the video-only chunk only once and copies it to each new language.
For example,
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
    it's a good sign that both the network is working and videos are complete
    if subprocess does not return with 0, a message will be printed out indicating the error
"""
import argparse
import os.path
import shutil
import string
import subprocess
import sys
DEFAULT_YTIDS_FILENAME = 'youtube-ids.txt'
YTID_CHARSIZE = 11
enc64_valid_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + '_-'
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--ytid", type=str,
                    help="the video id")
parser.add_argument("--useinputfile", action='store_true',
                    help="read the default input ytids file")
parser.add_argument("--dirpath", type=str,
                    help="Directory recipient of the download")
parser.add_argument("--videoonlycode", type=str, default="160",
                    help="video only code: example: 160")
parser.add_argument("--audioonlycodes", type=str, default="233-0,233-1",
                    help="audio only codes: example: 233-0,233-1")
args = parser.parse_args()


def read_ytids_from_default_file_n_get_as_list(p_dlddir_abspath, ytids_filename=None):
  if ytids_filename is None:
    ytids_filename = DEFAULT_YTIDS_FILENAME
  inputfilepath = os.path.join(p_dlddir_abspath, ytids_filename)
  lines = open(inputfilepath, 'r').readlines()
  lines = map(lambda line: line[:YTID_CHARSIZE] if len(line) > 10 else '', lines)
  ytdis = list(filter(lambda line: len(line) == YTID_CHARSIZE, lines))
  return ytdis


def verify_ytid_validity_or_raise(ytid):
  if ytid is None:
    errmsg = 'Error: ytid cannot be empty, please reenter it.'
    raise ValueError(errmsg)
  all_chars_enc64 = True  # until proven contrary
  # 1 - verify chars are ENC64
  should_not_have_falses = list(map(lambda c: c in enc64_valid_chars, ytid))
  size = len(str(ytid))
  if False in should_not_have_falses:
    all_chars_enc64 = False
  # 2 - verify charsize is YTID_CHARSIZE (11 at the time of writing)
  if size != YTID_CHARSIZE or not all_chars_enc64:
    errmsg = (
      f"""
      Please check the following two problems with ytid (the {YTID_CHARSIZE}-character video id):
      (one or the other or both)

      => ytid = "{ytid}" 

      1 It must have {YTID_CHARSIZE} characters: {len(ytid) == YTID_CHARSIZE}: It has {size}

      2 All its characters should be ENC64
        In "{ytid}", is it ENC64? {all_chars_enc64}

      ENC64 characters are: "{enc64_valid_chars}"

      Please, correct the observations(s) above and retry.
      """
    )
    raise ValueError(errmsg)


class Downloader:

  DEFAULT_VIDEO_ONLY_CODE = 160
  videodld_tmpdirname = 'videodld_tmpdir'
  comm_line_base = 'yt-dlp -w -f {codecomposite} "{videourl}"'
  video_baseurl = 'https://www.youtube.com/watch?v={ytid}'

  def __init__(
      self,
      ytid: str,
      dlddir_abspath: (os.path, str) = None,
      videoonlycode: int = None,
      audioonlycodes: list = None
    ):
    self.ytid = ytid
    self.dlddir_abspath, self.videoonlycode, self.audioonlycodes = dlddir_abspath, videoonlycode, audioonlycodes
    self.treat_input()
    self.videoonly_filename = None
    # self.videoonly_filepath = None : this is a property
    self.audio_first_filepath = None
    self.audioonly_filepaths = []
    self.copied_filenames = []
    self.videoonly_filename = None  # this is the base filename that will keep the videoonly across various audiofiles
    self.n_audio_dld = 0

  def treat_input(self):
    verify_ytid_validity_or_raise(self.ytid)
    if self.dlddir_abspath is None:
      self.dlddir_abspath = os.path.abspath('.')
    if self.videoonlycode is None:
      self.videoonlycode = self.DEFAULT_VIDEO_ONLY_CODE

  @property
  def videoonly_filepath(self):
    return os.path.join(self.child_tmpdir_abspath, self.videoonly_filename)

  @property
  def n_langs(self):
    if self.audioonlycodes is None:
      return 0
    return len(self.audioonlycodes)

  @property
  def videourl(self):
    pdict = {'ytid': self.ytid}
    url = self.video_baseurl.format(**pdict)
    return url

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
  def child_tmpdir_abspath(self):
    _tmpdir_abspath = os.path.join(self.dlddir_abspath, self.videodld_tmpdirname)
    if not os.path.isdir(_tmpdir_abspath):
      os.makedirs(_tmpdir_abspath)
    return _tmpdir_abspath

  @property
  def dot_f_videocode(self):
    _dot_f_videocode = f'.f{self.videoonlycode}'
    return _dot_f_videocode

  def discover_dld_videofilename(self):
    """
    Because a temporary dir is created for the download,
      there expects to be only one videofile
    Then, one looks for one file (and only one) with a video extension
    (for the time being, code 160 or 602 are mp4 - they will be hardcoded for the time being)
    (a second option might be mkv, but this is a TODO for the time being)
    another one is a checking of the current working directory
    """
    filenames = os.listdir('.')  # notice an os.chdir(<dld_dir>) happened before
    videofilename_soughtfor = list(filter(lambda f: f.endswith('.mp4'), filenames))
    if len(videofilename_soughtfor) == 0:
      return
    videofilename = videofilename_soughtfor[0]
    name, dot_ext = os.path.splitext(videofilename)
    # graft the ".f<number>" sufix before its extension (example ".f160")
    newname = name + self.dot_f_videocode + dot_ext
    scrnsg = f'Renaming "{videofilename}" to "{newname}"'
    print(scrnsg)
    os.rename(videofilename, newname)
    # this filename will be used for as many audio files are queued up for download
    scrnsg = f"Videofilename is {self.videoonly_filename}"
    self.videoonly_filename = newname

  def download_video_only(self):
    """
    At this point, that video filename will be known
    :return:
    """
    strdict = {'codecomposite': self.videoonlycode, 'videourl': self.videourl}
    comm = self.comm_line_base.format(**strdict)
    try:
      scrmsg = f"""In directory: {self.child_tmpdir_abspath}
      Running: {comm}
      """
      print(scrmsg)
      ans = input('Run this command above (Y/n) ? [ENTER] means Yes')
      if ans not in ['Y', 'y', '']:
        return False
      subprocess.run(comm, shell=True, check=True)  # timeout=5 (how long can a download last?)
    # except subprocess.TimeoutExpired:
    #     print(f"Command timed out: {comm}")
    except subprocess.CalledProcessError as e:
      print(f"Command failed with return code {e.returncode}: {comm}")
    except KeyboardInterrupt:
      print("Interrupted by user. Exiting loop.")
    return True

  def get_videoonly_filename_for_number(self, nsufix):
    return self.videoonly_filename + str(nsufix)

  def rename_videobasefile_sothatitcancomposite(self):
    """
    The suppose videofilename is videobasefilename minus its number sufix
    For example:
      if  videofile is this-video-ytid.f160.mp4.3
      then this rename should only remove the ".3" sufix
      resulting filename should be this-video-ytid.f160.mp4
    """
    videoonly_filename_w_nsufix = self.get_videoonly_filename_for_number(self.n_audio_dld)
    videoonly_basefilename = videoonly_filename_w_nsufix.rstrip(str(self.n_audio_dld))
    scrmsg = f"Renaming {videoonly_filename_w_nsufix} to {videoonly_basefilename}"
    print(scrmsg)
    os.rename(videoonly_filename_w_nsufix, videoonly_basefilename)

  def download_audio_complementing_basevideoonly(self, audiocode):
    self.n_audio_dld += 1
    self.rename_videobasefile_sothatitcancomposite()  # it's done by removing number sufix
    compositecode = f"{self.videoonlycode}+{audiocode}"
    comm = self.comm_line_base.format({'codecomposite': compositecode, 'videourl': self.videourl})
    try:
      scrmsg = f"Running: {comm}"
      print(scrmsg)
      subprocess.run(comm, shell=True, check=True)  # timeout=5 (how long can a download last?)
    # except subprocess.TimeoutExpired:
    #     print(f"Command timed out: {comm}")
    except subprocess.CalledProcessError as e:
      print(f"Command failed with return code {e.returncode}: {comm}")
    except KeyboardInterrupt:
      print("Interrupted by user. Exiting loop.")

  def download_audiofiles(self):
    for i in range(self.n_langs):
      audiocode = self.audioonlycodes
      self.download_audio_complementing_basevideoonly(audiocode)


  def process(self):
    """
      1st -> position (cd changedir) at the working tmpdir
      2nd -> download the 160 video
      3rd -> disconver the downloaded video's filename
      4th -> copy it to as many as there audio lang entered
        (for example: if one language is Italian, another is for English, two copies are made)
      5th -> download the audio(s) for each language
        5-1 download the audiofile proper
        5-2 "fuse" it with the videofile in store so that the composite results
    """
    scrmsg = f"1st -> position at the working tmpdir {self.child_tmpdir_abspath}"
    print(scrmsg)
    os.chdir(self.child_tmpdir_abspath)
    scrmsg = f"Entered dir {self.child_tmpdir_abspath}"
    print(scrmsg)
    scrmsg = "2nd -> download the 160 video"
    print(scrmsg)
    self.download_video_only()
    scrmsg = "3rd -> copy it once because one will be used for Italian, the other for English"
    print(scrmsg)
    scrmsg = "3rd -> disconver the downloaded video's filename"
    print(scrmsg)
    self.discover_dld_videofilename()
    scrmsg = "4th -> copy it to as many as there audio lang entered"
    print(scrmsg)
    self.copy_video_only_n_lang_times()
    scrmsg = "5th -> download the audio(s) complements"
    print(scrmsg)
    for i in range(self.n_langs):
      audiocode = self.audioonlycodes
      self.download_audio_complementing_basevideoonly(audiocode)
    # move all videos from child_tmpdir_abspath to its parent dir


def adhoctest1():
  pass


def adhoctest2():
  dirpath = args.dirpath or os.path.abspath('.')
  # inputfilepath = os.path.join(dirpath, DEFAULT_YTIDS_FILENAME)
  ytids = read_ytids_from_default_file_n_get_as_list(dirpath)
  scrmsg = f"adhoctest2 :: ytids = {ytids}"
  print(scrmsg)


def adhoc_test1():
  ytid = 'abc+10'
  scrmsg = f'Testing verify_ytid_validity_or_raise({ytid})'
  print(scrmsg)
  verify_ytid_validity_or_raise(ytid)


def get_cli_args():
  """
  Required parameters:
    src_rootdir_abspath & trg_rootdir_abspath

  Optional parameter:
    resolution_tuple

  :return: srctree_abspath, trg_rootdir_abspath, resolution_tuple
  """
  try:
    if args.h or args.help:
      print(__doc__)
      sys.exit(0)
  except AttributeError:
    pass
  ytid = args.ytid
  boo_readfile = args.useinputfile
  # default to the current working directory if none is given
  dirpath = args.dirpath or os.path.abspath(".")
  videoonlycode = args.videoonlycode or None
  audioonlycodes = args.audioonlycodes or None
  return ytid, boo_readfile, dirpath, videoonlycode, audioonlycodes


def confirm_cli_args_with_user():
  ytid, b_useinputfile, dirpath, videoonlycode, audioonlycodes = get_cli_args()
  print(ytid, 'b_useinputfile', b_useinputfile, dirpath, videoonlycode, audioonlycodes)
  if not os.path.isdir(dirpath):
    scrmsg = "Source directory [{src_rootdir_abspath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  try:
    int(videoonlycode)
  except ValueError:
    scrmsg = f"videoonlycode [{videoonlycode}] should be a number. Please, retry"
    print(scrmsg)
    return False
  try:
    audioonlycodes = audioonlycodes.split(',')
  except ValueError:
    scrmsg = f"audioonlycodes [{audioonlycodes}] should be a list of numbers with possible sufixes. Please, retry"
    print(scrmsg)
    return False
  print('Paramters')
  print('='*20)
  scrmsg = f"ytid = [{ytid}]"
  print(scrmsg)
  scrmsg = f"useinputfile = [{b_useinputfile}]"
  print(scrmsg)
  scrmsg = f"dirpath = [{dirpath}]"
  print(scrmsg)
  scrmsg = f"videoonlycode = [{videoonlycode}]"
  print(scrmsg)
  scrmsg = f"audioonlycodes = [{audioonlycodes}]"
  print(scrmsg)
  print('='*20)
  scrmsg = "The parameters are okay? (Y/n) [ENTER] means Yes "
  ans = input(scrmsg)
  print('='*20)
  confirmed = False
  if ans in ['Y', 'y', '']:
    confirmed = True
  return confirmed, b_useinputfile, ytid, dirpath, videoonlycode, audioonlycodes


def process():
  """
  """
  confirmed, b_useinputfile, ytid, dirpath, videoonlycode, audioonlycodes = confirm_cli_args_with_user()
  if not confirmed:
    return
  p_dlddir_abspath = dirpath
  p_videoonlycode = 160
  p_audioonlycodes = ['233-0', '233-1']
  if b_useinputfile:
    ytids = read_ytids_from_default_file_n_get_as_list(p_dlddir_abspath)
  else:
    ytids = [ytid]
  scrmsg = f'ytids are: {ytids}'
  print(scrmsg)
  for ytid in ytids:
    downloader = Downloader(
      ytid=ytid,
      dlddir_abspath=p_dlddir_abspath,
      videoonlycode=p_videoonlycode,
      audioonlycodes=p_audioonlycodes,
    )
    downloader.process()


if __name__ == '__main__':
  """
  Example for test (could be any one that has some dubbing options)
  https://www.youtube.com/watch?v=xtaOUGft57o
  ytid = xtaOUGft57o
    dlYouTubeWhenThereAreDubbed.py --ytid xtaOUGft57o   
    dlYouTubeWhenThereAreDubbed.py ----useinputfile   

  adhoc_test1()
  adhoctest2()
  """
  process()
