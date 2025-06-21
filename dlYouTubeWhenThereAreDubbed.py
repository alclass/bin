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
from localuserpylib.pydates import localpydates as pydates
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


def is_str_enc64(line):
  blist = list(map(lambda c: c in enc64_valid_chars, line))
  if False in blist:
    return False
  return True


def read_ytids_from_default_file_n_get_as_list(p_dlddir_abspath, ytids_filename=None):
  if ytids_filename is None:
    ytids_filename = DEFAULT_YTIDS_FILENAME
  inputfilepath = os.path.join(p_dlddir_abspath, ytids_filename)
  lines = open(inputfilepath, 'r').readlines()
  lines = map(lambda line: line[:YTID_CHARSIZE] if len(line) > 10 else '', lines)
  ytdis = filter(lambda line: len(line) == YTID_CHARSIZE, lines)
  ytdis = list(filter(lambda line: is_str_enc64(line), ytdis))
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
  comm_line_base = 'yt-dlp -w -f {compositecode} "{videourl}"'
  video_baseurl = 'https://www.youtube.com/watch?v={ytid}'
  video_dot_extensions = ['.mp4', '.mkv', '.webm', '.m4v', '.avi', '.wmv']

  def __init__(
      self,
      ytid: str,
      dlddir_abspath: (os.path, str) = None,
      videoonlycode: int = None,
      audioonlycodes: list = None
    ):
    self.ytid = ytid
    self.dlddir_abspath = dlddir_abspath
    self.videoonlycode = videoonlycode
    self.audioonlycodes = audioonlycodes  # example: ['233-0', '233-1']
    self.treat_input()
    self.b_verified_once_tmpdir_abspath = None
    self.video_canonical_filename = None  # this is the video filename with the f-sufix, it's known after download
    self.audio_first_filepath = None
    self.n_on_going_lang = 0

  def treat_input(self):
    verify_ytid_validity_or_raise(self.ytid)
    if self.dlddir_abspath is None:
      self.dlddir_abspath = os.path.abspath('.')
    if self.videoonlycode is None:
      self.videoonlycode = self.DEFAULT_VIDEO_ONLY_CODE

  @property
  def canonical_video_filepath(self):
    return os.path.join(self.child_tmpdir_abspath, self.video_canonical_filename)

  def get_video_or_audio_filename_with_bksufix(self, n_for_bksufix):
    """
    Example:
      a-videofilename-ytid.mp4.bk3
      bk3 means that it is the 3rd copy of a-videofilename-ytid.mp4
        and is to be used to complement the 3rd audio language file
    """
    bksufix = f".bk{n_for_bksufix}"
    videofilename_w_bksufix = self.video_canonical_filename + bksufix
    return videofilename_w_bksufix

  def get_video_or_audio_filename_with_fsufix(self, fsufix):
    """
        os.path.join(self.child_tmpdir_abspath, self.video_canonical_filename)
    """
    name, dotext = os.path.splitext(self.video_canonical_filename)
    if fsufix.startswith('.'):
      newname_w_fsufix = name + fsufix
    else:
      newname_w_fsufix = name + '.' + fsufix
    fsufixed_filename = f"{newname_w_fsufix}{dotext}"
    return fsufixed_filename

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

  def form_bksufixed_videofilepath_basedonthecanonical(self, nth) -> os.path:
    bksufix = f".bk{nth}"
    folderpath, filename = os.path.split(self.canonical_video_filepath)
    next_filename = filename + bksufix
    return os.path.join(folderpath, next_filename)

  def copy_n_rename_videoonly_n_lang_times(self):
    """
    The first video is just renamed to sufix "bk<seq>" where seq is the audio sequential number
    The following videos are copied each one with its "bk<seq>" sufix
    Obs: The first video is renamed at the end, ie the copies are done firstly
    """
    if self.n_langs == 0:
      return
    if self.n_langs > 1:
      for i in range(1, self.n_langs):
        lang_seq = i + 1
        trg_filepath = self.form_bksufixed_videofilepath_basedonthecanonical(lang_seq)
        shutil.copy2(self.canonical_video_filepath, trg_filepath)
        audiocode = self.audioonlycodes[lang_seq-1]
        scrmsg = f"""lang={lang_seq} audiocode={audiocode}
         canonical_video_filepath =  {self.canonical_video_filepath}
         copied (for complementing later on) to {trg_filepath}"""
        print(scrmsg)
    # rename "bk1" at last
    lang_seq = 1
    trg_filepath = self.form_bksufixed_videofilepath_basedonthecanonical(lang_seq)
    os.rename(self.canonical_video_filepath, trg_filepath)
    scrmsg = f"lang={lang_seq}: renamed canonical file to {trg_filepath}"
    print(scrmsg)

  def verify_tmpdir_once_n_raise_oserror_if_files_wo_pastdatesufixes_exist(self, tmpdir_abspath):
    """
    This method:
      1: creates tmpdir if needed
      2: verifies that if there are videos in tmpdir, it should be date-prefixed and this date be past 'today'
      3: in case a video exists with today's date, an OSError exception is raised
    :param tmpdir_abspath:
    :return:
    """
    self.b_verified_once_tmpdir_abspath = False
    os.makedirs(tmpdir_abspath, exist_ok=True)
    filenames = os.listdir(tmpdir_abspath)
    for filename in filenames:
      if not filename.endswith(tuple(self.video_dot_extensions)):
        continue
      pp = filename.split(' ')
      strdate = pp[0]
      if not pydates.is_strdate_before_today(strdate):
        errmsg = f"Date Sufix [{strdate}] in filename is either missing or it's not past today"
        raise OSError(errmsg)
    self.b_verified_once_tmpdir_abspath = True

  @property
  def child_tmpdir_abspath(self):
    """
    The actions/tasks of the script happen in a newly created directory
      (or if previously created, files should have a previous-date prefix, otherwise this script should be interrupted)
    :return:
    """
    tmpdir_abspath = os.path.join(self.dlddir_abspath, self.videodld_tmpdirname)
    if not self.b_verified_once_tmpdir_abspath:
      self.verify_tmpdir_once_n_raise_oserror_if_files_wo_pastdatesufixes_exist(tmpdir_abspath)
    return tmpdir_abspath

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
    os.rename(videofilename, newname)
    # this filename will be used for as many audio files are queued up for download
    self.video_canonical_filename = newname
    scrmsg = f"""Discovered videofilename:
     found =  [{videofilename}]
     renamed to =  [{self.video_canonical_filename}]"""
    print(scrmsg)

  def download_video_only(self):
    """
    At this point, that video filename will be known
    :return:
    """
    strdict = {'compositecode': self.videoonlycode, 'videourl': self.videourl}
    comm = self.comm_line_base.format(**strdict)
    scrmsg = f"@download_video_only | {comm}"
    print(scrmsg)
    try:
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
    return self.video_canonical_filename + str(nsufix)

  def rename_videobasefile_sothatitcancomposite(self):
    """
    The supposed videofilename is videobasefilename (*) minus its number sufix
    (*) reminding that the video part is only downloaded once,
        every lang video will be formed by just getting its own audiopart as a complement
    For example:
      if  videofile is this-video-ytid.f160.mp4.bk3
      then this rename should only remove the ".bk3" sufix
        (actually a removal (rstrip) is not necessary, for the canonical name is kept in the object
        so it's just retrieved)
      resulting filename should be this-video-ytid.f160.mp4
    """
    n_for_bksufix = self.n_on_going_lang
    videoonly_filename_w_nsufix = self.get_video_or_audio_filename_with_bksufix(n_for_bksufix)
    scrmsg = f"""bksufix = .bk{n_for_bksufix} | renaming:
    FROM:   {videoonly_filename_w_nsufix}
    TO:   {self.video_canonical_filename}"""
    print(scrmsg)
    # check existence
    srcfilepath = os.path.join(self.child_tmpdir_abspath, videoonly_filename_w_nsufix)
    if not os.path.isfile(srcfilepath):
      errmsg = f"Error: srcfile [{videoonly_filename_w_nsufix}] for backrename does not exist."
      raise OSError(errmsg)
    os.rename(videoonly_filename_w_nsufix, self.video_canonical_filename)

  def download_audiopart_to_fuse_w_videoonly(self):
    self.rename_videobasefile_sothatitcancomposite()  # it's done by removing number sufix
    audiocode = self.audioonlycodes[self.n_on_going_lang - 1]
    compositecode = f"{self.videoonlycode}+{audiocode}"
    pdict = {'compositecode': compositecode, 'videourl': self.videourl}
    comm = self.comm_line_base.format(**pdict)
    try:
      scrmsg = f"audiocode={audiocode} | running: {comm}"
      print(scrmsg)
      scrmsg = f"Continue with the download above (Y/n)? [ENTER] means Yes"
      ans = input(scrmsg)
      if ans not in ['Y', 'y', '']:
        sys.exit(0)
      subprocess.run(comm, shell=True, check=True)  # timeout=5 (how long can a download last?)
    # except subprocess.TimeoutExpired:
    #     print(f"Command timed out: {comm}")
    except subprocess.CalledProcessError as e:
      print(f"Command failed with return code {e.returncode}: {comm}")
    except KeyboardInterrupt:
      print("Interrupted by user. Exiting loop.")

  def rename_videofile_after_audiovideofusion(self):
    newfilename = f"lang{self.n_on_going_lang} " + self.video_canonical_filename
    trg_filepath = os.path.join(self.child_tmpdir_abspath, newfilename)
    audiocode = self.audioonlycodes[self.n_on_going_lang-1]
    scrmsg = f"""lang={self.n_on_going_lang} | audiocode={audiocode} | renaming:
    FROM: {self.video_canonical_filename}
    TO:   {newfilename}
    """
    print(scrmsg)
    if not os.path.isfile(self.canonical_video_filepath):
      errmsg = f"Error: srcfile [{self.canonical_video_filepath}] for lang-add-rename does not exist."
      raise OSError(errmsg)
    os.rename(self.canonical_video_filepath, trg_filepath)

  def download_audio_complements(self):
    """
    self.n_on_going_lang is an instance variable that controls lang orderseq throughout the class
    """
    for self.n_on_going_lang in range(1, self.n_langs+1):
      self.download_audiopart_to_fuse_w_videoonly()
      self.rename_videofile_after_audiovideofusion()

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
    self.copy_n_rename_videoonly_n_lang_times()
    scrmsg = "5th -> download the audio(s) complements"
    print(scrmsg)
    self.download_audio_complements()
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
  if b_useinputfile:
    ytids = read_ytids_from_default_file_n_get_as_list(dirpath)
  else:
    ytids = [ytid]
  scrmsg = f'ytids are: {ytids}'
  print(scrmsg)
  for ytid in ytids:
    downloader = Downloader(
      ytid=ytid,
      dlddir_abspath=dirpath,
      videoonlycode=videoonlycode,
      audioonlycodes=audioonlycodes,
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
