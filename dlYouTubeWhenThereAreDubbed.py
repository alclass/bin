#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

This script uses yt-dlp to download (YouTube) videos in two or more languages if available
  (translations in general are autodubbed)

This script accepts the following input:
  1  it receives as input a youtube-video-id (ytid)
  2  it also receives the codes for languages (it does not discover them, the user has to enter them)
     obs: as far as we've observed, these codes are not standardized,
          for example, in general, a video that is autodubbed into English
            has sufix "-0" added to its audiocode (example: 233-0 or 234-0),
            but if the original audio is already English,
            it seems undeterminate what "dash-number" the system will give to it
            (example: it might be a "-7", or a "-8" or a "-9"
              (the user would have to find and enter it via the audiocodes parameter),
              asking the API [something not done here] could make this known)
            On the other hand, what seems stable is when English is autodubbed
              so it gets the "-0" annexed to the audiocode and the original language an "-1"
              (example: 233-0 English and 233-1 the original other language)

This script downloads the video-only part exactly once and copies it to each new language.
This saves transfer bytes and redownload times.

For example,
  1 suppose a video id as <videoid>
  2 suppose also that videocode 160 is available
  3 suppose also that audio codes are available in dubbed Italian (as 233-5) and in the original English (as 233-9)

Then, this script will:
  1st download the 160 video
  2nd copy it once because one will be used for Italian, the other for English
  3rd download the 160+233-5, yt-dlp recognizes that the video is present and proceeds to download the audio "it" part
  4th download the 160+233-9, idem for "en"

An example of language audiocodes, having English as the original,
    used for one of the channels we've seen (notice that this pattern may not be a general one):

  233-0  mp4 audio only    m3u8 [de-DE] Deutsch (Deutschland) - dubbed-auto
  233-1  mp4 audio only    m3u8 [es-US] es-US - dubbed-auto
  233-2  mp4 audio only    m3u8 [fr-FR] Français (France) - dubbed-auto
  233-3  mp4 audio only    m3u8 [hi] हिन्दी - dubbed-auto
  233-4  mp4 audio only    m3u8 [id] Indonesia - dubbed-auto
  233-5  mp4 audio only    m3u8 [it] Italiano - dubbed-auto
  233-6  mp4 audio only    m3u8 [ja] 日本語 - dubbed-auto
  233-7  mp4 audio only    m3u8 [pl] polski - dubbed-auto
  233-8  mp4 audio only    m3u8 [pt-BR] Português (Brasil) - dubbed-auto
  233-9  mp4 audio only    m3u8 [en-US] American English - original (default)

An example of language audiocodes, having Portuguese as the original,
    used for one of the channels:

  233-0  mp4 audio only    m3u8 [en-US] American English - original (default)
  233-1  mp4 audio only    m3u8 [pt-BR] Português (Brasil) - dubbed-auto

This second case (where English is autodubbed) seems more stable in terms of standardized audiocodes.
The first case (where English is original) seems to differ a little but enough to "miss the point".
  The user has to use the audiocodes parameter to tell the correct audiocodes.
  A programatic discovery via yt-dlp might be done, but as of yet this is not performed by this script.

Notice that in the first example above, the original English is 233-9 and, in the second, English autodubbed, it's 233-0

