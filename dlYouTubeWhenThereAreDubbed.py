#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

This script uses yt-dlp to download (YouTube) a video in two or more languages if available
  (translations in general are autodubbed)
  (each language forms a separate videofile)

Usage:
======
  $dlYouTubeWhenThereAreDubbed.py [--ytid <ytid or yturl within "">]
    [--useinputfile]
    [--videoonlycode <video-format-number>]
    --audioonlycodes <list of audio-format-codes>

Where:
  <ytid> => the ENCODE64 11-character YouTube video id
    or a youtube-style URL with one but in the latter case
      it should come within "" (quotes) if it has an "&" (ampersand character)
      obs: the use of parameter --useinputfile looks for ytid's
           in a file named youtube-ids.txt in the working directory and ignores --ytid
  <video-format-number> => an integer representing the video-only-format
    default: this parameter defaults to 160 (a video-only-code having 256x144 resolution)
  <list of audio-format-codes> => a list of all audio-only-codes desired for the yt-dlp downloads

Example:
========
  $dlYouTubeWhenThereAreDubbed.py --ytid abcABC123-_
    --audioonlycodes 233-0,233-1

The above example 'automatizes' the following two yt-dlp downloads:
  $yt-dlp -w -f 160+233-0 abcABC123-_
  $yt-dlp -w -f 160+233-1 abcABC123-_

The result will be the download of two videofiles: one with the language audio 233-0
  and the other with the language audio 233-1 (be they original or autodubbed)
This automatization also takes care of the renaming needed
  because yt-dlp does not differentiate filenames by language audio

Care with the use of parameter --useinputfile:
=============================================
  if the user wants to download many videos at once, it can be done with --useinputfile,
    suffice a youtube-ids.txt is created with all the ytid's consolidated
  however, this script (and this is reinforced below) does not know beforehand if a video
   has or doesn't have a specific language for it.

Explanation
===========

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
  233-0  mp4 audio only    m3u8 [en-US] American English - dubbed-auto
  233-1  mp4 audio only    m3u8 [pt-BR] Português (Brasil) - original (default)

This second case (where English is autodubbed) seems more stable in terms of standardized audiocodes.
The first case (where English is the original) seems to differ "a little" among channels,
  though "a little", it's enough to "miss the point", at some moment, if applied generally.
The user has to use the audiocodes CLI parameter to tell the correct audiocodes (*).
  The default today uses [233-0, 233-1]
    roughly stable for when English is autodubbed and another language is the original

 (*) to see the full list of CLI parameters for this script, run it with --help
     (or scroll up the text to the beginning)

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
import re
import shutil
import string
import subprocess
import sys
import localuserpylib.ytfunctions.yt_sufix_lang_map_fs as ytsufixlang
DEFAULT_AUDIOVIDEO_CODE = 160
DEFAULT_AUDIOVIDEO_DOT_EXT = '.mp4'
DEFAULT_YTIDS_FILENAME = 'youtube-ids.txt'
REGISTERED_VIDEO_DOT_EXTENSIONS = ['.mp4', '.mkv', '.webm', '.m4v', '.avi', '.wmv']
YTID_CHARSIZE = 11
enc64_valid_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + '_-'
# Example for the regexp below: https://www.youtube.com/watch?v=abcABC123_-&pp=continuation
ytid_url_regexp_pattern = r'watch\?v=([A-Za-z0-9_-]{11})(?=(&|$))'
cmpld_ytid_url_re_pattern = re.compile(ytid_url_regexp_pattern)
ytid_in_ytdlp_filename_pattern = r'\[([A-Za-z0-9_-]{11})\]'
cmpld_ytid_in_ytdlp_filename_pattern = re.compile(ytid_in_ytdlp_filename_pattern)
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


def is_str_enc64(line: str | None) -> bool:
  blist = list(map(lambda c: c in enc64_valid_chars, line))
  if False in blist:
    return False
  return True


def is_str_a_ytid(ytid: str | None) -> bool:
  if ytid is None or len(ytid) != YTID_CHARSIZE:
    return False
  return is_str_enc64(ytid)


def extract_ytid_from_yturl_or_itself_or_none(p_supposed_ytid: str | None) -> str | None:
  """
  Extracts ytid from a larger string (incluing a URL)
  Noting:
    if ytid is None, return None
    if ytid is already "in shape", return it as is
    if ytid is a larger string, try to extract a valid "ytid" from it
    if extraction fails, return None

  Example of an extraction from a yt_url:
    url = "https://www.youtube.com/watch?v=abcABC123_-&pp=continuation"
  The extraction result is:
    ytid = "abcABC123_-"

    Obs: "abcABC123_-" in the example is hypothetical (an ENC64 11-char string)!
  """
  if p_supposed_ytid is None:
    return None
  if is_str_a_ytid(p_supposed_ytid):
    ytid = p_supposed_ytid
    return ytid
  match = cmpld_ytid_url_re_pattern.search(p_supposed_ytid)
  return match.group(1) if match else None


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
  if not is_str_a_ytid(ytid):
    errmsg = (
      f"""
      Please check the value entered for/with ytid
        => its entered value is "{ytid}"

      Rules for a valid ytid:
      =======================
      a) it must have {YTID_CHARSIZE} characters
      b) all of them must be ENC64 *

      * All 64 ENC64 characters are: "{enc64_valid_chars}"

      Please, correct the observations(s) above and retry.
      """
    )
    raise ValueError(errmsg)


