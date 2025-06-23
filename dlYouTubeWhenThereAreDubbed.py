#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

This script uses yt-dlp to download (YouTube) a video in two or more languages if available
  (translations in general are autodubbed)
  (each language forms a separate videofile)

This script accepts the following input:
  1  it receives as input a youtube-video-id (ytid)
  2  alternatively, instead of a ytid, it may receive as input ytids in a text file (whose name is youtube-ids.txt)
  3  it receives as input the videoonlycode (it's only one number, and it's an integer)
  4  it also receives the audioonlycodes for languages (it does not discover them, the user has to enter them)

Observation about standardization of audio format codes:
  As far as we've observed, these codes are not "fully" standardized
    For example, in general, a video that is autodubbed into English
      has sufix "-0" added to its audioonlycode (example: 233-0 or 234-0),
      but if the original audio is already English,
      it seems undeterminate what "dash-number" the YouTube (web) system will give to it
        example: it might be either a "-7", or a "-8" or a "-9"
        (ie, it's not a standard fixed dash-number for all cases)
        the user would have to find out and enter it via the audiocodes parameter

  This script as yet doesn't do an API asking for a mapping of language to audio-only format code

  On the other hand, what seems stable is when English is autodubbed and another language is the original
  In these cases, English gets a "-0" annexed to the audioonlycode and the original language gets a "-1"
    Examples:
       233-0 autodubbed English and 233-1 the original other language
       234-0 autodubbed English and 234-1 the original other language

This script downloads the video-only part exactly once and copies it to each new audio language piece.
This saves transfer bytes and redownload times, because the n-language resulting videos will be formed,
  each one, by joining its videopart (the same for all languages) with its audiopart (language by language).

For example,
  1 suppose a video with available autodubbed translation(s)
  2 suppose also that videoonlycode 160 is available
  3 suppose also that audioonlycodes are available in dubbed Italian (as 233-5) and in the original English (as 233-9)

Then, this script will:
  1st download the 160 video
  2nd copy it once (making two of them) because one will be used for Italian (it), the other for English (en)
  3rd download the 160+233-5, yt-dlp recognizes that the videopart is already present
    and proceeds to download only the audio "it" piece (yt-dlp then blends the audio with the videoonly)
  4th download the 160+233-9, idem for the "en" piece

An example of language audiocodes, having English as the original:
    (seen in a channel we visited) (notice that this pattern may not be a general rule):
    (this example shows only the dash-numbers for the audioonlycode 233)
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

An example of language audiocodes, having Portuguese as the original:
    (seen in another channel we visited):
    (again it only shows the dash-numbers for the audioonlycode 233)
  233-0  mp4 audio only    m3u8 [en-US] American English - original (default)
  233-1  mp4 audio only    m3u8 [pt-BR] Português (Brasil) - dubbed-auto

This second case (where English is autodubbed) seems more stable in terms of standardized audiocodes.
The first case (where English is the original) seems to differ a little among channels
  but enough to "miss the point", at some moment, if applied generally.
The user has to use the audiocodes CLI parameter to tell the correct audiocodes (*).
  The default today uses [233-0, 233-1]
    roughly stable for when English is autodubbed and another language is the original

 (*) to see the full list of CLI parameters for this script, run it with --help

A programatic discovery of these audioonlycodes (mapping language to format code)
  via yt-dlp might be done in the future,
  but as yet this is not performed by this script

Notice as a reemphasis that in the first example above, the original English is 233-9
  and, in the second, English autodubbed, it's 233-0

===========
Limitation: what does this script not do (at least yet)?

  1 it doesn't discover the language codes,
    even less which codes for a certain video are available at all.
    (@see also docstr above)
    (The user may find out available format codes using the
      -F (or --format) parameter in yt-dlp.)
  2 it may not be able to check all problems from the command line, but if subprocess returns 0,
    it's a good sign that both the network is working and videos have "arrived" complete
    if 'subprocess' does not return with 0, at the time of writing,
      the program will halt showing its error message,
    (ie, this script does not yet treat non-0 return cases [*] in a better way)
    [*] imagining mostly that non-O returns are network problems or yt-dlp upgrade needs
"""
import argparse
import os.path
import shutil
import string
import subprocess
import sys
# from localuserpylib.pydates import localpydates as pydates
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
  is_ytid_enc64_compliant = True  # until proven contrary
  # 1 - verify chars are ENC64
  should_not_have_falses = list(map(lambda c: c in enc64_valid_chars, ytid))
  size = len(str(ytid))
  if False in should_not_have_falses:
    is_ytid_enc64_compliant = False
  # 2 - verify charsize is YTID_CHARSIZE (11 at the time of writing)
  if size != YTID_CHARSIZE or not is_ytid_enc64_compliant:
    errmsg = (
      f"""
      Please check the following two problems with ytid (the {YTID_CHARSIZE}-character video id):
      (one or the other or both)

      => ytid = "{ytid}" 

      1 It must have {YTID_CHARSIZE} characters: {len(ytid) == YTID_CHARSIZE}: It has {size}

      2 All its characters should be ENC64
        In "{ytid}", is it ENC64? {is_ytid_enc64_compliant}

      All 64 ENC64 characters are: "{enc64_valid_chars}"

      Please, correct the observations(s) above and retry.
      """
    )
    raise ValueError(errmsg)


class Downloader:

  # class-wide static constants
  DEFAULT_VIDEO_ONLY_CODE = 160
  DEFAULT_AUDIO_ONLY_CODES = ['233-0', '233-1']
  videodld_tmpdirname = 'videodld_tmpdir'
  video_dot_extensions = ['.mp4', '.mkv', '.webm', '.m4v', '.avi', '.wmv']
  # class-wide static interpolable-string constants
  comm_line_base = 'yt-dlp -w -f {compositecode} "{videourl}"'
  video_baseurl = 'https://www.youtube.com/watch?v={ytid}'

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
    self.previously_existing_filenames_in_tmpdir = []
    self.n_ongoing_lang = 0

  def treat_input(self):
    verify_ytid_validity_or_raise(self.ytid)
    if self.dlddir_abspath is None:
      # default is the current working directory
      self.dlddir_abspath = os.path.abspath('.')
    if self.videoonlycode is None:
      # this is the default for the videocode
      self.videoonlycode = self.DEFAULT_VIDEO_ONLY_CODE
    if self.audioonlycodes is None or len(self.audioonlycodes) == 0:
      # this default for the audiocodes generally works when English is autodubbed and another language is the original
      # notice that this script, at the time of writing, does not know about which language is which (@see docstr above)
      self.audioonlycodes = self.DEFAULT_AUDIO_ONLY_CODES

  @property
  def fixed_videoonlyfilepath(self):
    return os.path.join(self.child_tmpdir_abspath, self.fixed_videoonlyfilename)

  @property
  def video_canonical_filepath(self):
    return os.path.join(self.child_tmpdir_abspath, self.video_canonical_filename)

  def get_video_or_audio_filename_with_bksufix(self, n_for_bksufix):
    """
    Example:
      'a-videofilename-ytid.f160.mp4.bk3'
      bk3 means that it is the 3rd copy of a-videofilename-ytid.f160.mp4
        and is to be used to complement the 3rd audio language file

      Notice that pre-sufix f160 in the example above is a videoonly sufix coming before the extension,
        this latter sufix is different and is nicknamed fsufix
    """
    bksufix = f".bk{n_for_bksufix}"
    videofilename_w_bksufix = self.fixed_videoonlyfilename + bksufix
    return videofilename_w_bksufix

  def form_the_fixedvideoonlyfname_w_fsufix_fr_the_canonicalfname(self):
    """
      Let's look at the fsufix with an example:
            a-videofilename-ytid.f160.mp4
      In this example, ".f160" is a videoonly sufix coming before the extension
      (it's videoonly because videoformat code 160 is videoonly, i.e., video without audio)

      So this method does the following:
      a) it takes the canonical filename:
        In the example:
            a-videofilename-ytid.mp4
      b) and grafts (inserts) the ".f160" before the extension
        In the example:
            a-videofilename-ytid.f160.mp4

      Notice that this method does not use the other sufix in this script, the bksuffix (@see above)
    """
    name, dot_ext = os.path.splitext(self.video_canonical_filename)
    dot_fsufix = f".f{self.videoonlycode}"
    fsufixed_filename = f"{name}{dot_fsufix}{dot_ext}"
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
    Obs: The first video is renamed at the end, i.e., the copies are done firstly
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

  def store_files_that_already_exist_into_a_list(self, tmpdir_abspath):
    """
    routine that looked up dateprefix, discontinued later on (kept for history purpose)
      pp = filename.split(' ')
      strdate = pp[0]
      if not pydates.is_strdate_before_today(strdate):
        errmsg = fDate Sufix [{strdate}] in filename is either missing or it's not past today
        raise OSError(errmsg)
    """
    filenames = os.listdir(tmpdir_abspath)
    for filename in filenames:
      if not filename.endswith(tuple(self.video_dot_extensions)):
        continue
      self.previously_existing_filenames_in_tmpdir.append(filename)

  def verify_tmpdir_once_n_store_files_already_existing(self, tmpdir_abspath):
    """
    This method:
      1: creates tmpdir if needed
      2: ignores (jumps over) files that are not video (by extension)
      3: those are video (by extension) have their filenames stored for later finding the downloaded one
      3: in case a video exists with today's date, an OSError exception is raised
    :param tmpdir_abspath:
    :return:
    """
    self.b_verified_once_tmpdir_abspath = False
    os.makedirs(tmpdir_abspath, exist_ok=True)
    self.store_files_that_already_exist_into_a_list(tmpdir_abspath)
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
      self.verify_tmpdir_once_n_store_files_already_existing(tmpdir_abspath)
    return tmpdir_abspath

  @property
  def fsufix(self) -> str:
    """
    Examples of videoonlycodes are: 160 (a 256x144), 602 (another 256x144), etc.
    """
    _fsufix = f"f{self.videoonlycode}"
    return _fsufix

  @property
  def dot_fsufix(self) -> str:
    """
    Examples of videoonlycodes are: 160 (a 256x144), 602 (another 256x144), etc.
    """
    _dot_fsufix = f'.{self.fsufix}'
    return _dot_fsufix

  def fallbackcase_ask_user_what_the_downloaded_filename_is(self):
    scrmsg = f"""Script was not able to find the downloaded filename,
     this can happen when the download had alread happened before,
     please check whether one can be found in the tmpdir and enter it here
     ---------------------------------------------------------------------
     the tmpdir to look up is [{self.child_tmpdir_abspath}]
     ---------------------------------------------------------------------
     In case one cannot be found, type [ENTER] to stop script and
     restart it back up after cleaning up tmpdir (ie leaving the directory empty without files)
     ---------------------------------------------------------------------
     type downloaded filename or [ENTER] => """
    ans = input(scrmsg)
    if ans == '':
      sys.exit(1)
    # check entered filename
    filename = ans
    filepath = os.path.join(self.child_tmpdir_abspath, filename)
    if not os.path.isfile(filepath):
      errmsg = f"""Error:
      entered filename "{filename}" does not exist in tmpdir:
      tmpdir = {self.child_tmpdir_abspath}'
      Please, emtpy this tmpdir directory and retry this program.
      (From an empty dir, script will be able to find the correct downloaded filename.)
      If it tmpdir was already empty, the following two actions may be looked up at:
        a) check network connection 
        b) check the status of the underlying yt-dlp command (it may need upgrading)
      """
      print(errmsg)
      sys.exit(1)
    return filename

  def discover_dld_videofilename(self):
    """
    Because a temporary dir is created for the download,
      one expects there will be only one videofile (*) after the first download happens
        and its name will be just easy to find out by looking dir-contents

    However, this script is also prepared to work with a legacy tmpdir and this poses a problem
      if the sought-for file was already downloaded before running the script
      (because this script does not know what the downloaded filename will be
        except by comparing dir-contents: before and after)

    This method looks for one file (and one only)
      with a video extension (*):
      1 - it looks for a filename that is not inside the previously stored videofilenames list
      2 - if it can't find it (the hypothesis given above), it asks the user for that
      3 - if the user can't find it either, this script then asks for the user to retry after cleaning up tmpdir,
          ie, leaving it empty for the new run

    (*) The extension list for videos is hardcoded for the time being
        i.e., it's a (static) list at the class root level
    """
    allfilenames = os.listdir('.')  # notice an os.chdir(<dld_dir>) happened before
    videofilenames = filter(lambda f: f.endswith('.mp4'), allfilenames)
    videofilenames_appearing_after = list(
      filter(
        lambda f: f not in self.previously_existing_filenames_in_tmpdir,
        videofilenames
      )
    )
    n_results = len(videofilenames_appearing_after)
    if n_results == 0 or n_results > 1:
      videofilename_soughtfor = self.fallbackcase_ask_user_what_the_downloaded_filename_is()
    else:
      videofilename_soughtfor = videofilenames_appearing_after[0]
    self.video_canonical_filename = videofilename_soughtfor
    scrmsg = f"Discovered videofilename after download: [{self.video_canonical_filename}]"
    print(scrmsg)

  def rename_canonical_to_the_fixedvideoonlyfile(self) -> bool:
    """
    Grafts (inserts) the ".f<number>" sufix before its extension,
      for example:
        a) if videoonlycode is 160
        b) then the in-between fsufix will be ".f160"
        c) and a filename example should be like "this-filename.f160.mp4"

    Obs: notice that the nicknamed bksufix is another different one in this class,
         this here is nicknamed fsufix
         this is noted because sometimes at first nod one confuses
           the former [bksufix] with the latter [fsufix]
           and this bksufix is not used in this method
    """
    self.fixed_videoonlyfilename = self.form_the_fixedvideoonlyfname_w_fsufix_fr_the_canonicalfname()
    if os.path.isfile(self.fixed_videoonlyfilename):
      srcmsg = f"""Not renaming to fixed_videoonlyfilename [{self.video_canonical_filename}] as it already exists.
      Continuing."""
      print(srcmsg)
      return False
    try:
      os.rename(self.video_canonical_filename, self.fixed_videoonlyfilename)
      return True
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename
      canonical to fixed_videoonlyfilename as: [{self.video_canonical_filename}]
      => {e}
      """
      raise OSError(errmsg)

  def download_video_only(self):
    """
    This method download the videoonlyfile via yt-dlp using subprocess.run()

    At the time of this writing, when subprocess raises subprocess.CalledProcessError
      the script wraps it up with an additional error-message and raises ValueError

    [For later on]
    This may be improved later on if some hypotheses for the
      subprocess.CalledProcessError exception allow this program to continue on
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
      errmsg = f"""Command: [{comm}]
       failed with return code: [{e.returncode}]
       => {e}"""
      print(errmsg)
      raise ValueError(errmsg)
    except KeyboardInterrupt:
      scrmsg = "Interrupted by user. Exiting loop. Continuing."
      print(scrmsg)
    return True

  def form_stocked_videoonlyfilename_w_fsufix_n_bksufix(self, nsufix):
    """
    This method is not in use (with the IDE, clicking it goes nowhere),
      but a future refactoring may put this in use
    """
    dot_bksufix = f".bk{nsufix}"
    name, dot_ext = os.path.splitext(self.video_canonical_filename)
    stocked_videoonlyfilename_w_fsufix_n_bksufix = f"{name}{self.dot_fsufix}{dot_ext}{dot_bksufix}"
    return stocked_videoonlyfilename_w_fsufix_n_bksufix

  def fallback_try_find_samecanonicalpath_w_different_ext(self):
    """
    It's already known at this point that the canonical filepath
      (self.video_canonical_filepath)
      is not present in dir.
    Chances are that its extension is now a different.
    Example: instead of mp4, it's not mkv
      (the blending of audio+video may change a previous extension)
    This method tries to find a same canonical name with a different extension
    :return:
    """
    soughtfor_alt_filepath = None
    canoname, a_previous_dot_ext = os.path.splitext(self.video_canonical_filename)
    extensions = list(self.previously_existing_filenames_in_tmpdir)
    extensions.remove(a_previous_dot_ext)
    # look up one among "all" available
    while len(extensions) > 0:
      next_dot_ext = extensions.pop()
      # recompose filename with new extension
      soughtfor_alt_filename = f"{canoname}{next_dot_ext}"
      soughtfor_alt_filepath = os.path.join(folderpath, soughtfor_alt_filename)
      if not os.path.isfile(soughtfor_alt_filepath):
        return soughtfor_alt_filepath
    errmsg = (f"Error: canonical file [{self.video_canonical_filename}] is not present in dir "
              f"for the langN prefix prepending rename. Script cannot continue,"
              f"but the last video downloaded is probably complete on folder. Halting.")
    raise OSError(errmsg)

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

    Notice also that self.n_on_going_lang -- keeping language 1, 2, 3... sequence -- is also
      the number for the bksufix

    Cases where extensions are not '.mp4'
    =====================================

    When a 'fused' video (fusion is the junction of audio with video),
      joining an audio that will generated a different extension
      (say mkv) than the first ones (say mp4), this last rename will not
      find the correct filename. At the same time, this script does not
      know which combinations generate which extensions.
    To solve this, the system falls back looking to
      a second file with the same name, i.e.,
        filename-video-such-and-such-ytid.mp4
        filename-video-such-and-such-ytid.mkv
      then, with the name part of the filename, the mkv one may be found.
    """
    n_for_bksufix = self.n_ongoing_lang
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

  def fallback_to_nondashed_audiocode_changing_it(self):
    """
    The strategy here is the following:

    1 when languages are asked in the audiocodes parameters,
      they are "dash-sufixed", for example

      ['233-0', '233-1'] or ['233-5', '233-9']

      (The hypothesis below is not guaranteed, but this program will try it.)

      When 'subprocess' returns non-0, there's a change the video does
        not have language variations which might be also deduced
        that audiocode 233 could work and form the video in its original language.
        That would complete the job if the video does not have another language anyway.
    """
    try:
      # position to new logical next self.n_ongoing_lang
      # if it was already the last, the exception will handle it
      audiocodestr = self.audioonlycodes[self.n_ongoing_lang]
      pp = audiocodestr.split('-')
      newaudiocode = pp[0]
      self.audioonlycodes[self.n_ongoing_lang] = newaudiocode
    except IndexError:
      scrmsg = f"""WARNING: 
      could not derive a non-dashed-sufix.
        => audioonlycodes = {self.audioonlycodes}
      Returning."""
      print(scrmsg)

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
      otherwise yt-dlp will deduce that the audio+video composite has already happened which it doesn't yet.
      
      The user should check whether this file is the final one or
        in case it's not, something might be incorrect with this script
        (or network or yt-dlp's underlying version).
      
      Notice also that the canonical filename will be, at the end,
        prepended with "lang<n>" (lang1, lang2, etc.)
      The user may rename it to a different pattern because this script is,
        at moment of writing, agnostic of the audiocode-to-language mapping.
        (Ignore this last paragraph if this system can already find out 
          about the audiocode-to-language mapping.) 
      """
      raise OSError(errmsg)
    audiocode = self.audioonlycodes[self.n_ongoing_lang - 1]
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
      errmsg = f"""
      =+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|
      Subprocess returned with an error:
      Command failed with return code {e.returncode}: {comm}
      full error msg => {e}
      => trying a download with an audiocode with the dashed-sufix
      =+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|=+=|
      """
      print(errmsg)
      self.fallback_to_nondashed_audiocode_changing_it()
    except KeyboardInterrupt:
      print("Interrupted by user. Exiting loop.")

  def rename_videofile_after_audiovideofusion(self):
    """
    To troubleshoot:
      video_canonical_filename is wrongly taking the fsufix (ex f160)
      after the first fusion (i.e., the download of the first audio and formation of the 1st lang video)
    """
    newfilename = f"lang{self.n_ongoing_lang} " + self.video_canonical_filename
    trg_filepath = os.path.join(self.child_tmpdir_abspath, newfilename)
    audiocode = self.audioonlycodes[self.n_ongoing_lang - 1]
    scrmsg = f"""lang={self.n_ongoing_lang} | audiocode={audiocode} | renaming:
    FROM: {self.video_canonical_filename}
    TO:   {newfilename}
    """
    print(scrmsg)
    if not os.path.isfile(self.video_canonical_filepath):
      self.fallback_try_find_samecanonicalpath_w_different_ext()
      errmsg = f"Error: srcfile [{self.video_canonical_filepath}] for lang-add-rename does not exist."
      raise OSError(errmsg)
    os.rename(self.video_canonical_filepath, trg_filepath)

  def download_audio_complements(self):
    """
    self.n_on_going_lang is an instance variable that controls lang orderseq throughout the class
    """
    for self.n_ongoing_lang in range(1, self.n_langs + 1):
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
  audioonlycodes = args.audioonlycodes or []
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
  scrmsg = f'Entered ytid(s) is/are: {ytids}'
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