Limitation: what does this script not do (at least yet)?

  1 it doesn't discover the language codes, even less which codes are available at all
    (the user enters those, this could be a TODO here for these codes are given with the parameter -F in yt-dlp)
  2 it may not be able to check all problems from the command line, but if subprocess returns 0,
    it's a good sign that both the network is working and videos are complete
    if subprocess does not return with 0, a message will be printed out indicating the error,
      but at the time of writing, it just a print-out, the program continues
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
    self.fixed_videoonlyfilename = None
    self.n_on_going_lang = 0

  def treat_input(self):
    verify_ytid_validity_or_raise(self.ytid)
    if self.dlddir_abspath is None:
      self.dlddir_abspath = os.path.abspath('.')
    if self.videoonlycode is None:
      self.videoonlycode = self.DEFAULT_VIDEO_ONLY_CODE

  @property
  def fixed_videoonlyfilepath(self):
    return os.path.join(self.child_tmpdir_abspath, self.fixed_videoonlyfilename)

  @property
  def video_canonical_filepath(self):
    return os.path.join(self.child_tmpdir_abspath, self.video_canonical_filename)

  def get_video_or_audio_filename_with_bksufix(self, n_for_bksufix):
    """
    Example:
      a-videofilename-ytid.f160.mp4.bk3
      bk3 means that it is the 3rd copy of a-videofilename-ytid.f160.mp4
        and is to be used to complement the 3rd audio language file

      Notice that pre-sufix f160 in the example above is a videoonly sufix coming before the extension,
        this latter sufix is a different one and is nicknamed fsufix
    """
    bksufix = f".bk{n_for_bksufix}"
    videofilename_w_bksufix = self.fixed_videoonlyfilename + bksufix
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

  def form_bksufixed_videofilepath_basedonthefsufixvideo(self, nth) -> os.path:
    """
    An example this method does the following: it takes a fsufix video, say:
      a) filename.f160.mp4 (in the example this is self.fixed_videoonlyfilename)
    and appends to it a bksufix, say:
      b) filename.f160.mp4.bk2

    Notice that the forming also considers the dirpath, in a nutshell, the forming is:
      a) INPUT: <dirabspath>/filename.f160.mp4
      b) OUTPUT: <dirabspath>/filename.f160.mp4.bk2
    :param nth:
    :return:
    """
    dot_bksufix = f".bk{nth}"
    next_filename = self.fixed_videoonlyfilename + dot_bksufix
    return os.path.join(self.child_tmpdir_abspath, next_filename)

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
        audiocode = self.audioonlycodes[lang_seq-1]
        trg_filepath = self.form_bksufixed_videofilepath_basedonthefsufixvideo(lang_seq)
        if os.path.isfile(trg_filepath):
          scrmsg = f"""lang={lang_seq} audiocode={audiocode}
           fixed_videoonlyfilename =  {self.fixed_videoonlyfilename}
           HAS ALREADY BEEN COPIED (for complementing later on) to {trg_filepath}"""
          print(scrmsg)
          continue
        shutil.copy2(self.fixed_videoonlyfilepath, trg_filepath)
        scrmsg = f"""lang={lang_seq} audiocode={audiocode}
         fixed_videoonlyfilename =  {self.fixed_videoonlyfilename}
         COPIED (for complementing later on) to {trg_filepath}"""
        print(scrmsg)
    # rename "bk1" at last
    lang_seq = 1
    audiocode = self.audioonlycodes[lang_seq - 1]
    trg_filepath = self.form_bksufixed_videofilepath_basedonthefsufixvideo(lang_seq)
    if os.path.isfile(trg_filepath):
      scrmsg = f"""lang={lang_seq} audiocode={audiocode}
       fixed_videoonlyfilename =  {self.fixed_videoonlyfilename}
       HAS ALREADY BEEN RENAMED (for complementing later on) to {trg_filepath}"""
      print(scrmsg)
      return
    try:
      os.rename(self.fixed_videoonlyfilepath, trg_filepath)
      scrmsg = f"""lang={lang_seq} audiocode={audiocode}
       fixed_videoonlyfilename =  {self.fixed_videoonlyfilename}
       RENAMED (for complementing later on) to {trg_filepath}"""
      print(scrmsg)
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename
      bksufix lang={lang_seq} audiocode={audiocode} 
      to the fixed_videoonlyfilename as: [{self.fixed_videoonlyfilename}]
      => {e}
      """
      raise OSError(errmsg)

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
  def dot_f_videoonlycode(self) -> str:
    """
    Examples of videoonlycodes are: 160 (a 256x144), 602  (another 256x144) etc
    """
    _dot_f_videocode = f'.f{self.videoonlycode}'
    return _dot_f_videocode

  def discover_dld_videofilename(self) -> bool:
    """
    Because a temporary dir is created for the download,
      there expects to be only one videofile
    Then, one looks for one file (and only one) with a video extension
    (for the time being, code 160 or 602 are mp4 - they will be hardcoded for the time being)
    (a second option might be mkv, but this is a TODO for the time being)
    another one is a checking of the current working directory
    """
    filenames = os.listdir('.')  # notice an os.chdir(<dld_dir>) happened before
    videofilenames_soughtfor = list(filter(lambda f: f.endswith('.mp4'), filenames))
    if len(videofilenames_soughtfor) == 0:
      return False
    videofilename_soughtfor = videofilenames_soughtfor[0]
    self.video_canonical_filename = videofilename_soughtfor
    scrmsg = f"Discovered videofilename after download: [{self.video_canonical_filename}]"
    print(scrmsg)
    return True

  def rename_canonical_to_the_fixedvideoonlyfile(self) -> bool:
    """
    Grafts the ".f<number>" sufix before its extension
      for example:
        a) if videoonlycode is 160
        b) then the in-between fsufix will be ".f160"
        c) and a filename example should be like "this-filename.f160.mp4"

    Obs: notice that the nicknamed bksufix is another different one in this class,
         this here is nicknamed fsufix
         this is noted because sometimes at first nod one confuses
           the former [bksufix] with the latter [fsufix]
    """
    name, dot_ext = os.path.splitext(self.video_canonical_filename)
    videoonlyfilename = name + self.dot_f_videoonlycode + dot_ext
    try:
      if os.path.isfile(videoonlyfilename):
        srcmsg = f"Not renaming to videoonlyfilename [{self.video_canonical_filename}] as already exists. Continuing."
        print(srcmsg)
        return False
      os.rename(self.video_canonical_filename, videoonlyfilename)
      self.fixed_videoonlyfilename = videoonlyfilename
      return True
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename
      canonical to videoonlyfilename as: [{self.video_canonical_filename}]
      => {e}
      """
      raise OSError(errmsg)

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

  def rename_bksufixedfile_backtovideoonlyfilename_sothatitcancomposite(self):
    """
    The supposed videofilename is videobasefilename (*) minus its number sufix
    (*) reminding that the video part is only downloaded once,
        every lang video will be formed by just getting its own audiopart as a complement
    For example:
      if  videofile is "this-video-ytid.f160.mp4.bk3"
          then the result videofile should be "this-video-ytid.f160.mp4"
      ie this rename should only remove the ".bk3" sufix
        (actually a removal (rstrip) is not necessary,
          for the canonical-videoonly name is kept in the object (self.fixed_videoonlyfilename)
          so it's just retrieved)
      resulting filename should be this-video-ytid.f160.mp4

    Notice also that self.n_on_going_lang -- keeping the language 1, 2, 3... sequence -- is also
      the number for the bksufix
    """
    n_for_bksufix = self.n_on_going_lang
    videoonly_filename_w_bksufix = self.get_video_or_audio_filename_with_bksufix(n_for_bksufix)
    scrmsg = f"""bksufix = .bk{n_for_bksufix} | renaming:
    FROM:   {videoonly_filename_w_bksufix}
    TO:   {self.fixed_videoonlyfilename}"""
    print(scrmsg)
    # check existence
    srcfilepath = os.path.join(self.child_tmpdir_abspath, videoonly_filename_w_bksufix)
    trgfilepath = os.path.join(self.child_tmpdir_abspath, self.fixed_videoonlyfilename)
    if os.path.isfile(trgfilepath):
      errmsg = f"Error: trgfile [{self.fixed_videoonlyfilename}] for backrename should not be present at this point."
      raise OSError(errmsg)
    try:
      os.rename(srcfilepath, trgfilepath)
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename
      canonical to videoonlyfilename as: [{self.video_canonical_filename}]
      => {e}
      """
      raise OSError(errmsg)

  def download_audiopart_to_fuse_w_videoonly(self):
    """
    One caution here:
      the videoonly_canonical_filename (the one without sufixes) should not be present,
        otherwise yt-dlp will deduce that the composition has already happened,
        so if the videoonly_canonical_filename is present,
        this is an error to be caught (exception to be raised)
    """
    self.rename_bksufixedfile_backtovideoonlyfilename_sothatitcancomposite()  # it's done by removing number sufix
    # now, after the previous rename, the above caution in the docstr can be checked
    if os.path.isfile(self.video_canonical_filepath):
      # oh, oh error
      errmsg = f"""Error:
      the canonical_videoonly_filename [{self.video_canonical_filename}] should not be present in dir,
      otherwise yt-dlp will deduce that the audio+video composite has already happened which it doesn't yet,
        so, in a nutshell, if the canonical_videoonly_filename is present in dir,
        raises this interruption so that one may look up to this problem 
      """
      raise OSError(errmsg)
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
    """
    To troubleshoot:
      video_canonical_filename is wrongly taking the fsufix (ex f160)
      after the first fusion (ie the download of the first audio and formation of the 1st lang video)
    """
    newfilename = f"lang{self.n_on_going_lang} " + self.video_canonical_filename
    trg_filepath = os.path.join(self.child_tmpdir_abspath, newfilename)
    audiocode = self.audioonlycodes[self.n_on_going_lang-1]
    scrmsg = f"""lang={self.n_on_going_lang} | audiocode={audiocode} | renaming:
    FROM: {self.video_canonical_filename}
    TO:   {newfilename}
    """
    print(scrmsg)
    if not os.path.isfile(self.video_canonical_filepath):
      errmsg = f"Error: srcfile [{self.video_canonical_filepath}] for lang-add-rename does not exist."
      raise OSError(errmsg)
    os.rename(self.video_canonical_filepath, trg_filepath)

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
    scrmsg = f"""1st step ->
    POSITION (chdir) at the working tmpdir: [{self.child_tmpdir_abspath}]"""
    print(scrmsg)
    os.chdir(self.child_tmpdir_abspath)
    scrmsg = f"""2nd step ->
    DOWNLOAD the 160 video (ytid={self.ytid})"""
    print(scrmsg)
    self.download_video_only()
    scrmsg = f"""3rd step -> 
    DISCOVER the downloaded video's filename (with ytid={self.ytid}) and rename it to the videoonlyfile
             that one will serve the audio files to later compose audio+video"""
    print(scrmsg)
    self.discover_dld_videofilename()
    self.rename_canonical_to_the_fixedvideoonlyfile()
    scrmsg = f"""4th step ->
    COPY it  (with ytid={self.ytid}) to as many as there are audio lang entered"""
    print(scrmsg)
    self.copy_n_rename_videoonly_n_lang_times()
    scrmsg = f"""5th step ->
    DOWNLOAD (with ytid={self.ytid}) the audio(s) complements | audioonlycodes={self.audioonlycodes}"""
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