class OSEntry:
  """
  This class organizes the OSEntries (files and folders) needed for the Downloader class below
  This class is used by composition by the latter
  """

  def __init__(self, workdir_abspath, basefilename, videoonly_or_audio_code):
    self.name, self.dot_ext = None, None
    self._basefilename = None
    self.basefilename = basefilename
    if videoonly_or_audio_code is None:
      self.videoonly_or_audio_code = DEFAULT_AUDIOVIDEO_CODE
    else:
      self.videoonly_or_audio_code = videoonly_or_audio_code
    self.workdir_abspath = workdir_abspath
    self.treat_workdir_abspath()

  def treat_workdir_abspath(self):
    if self.workdir_abspath is None or self.workdir_abspath == '.':
      self.workdir_abspath = os.path.abspath('.')
      return
    if not os.path.isdir(self.workdir_abspath):
      # this directory is set at client Class Downloader and passed on here
      # but at this instantiation time chances are it may still need to be made (mkdir)
      os.makedirs(self.workdir_abspath, exist_ok=True)
      return
    if not os.path.isdir(self.workdir_abspath):
      # this is a logical condition that it will probably never happen
      # for an exception should have probably been already raised above
      errmsg = f"Error: workdir_abspath {self.workdir_abspath} does not exist. Please, retry reentering it."
      raise OSError(errmsg)

  @property
  def basefilename(self):
    """
    basefilename is video filename as it comes from yt-dlp
      In this class:
        1 - it's the same as fn_as_name_ext
        2 - and also decomposable as "{name}{dot_ext}"
    it could be further decomposed because of the video-id sufixing the name,
      but that goes for a different method below (TODO)
    :return:
    """
    return self.fn_as_name_ext

  @basefilename.setter
  def basefilename(self, filename):
    if filename is None:
      # this should happen at the beginning when filename is not yet known
      return
    self.name, self.dot_ext = os.path.splitext(filename)
    if self.dot_ext not in REGISTERED_VIDEO_DOT_EXTENSIONS:
      errmsg = (f"extension {self.dot_ext} not in the REGISTERED_VIDEO_DOT_EXTENSIONS"
                f" list = {REGISTERED_VIDEO_DOT_EXTENSIONS}")
      raise OSError(errmsg)

  @property
  def ytid(self) -> str | None:
    """
    The attribute is the ytid (youtube-video-id)

    Important:
      a) the way ytid is extracted here from the filename is the convention (*) used in yt-dlp
      b) there is another convention used in the older ytdl project, this is still
         used in some of our scripts
      c) because this script looks up the downloaded file from yt-dlp,
         the correct convention is the one in 'a' above
      (*) the convention is to have the 11-char ytid enclosed within "[]" at the end of name

    ------------------
    # [ALTERNATIVELY] code to try find ytid (the ENC64 11-character id) via RegExp
    match = cmpld_ytid_in_ytdlp_filename_pattern.search(self.name)
    self.ytid = match.group(1) if match else None
    """
    try:
      sufix = self.name[-13:]
      ytid = sufix.lstrip('[').rstrip(']')
      if not is_str_a_ytid(ytid):
        return None
      return ytid
    except (IndexError, ValueError):
      return None

  @property
  def fsufix(self) -> str:
    """
    Examples of videoonlycodes are: 160 (a 256x144), 602 (another 256x144), etc.
    A fsufix is the string "f" + str(videoonly_or_audio_code)
    With the example above fsufix = "f160"
    """
    _fsufix = f"f{self.videoonly_or_audio_code}"
    return _fsufix

  @property
  def dot_fsufix(self) -> str:
    """
    It prepends a "." (dot) before fsufix (@see it above)
    """
    _dot_fsufix = f'.{self.fsufix}'
    return _dot_fsufix

  @property
  def fn_as_name_ext(self) -> str:
    name_ext = f"{self.name}{self.dot_ext}"
    return name_ext

  @property
  def fp_for_fn_as_name_ext(self) -> os.path:
    return os.path.join(self.workdir_abspath, self.fn_as_name_ext)

  @property
  def fn_as_name_fsufix_ext(self) -> str:
    """
    name_fsufix_ext means the canonical filename with the f<videoonlycode> sufix.

    An example:
      title.f160.ext.bk3

    For example, parts after title are:
      f160 => an "f" followed by the videoonlycode
      ext => the current extension
      bk3 => means it's the 3rd copy of the videoonlyfile that will compose with a 3rd language audio file

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
    name_fsufix_ext = f"{self.name}{self.dot_fsufix}{self.dot_ext}"
    return name_fsufix_ext

  @property
  def name_from_fn_as_name_fsufix_ext(self) -> str:
    """
    For example:
      name:
        from "a-videofilename-ytid.f160.mp4"
          is "a-videofilename-ytid.f160"
    :return:
    """
    name, _ = os.path.splitext(self.fn_as_name_fsufix_ext)
    return name

  @property
  def fp_for_fn_as_name_fsufix_ext(self) -> os.path:
    return os.path.join(self.workdir_abspath, self.fn_as_name_fsufix_ext)

  @staticmethod
  def get_dot_bksufix(n_bksufix) -> str:
    """
    This method composes a bksufix-fsufix audio|video filename
    This filename is composed with the following chunks:
      "{name}{dot_fsufix}{dot_ext}{dot_bksufix}"
    Where:
      {name} is the name part of the filename altogether
      {dot_fsufix} is a dot, followed by "f" followed by the videoonlycode
        * it could also be an audioonlycode, but in this clas, its main use aims the vocode
      {dot_ext} is a dot followed by the file-extension
      {dot_bksufix} is a dot, followed by "bk" followed by a sequence number

    Example:
      name = "this-video"
      dot_fsufix = ".f160"
      dot_ext = ".mp4"
      dot_bksufix = ".bk3"
    This will compose as:
      "this-video.f160.mp4.bk3"
    """
    _dot_bksufix = f".bk{n_bksufix}"
    return _dot_bksufix

  def get_fn_as_name_fsufix_ext_bksufix(self, n_bksufix) -> str:
    """
    An example of a filename name_fsufix_ext_bksufix is as follows:
      it takes a fsufix video, say, videoonlycode=160 (a 256x144 video), forming:

      a) filename.f160.mp4 (in the example, this is self.fsufixed_videoonlyfilename)
    and appends to it a bksufix, say:
      b) filename.f160.mp4.bk2

    Notice that the forming also considers the dirpath, in a nutshell, the forming is:
      a) INPUT: <dirabspath>/filename.f160.mp4
      b) OUTPUT: <dirabspath>/filename.f160.mp4.bk2
    """
    name_fsufix_ext_bksufix = f"{self.fn_as_name_fsufix_ext}{self.get_dot_bksufix(n_bksufix)}"
    return name_fsufix_ext_bksufix

  def get_fp_for_fn_as_name_fsufix_ext_bksufix(self, n_bksufix) -> os.path:
    return os.path.join(self.workdir_abspath, self.get_fn_as_name_fsufix_ext_bksufix(n_bksufix))

  def rename_canofile_to_next_available_lang_n_prefixed_or_raise(self):
    """
    This method renames existing canofile to the next available langN prefix
    if prefix gets greater than 1000, raise an exception
    """
    canofilepath = self.fp_for_fn_as_name_ext
    if not os.path.isfile(canofilepath):
      # nothing to do, return
      return
    n_iter, max_iter = 0, 1000
    changing_filepath = canofilepath
    while os.path.isfile(changing_filepath):
      n_iter += 1
      if n_iter > max_iter:
        canofilename = self.fn_as_name_ext
        _, changing_filename = os.path.split(changing_filepath)
        errmsg = (f"Maximum iteration cycles reaches when trying to rename {canofilename}"
                  f" | {changing_filename} | {changing_filepath}")
        raise OSError(errmsg)
      _, changing_filename = os.path.split(canofilepath)
      prefix = f"lang{n_iter} "
      changing_filename = prefix + changing_filename
      changing_filepath = os.path.join(self.workdir_abspath, changing_filename)
    try:
      os.rename(canofilepath, changing_filepath)
      scrmsg = f"""Rename succeeded for incrementing langN prefix to canofile
      ---------------------------------------
      FROM (canofilepath):    [{canofilepath}]
      TO (changing_filepath): [{changing_filepath}]
      ---------------------------------------
      """
      print(scrmsg)
    except (OSEntry, IOError) as e:
      errmsg = f"""Error: could not rename canofile to next available prefix
      ---------------------------------------
      FROM (canofilepath):    [{canofilepath}]
      TO (changing_filepath): [{changing_filepath}]
      ---------------------------------------
      {e}
      Halting.    
      """
      print(errmsg)
      sys.exit(1)
    return

  def __str__(self):
    bksufix_example = 3
    outstr = f"""OSEntry object:
    name_ext = [{self.fn_as_name_ext}]
    fp_name_ext = [{self.fp_for_fn_as_name_ext}]
    ytid = [{self.ytid}]
    workdir = [{self.workdir_abspath}]
    --------------------------------
    name_fsufix_ext = [{self.fn_as_name_fsufix_ext}]
    fp_name_fsufix_ext = [{self.fp_for_fn_as_name_fsufix_ext}]
    --------------------------------
    Example with bksufix = [{bksufix_example}]
    name_fsufix_ext_bksufix[{bksufix_example}] = {self.get_fn_as_name_fsufix_ext_bksufix(bksufix_example)}
    fp_name_fsufix_ext = [{self.get_fp_for_fn_as_name_fsufix_ext_bksufix(bksufix_example)}]
    """
    return outstr


class Downloader:

  # class-wide static constants
  DEFAULT_VIDEO_ONLY_CODE = 160
  DEFAULT_AUDIO_ONLY_CODES = ['233-0', '233-1']
  videodld_tmpdirname = 'videodld_tmpdir'
  video_dot_extensions = REGISTERED_VIDEO_DOT_EXTENSIONS
  DEFAULT_DOT_EXTENSION = '.mp4'
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
    self.ytsufixlang_o = ytsufixlang.SufixLanguageMapFinder(self.audioonlycodes)
    self.b_verified_once_tmpdir_abspath = None
    self.video_canonical_name = None  # this is the video filename with the f-sufix, it's known after download
    self._cur_dot_ext = None
    self.cur_dot_ext = self.DEFAULT_DOT_EXTENSION
    self.previously_existing_filenames_in_tmpdir = []
    self.n_ongoing_lang = 0
    self.lang_map = {}  # this dict has {sufix: 2-letter-langid}
    self.osentry = OSEntry(
      workdir_abspath=self.child_tmpdir_abspath,
      basefilename=None,  # later to be known
      videoonly_or_audio_code=self.videoonlycode
    )
    # self.va_osentry = []

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
  def n_langs(self):
    if self.audioonlycodes is None:
      return 0
    return len(self.audioonlycodes)

  @property
  def videourl(self):
    pdict = {'ytid': self.ytid}
    url = self.video_baseurl.format(**pdict)
    return url

  def get_lang2lettercode_fr_audioonlycode(self, audioonlycode):
    """
    audioonlycode = self.audioonlycodes[self.n_ongoing_lang-1]
    """
    return self.ytsufixlang_o.get_lang2lettercode_fr_audioonlycode(audioonlycode)

  def rename_canofile_to_the_bk1sufixed(self):
    """
    The canonical filename (the one downloaded) gets renamed to the bk1_sufixed filename
      for the first language available
    :return:
    """
    srcfilepath = self.osentry.fp_for_fn_as_name_fsufix_ext
    srcfilename = self.osentry.fn_as_name_fsufix_ext
    audiocode = self.audioonlycodes[0]  # index 0 is the first language
    trgfilepath = self.osentry.get_fp_for_fn_as_name_fsufix_ext_bksufix(1)
    trgfilename = self.osentry.get_fn_as_name_fsufix_ext_bksufix(1)
    if not os.path.isfile(srcfilepath):
      scrmsg = f"""Cannot rename | lang=1 audiocode={audiocode}
        FROM canofilename = [{srcfilename}]
        TO bk1sufixfilename = [{trgfilename}]
          => reason: because {srcfilename} does not exist in folder. Halting.
      """
      print(scrmsg)
      sys.exit(1)
    if os.path.isfile(trgfilepath):
      scrmsg = f"""Already renamed | lang=1 audiocode={audiocode}
        -------------------- 
        FROM (canofilename)  : [{srcfilename}]
        TO (bk1sufixfilename): [{trgfilename}]
        -------------------- 
          => reason: because {trgfilename} exists in folder. Continuing.
      """
      print(scrmsg)
      return
    try:
      os.rename(srcfilepath, trgfilepath)
      print("Renamed accomplished")
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename bksufix lang=1 audiocode={audiocode} 
      => {e}

      Halting.
      """
      print(errmsg)
      sys.exit(1)

  def copy_n_rename_videoonly_n_lang_times(self):
    """
    The first video is just renamed to sufix "bk<seq>" where seq is the audio sequential number
    The following videos are copied each one with its "bk<seq>" sufix
    Obs: The first video is renamed at the end, i.e., the copies are done firstly
    """
    if self.n_langs == 0:
      #  nothing to rename, return
      return
    # the path below represents the video filename as downloaded
    # the first one is a rename
    self.rename_canofile_to_the_bk1sufixed()
    if self.n_langs == 1:
      # done, return
      return
    # at this point, bk1 exists due to the previous rename (the method called above in this)
    srcfilepath = self.osentry.get_fp_for_fn_as_name_fsufix_ext_bksufix(1)
    srcfilename = self.osentry.get_fn_as_name_fsufix_ext_bksufix(1)
    if not os.path.isfile(srcfilepath):
      errmsg = f"Error: srcfilename [{srcfilename}] for copying bk's does not exist."
      print(errmsg)
      sys.exit(1)
    for i in range(1, self.n_langs):
      lang_seq = i + 1
      audiocode = self.audioonlycodes[i]
      trgfilepath = self.osentry.get_fp_for_fn_as_name_fsufix_ext_bksufix(lang_seq)
      trgfilename = self.osentry.get_fn_as_name_fsufix_ext_bksufix(lang_seq)
      scrmsg = f"""[copying bk1 to the bk{lang_seq} audiocode={audiocode}]
        -------------------- 
        FROM:  {srcfilename}
        TO:    {trgfilename}
        -------------------- 
      """
      print(scrmsg)
      if os.path.isfile(trgfilepath):
        scrmsg = f"Continuing: trgfilename [{trgfilename}] already exists."
        print(scrmsg)
        continue
      try:
        shutil.copy2(srcfilepath, trgfilepath)
      except (IOError, OSError) as e:
        errmsg = f"""Error: the copying above failed
          -------------------- 
          FROM:  {srcfilename}
          TO:    {trgfilename}
          -------------------- 
        {e}
        Halting.
        """
        print(errmsg)
        sys.exit(1)

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
    The actions/tasks of the script happen in a newly created (intended to be temporary) directory
      (or if previously created, files should have a previous-date prefix, otherwise this script should be interrupted)

    The composition-class OSEntry also has it from here
    To avoid an "origins" bug, it may be advisable to always read it from OSEntry (though the two are the same)
    :return:
    """
    tmpdir_abspath = os.path.join(self.dlddir_abspath, self.videodld_tmpdirname)
    if not self.b_verified_once_tmpdir_abspath:
      self.verify_tmpdir_once_n_store_files_already_existing(tmpdir_abspath)
    return tmpdir_abspath

  def fallbackcase_ask_user_what_the_downloaded_filename_is(self):
    scrmsg = f"""Script was not able to find the downloaded filename,
     this can happen when the download had alread happened before,
     please check whether one can be found in the tmpdir and enter it here
     ---------------------------------------------------------------------
     the tmpdir to look up is [{self.osentry.workdir_abspath}]
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
    filepath = os.path.join(self.osentry.workdir_abspath, filename)
    if not os.path.isfile(filepath):
      errmsg = f"""Error:
      entered filename "{filename}" does not exist in tmpdir:
      tmpdir = {self.osentry.workdir_abspath}'
      Please, emtpy this tmpdir directory and retry this program.
      (From an empty dir, script will be able to find the correct downloaded filename.)
      If it tmpdir was already empty, the following two actions may be looked up at:
        a) check network connection 
        b) check the status of the underlying yt-dlp command (it may need upgrading)
      """
      print(errmsg)
      sys.exit(1)
    return filename

  def discover_dldd_videofilename(self):
    """
    The old discovery method was based on a comparison before versus after.
    This new one is based on searching for a file with ytid in its name.
    """
    filenames = os.listdir(self.osentry.workdir_abspath)
    filenames = filter(lambda f: self.ytid in f, filenames)
    filenames = list(filter(lambda f: f.endswith(tuple(self.video_dot_extensions)), filenames))
    if len(filenames) == 1:
      filename_found = filenames[0]
      scrmsg = f"""At after-download file discovery:
      ytid = {self.ytid}
      found = {filename_found}"""
      print(scrmsg)
    else:
      filename_found = self.fallbackcase_ask_user_what_the_downloaded_filename_is()
    self.osentry.basefilename = filename_found

  def discover_dldd_videofilename_old(self):
    """
    Because a temporary dir is created for the download,
      one expects there will be only one videofile (*) after the first download happens
        and its name will be just easy to find out by looking dir-contents

    However, this script is also prepared to work with a legacy tmpdir (perhaps having mix files)
      and this poses a problem:
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
        i.e., it's a (static attribute) list at the class root level
    """
    allfilenames = os.listdir('.')  # notice an os.chdir(<dld_dir>) happened before
    dot_ext = self.cur_dot_ext
    videofilenames = filter(lambda f: f.endswith(dot_ext), allfilenames)
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
    scrmsg = f"osentry.basefilename videofilename_soughtfor = {videofilename_soughtfor}"
    print(scrmsg)
    self.osentry.basefilename = videofilename_soughtfor
    scrmsg = f"Discovered videofilename after download: [{self.osentry.fn_as_name_ext}]"
    print(scrmsg)

  def rename_from_canonical_to_fsufixedvideoonlyfile(self) -> bool:
    """
    Grafts (inserts) the ".f<number>" sufix before its extension,
      for example:
        a) if videoonlycode is 160
        b) then the in-between fsufix will be ".f160"
        c) and a filename example should be like "this-filename.f160.mp4"

    Obs: notice that the nicknamed bksufix is another different one in this object-class,
         this here is nicknamed fsufix
         this is noted because sometimes at first nod one confuses
           the former [bksufix] with the latter [fsufix]
           and this bksufix is not used in this method
    """
    if os.path.isfile(self.osentry.fp_for_fn_as_name_fsufix_ext):
      scrmsg = f"""Not renaming to fsufixed_videoonlyfilename [{self.osentry.fn_as_name_fsufix_ext}]
       as it already exists. Continuing."""
      print(scrmsg)
      return False
    try:
      os.rename(self.osentry.fp_for_fn_as_name_ext, self.osentry.fp_for_fn_as_name_fsufix_ext)
      scrmsg = f"""Rename succeeded (from canonical to f-sufixed).
      FROM (canonical): [{self.osentry.fn_as_name_ext}]
      FROM (f-sufixed): [{self.osentry.fn_as_name_fsufix_ext}]"""
      print(scrmsg)
      return True
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename
      canonical to fsufixed_videoonlyfilename i.e.,
      FROM : [{self.osentry.fn_as_name_ext}]
      TO   : [{self.osentry.fn_as_name_fsufix_ext}]
      => {e}
      """
      raise OSError(errmsg)

  def download_video_only(self):
    """
    This method downloads the videoonlyfile via yt-dlp using Python's subprocess.run()

    At the time of this writing, when subprocess raises subprocess.CalledProcessError
      the script wraps it up with an additional error-message and then reraises ValueError

    [For later on]
    This may be improved later on if some hypotheses for the
      subprocess.CalledProcessError exception allow this program to continue on
    """
    strdict = {'compositecode': self.videoonlycode, 'videourl': self.videourl}
    comm = self.comm_line_base.format(**strdict)
    scrmsg = f"@download_video_only | {comm}"
    print(scrmsg)
    try:
      """
      ans = input('Run this command above (Y/n) ? [ENTER] means Yes')
      if ans not in ['Y', 'y', '']:
        return False
      """
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

  def find_existfilepath_of_samecanonicalfilename_w_different_ext_or_none(self):
    """
    At this point, the canonical filepath (with the name created by yt-dlp)
      is not present in dir.
    Chances are its extension got changed with a different combination of audio and video fusion.

    Example: instead of mp4, it may now be mkv
      (the blending of audio+video may have changed a previous extension)

    This method tries to find a same canonical name with a different extension

    Obs:
      a) the approach this method tries is to look up different extensions with the same name
      b) another approach would be to try to use the ytid itself sufixed to name

    """
    canoname = self.osentry.fn_as_name_ext
    curr_dot_ext = self.osentry.dot_ext
    extensions = list(self.video_dot_extensions)
    try:
      # remove the extension it already has, go look up a matching one among the remaining ones
      extensions.remove(curr_dot_ext)
    except ValueError:
      pass
    # look up if there are still extensions in the list
    while len(extensions) > 0:
      next_dot_ext = extensions.pop()
      # recompose filename with new extension
      soughtfor_alt_filename = f"{canoname}{next_dot_ext}"
      soughtfor_alt_filepath = os.path.join(self.osentry.workdir_abspath, soughtfor_alt_filename)
      if os.path.isfile(soughtfor_alt_filepath):
        # found it
        self.cur_dot_ext = next_dot_ext
        return soughtfor_alt_filepath
    return None

  def rename_bksufixedfilename_to_fsufixedfilename_to_avoid_the_vo_redownload(self):
    """
    The supposed videofilename is videobasefilename (*) minus its number sufix
    (*) reminding that the videopart (the audioless video) is only downloaded once,
        every language video will be formed by just getting extra its own audiopart as a complement
    For example:
      if  audiolessvideofile is "this-video-ytid.f160.mp4.bk3"
          then it needs just to strip the bk3 sufix, resulting "this-video-ytid.f160.mp4"
      ie this rename should only remove the ".bk3" sufix
      Because extensions may very, a rstrip() strategy is preferrable

    Notice also that self.n_on_going_lang -- keeping language 1, 2, 3... sequence -- is also
      the number for the bksufix

    Cases where extensions are not '.mp4'
    =====================================

    When a 'fused' video (fusion is the junction of audio with video),
      joining an audio that will generate a different extension
      (say mkv) than the first ones (say mp4), this last rename will not
      find the correct filename. At the same time, this script does not
      know which combinations generate which extensions.
    To solve this, the system falls back looking to
      a second file with the same name, i.e.,
        filename-video-such-and-such-ytid.mp4
        filename-video-such-and-such-ytid.mkv
      then, with the name part of the filename, the mkv one -- in another one in the set -- may be found.
    """
    srcfilepath = self.osentry.get_fp_for_fn_as_name_fsufix_ext_bksufix(self.n_ongoing_lang)
    srcfilename = self.osentry.get_fn_as_name_fsufix_ext_bksufix(self.n_ongoing_lang)
    trgfilepath = self.osentry.fp_for_fn_as_name_fsufix_ext
    trgfilename = self.osentry.fn_as_name_fsufix_ext
    # check existence
    if not os.path.isfile(srcfilepath):
      errmsg = f"""For the rename above
      ---------------------------------------
      FROM (bksufix):  [{srcfilename}]
      ---------------------------------------
        => is missing. Halting.
      """
      print(errmsg)
      sys.exit(1)
    if os.path.isfile(trgfilepath):
      if os.path.isfile(srcfilepath):
        # only the target should continue on folder
        errmsg = f"""For the rename above
        ---------------------------------------
        *** deleting (bksufix):  [{srcfilename}]
            existing (fsufix) :  [{trgfilename}]
        ---------------------------------------
          => reason: both files exist.
        """
        print(errmsg)
        os.remove(srcfilepath)
      return
    try:
      os.rename(srcfilepath, trgfilepath)
      scrmsg = f"""Rename succeeded: from bksufix=".bk{self.n_ongoing_lang}" to fsufix="{self.osentry.fsufix}":
      ----------------------------------
      FROM (bksufix):  [{srcfilename}]
      TO    (fsufix):  [{trgfilename}]
      ----------------------------------
        Going for downloading the audio-complement.
      """
      print(scrmsg)
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename:
      ---------------------------------------
      FROM (bksufix):  [{srcfilename}]
      TO    (fsufix):  [{trgfilename}]
      ---------------------------------------
      => {e}
      Halting.
      """
      print(errmsg)
      sys.exit(1)

  def fallback_to_nondashed_audiocode_changing_it(self):
    """
    The strategy here is the following:

    1 when languages are asked in the audiocodes parameters,
      they are "dash-sufixed", for example

      ['233-0', '233-1'] or ['233-5', '233-9']

      (The hypothesis below is not guaranteed, but this program will try it.)

      When 'subprocess' returns non-0, there's a chance the video does
        not have language variations which might be also deduced
        that, instead of audiocode, say, 233-0, 233 (without dash-0) could work
          and form the video in its original language.
        That would complete the job supposing the video does not have another translated language anyway.
    """
    try:
      # position to new logical next self.n_ongoing_lang
      # if it was already the last, the exception (IndexError) will handle it
      audiocodestr = self.audioonlycodes[self.n_ongoing_lang]
      pp = audiocodestr.split('-')
      newaudiocode = pp[0]
      # this list-index below is the next in the loop it's returning to
      self.audioonlycodes[self.n_ongoing_lang] = newaudiocode
      # let's also delete anything further on this index-point
      # (the reason is that translations do not exist without dash-numbers)
      if self.n_ongoing_lang < len(self.audioonlycodes) - 2:
        del self.audioonlycodes[self.n_ongoing_lang+1:]
    except IndexError:
      scrmsg = f"""WARNING: 
      could not derive a non-dashed-sufix.
        => audioonlycodes = {self.audioonlycodes}
      Returning."""
      print(scrmsg)

  def download_audiopart_to_blend_it_w_videoonly(self):
    """
    One caution here:
      the videoonly_canonical_filename (the one without sufixes) should not be present,
        otherwise yt-dlp will deduce that the composition has already happened,
        (and inform the video has already been download (when only the videopart has)
        so if the videoonly_canonical_filename is present
        (the first 'rename' method below sees to it)
    """
    self.rename_bksufixedfilename_to_fsufixedfilename_to_avoid_the_vo_redownload()  # it's done by removing number sufix
    audiocode = self.audioonlycodes[self.n_ongoing_lang - 1]
    compositecode = f"{self.videoonlycode}+{audiocode}"
    pdict = {'compositecode': compositecode, 'videourl': self.videourl}
    comm = self.comm_line_base.format(**pdict)
    try:
      scrmsg = f"audiocode={audiocode} | running: {comm}"
      print(scrmsg)
      """
      scrmsg = f"Continue with the download above (Y/n)? [ENTER] means Yes"
      ans = input(scrmsg)
      if ans not in ['Y', 'y', '']:
        sys.exit(0)
      """
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
    Because two or more files may be downloaded and cannot have the same name,
      (yt-dlp forms the same filename regardless of language)
      this method prefix-renames the file just downloaded so that the next
      download is "available" for yt-dlp (as its filename is available)
    """
    srccanofilepath = self.osentry.fp_for_fn_as_name_ext
    srccanofilename = self.osentry.fp_for_fn_as_name_ext
    audioonlycode = self.audioonlycodes[self.n_ongoing_lang-1]
    langprefix = self.get_lang2lettercode_fr_audioonlycode(audioonlycode)
    # "vd1" stands for "video 1", an idea is to make it possible for an increment (ex video 2, 3...) if needed
    langprefix = f"vd1-{langprefix}"
    langprefixedfilename = f"{langprefix} {self.osentry.fn_as_name_ext}"
    langprefixedfilepath = os.path.join(self.osentry.workdir_abspath, langprefixedfilename)
    if not os.path.isfile(srccanofilepath):
      srccanofilepath = self.find_existfilepath_of_samecanonicalfilename_w_different_ext_or_none()
      if srccanofilepath is None:
        # can't rename
        wrnmsg = f"""Cannot rename canonical filename:
          ------------------------------------
          FROM (canonical)  : [{srccanofilepath}]
          TO (lang-prefixed): [{langprefixedfilename}"]
          ------------------------------------
          => reason: canonical (FROM) is not present in folder. Continuing."""
        print(wrnmsg)
        return
      # update srccanofilename from srccanofilepath
      _, srccanofilename = os.path.split(srccanofilepath)
    if os.path.isfile(langprefixedfilepath):
      # if targetfile is present, rename will raise an exception, return from here
      wrnmsg = f"""Cannot rename to lang-prefixed filename:
        ------------------------------------
        FROM (canonical)  : [{srccanofilepath}]
        TO (lang-prefixed): [{langprefixedfilename}"]
        ------------------------------------
        => reason: lang-prefixed filename (TO) is already present in folder. Continuing."""
      print(wrnmsg)
      return
    try:
      os.rename(srccanofilepath, langprefixedfilepath)
      scrmsg = f"""Rename succeeded => lang={self.n_ongoing_lang} | audiocode={audioonlycode}
      ------------------------------------
      FROM (canonical)  : [{srccanofilename}]
      TO (lang-prefixed): [{langprefixedfilename}]
      ------------------------------------
      """
      print(scrmsg)
    except (IOError, OSError) as e:
      errmsg = f"""Error when attempting to rename:
      ---------------------------------------
      FROM (canonical)  : [{srccanofilepath}]
      TO (lang-prefixed): [{langprefixedfilename}"]
      ---------------------------------------
      => {e}
      Halting.
      """
      print(errmsg)
      sys.exit(1)

  def download_audio_complements(self):
    """
    self.n_on_going_lang is an instance variable that controls lang orderseq throughout the class
    """
    for self.n_ongoing_lang in range(1, self.n_langs + 1):
      self.download_audiopart_to_blend_it_w_videoonly()
      self.rename_videofile_after_audiovideofusion()

  def process(self):
    """
      1st -> position (cd changedir) at the working tmpdir
      2nd -> download the 160 (or the entered as input) video
      3rd -> disconver the downloaded video's filename
      4th -> copy it to as many as there audio lang entered
        (for example: if one language is Italian, another is for English, two copies are made)
      5th -> download the audio(s) for each language
        5-1 download the audiofile proper
        5-2 "fuse" it with the videofile in store so that the composite results
    """
    scrmsg = f"""1st step ->
    POSITION (chdir) at the working tmpdir: [{self.osentry.workdir_abspath}]"""
    print(scrmsg)
    os.chdir(self.osentry.workdir_abspath)
    scrmsg = f"""2nd step ->
    DOWNLOAD the {self.videoonlycode} video (ytid={self.ytid})"""
    print(scrmsg)
    self.download_video_only()
    scrmsg = f"""3rd step -> 
    DISCOVER the downloaded video's filename (with ytid={self.ytid})
      and rename it to the videoonlyfile
      that one will serve the audio files to later compose audio+video"""
    print(scrmsg)
    self.discover_dldd_videofilename()
    self.rename_from_canonical_to_fsufixedvideoonlyfile()
    scrmsg = f"""4th step ->
    COPY it  (with ytid={self.ytid}) to as many as there are audio lang entered"""
    print(scrmsg)
    self.copy_n_rename_videoonly_n_lang_times()
    scrmsg = f"""5th step ->
    DOWNLOAD (with ytid={self.ytid}) the audio(s) complements | audioonlycodes={self.audioonlycodes}"""
    print(scrmsg)
    self.download_audio_complements()
    # move all videos from child_tmpdir_abspath to its parent dir


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
  ytid = extract_ytid_from_yturl_or_itself_or_none(ytid)
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


def adhoc_test4():
  ose = OSEntry(
    workdir_abspath='.',
    basefilename='bla [123abcABC-_].mp4',
    videoonly_or_audio_code=160
  )
  print(ose)


def adhoc_test3():
  t = 'https://www.youtube.com/watch?v=Gjg471uIL9k&pp=wgIGCgQQAhgD'
  ytid = extract_ytid_from_yturl_or_itself_or_none(t)
  scrmsg = f"""Testing {t}
  Resulting {ytid}"""
  print(scrmsg)
  t = 'https://www.youtube.com/watch?v=abcABC123_-&pp=continuation'
  ytid = extract_ytid_from_yturl_or_itself_or_none(t)
  scrmsg = f"""Testing {t}
  Resulting {ytid}"""
  print(scrmsg)
  # return ytid


def adhoc_test2():
  dirpath = args.dirpath or os.path.abspath('.')
  # inputfilepath = os.path.join(dirpath, DEFAULT_YTIDS_FILENAME)
  ytids = read_ytids_from_default_file_n_get_as_list(dirpath)
  scrmsg = f"adhoc_test2 :: ytids = {ytids}"
  print(scrmsg)


def adhoc_test1():
  ytid = 'abc+10'
  scrmsg = f'Testing verify_ytid_validity_or_raise({ytid})'
  print(scrmsg)
  verify_ytid_validity_or_raise(ytid)


if __name__ == '__main__':
  """
  adhoc_test1()
  adhoc_test2()
  """
  process()
