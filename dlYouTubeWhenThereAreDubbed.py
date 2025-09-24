#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

This script uses (underlying) yt-dlp to download (from YouTube) a video
  in two or more languages.

  YouTube spoken-language-translations are, as far as we've noticed, autodubbed.

Observation about the auto-dubs and this script:

  1) if the video has only its original language available, no auto-dubs,
    this script is able to "fall back" to a one-language download;

  2) the fall-back is not "perfectly" perceived,
    at the time of writing any non-zero return from subprocess
    will make this script try a one-language download,

  3) but, if the non-zero return was caused by, say,
    a network fault, and the video is in fact multilanguage,
    the one-language attempt will also fail
    (attempting to download a multilanguage video with
     a one-language audiocode returns an error from YouTube).

Each language, dubbed or original, has its own separate audio-only-file
  that is 'fused' (or merged) to its video-only counterpart
  forming the language-dubbed video
  (@see example below)

Usage (this is about to receive some adjustments):
  (the --audioonlycodes will become --amn (for "audiomainnumber"))
  (the --map will be introduced)
  (the --videoonlycode will become --voc)
  (a sketch of this upgrade comes at the end)
======

Proposed (newer) syntax:
  $dlYouTubeWhenThereAreDubbed.py [--ytid <ytid or yturl within "">]
    [--useinputfile]
    [--voc <video-only-code-number>]
    [--amn <audio-main-number>]
    [--map <dictionary-map-informing-sufixes-and-their-2-letter-language-codes>]


Older syntax:
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

For example:
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

The first case (where English is the original) seems to make English have
  either a "-9" (dash nine), most of the time,
  or "-8" (dash eight) sometimes.

The user has to use the audiocodes CLI parameter to tell the correct audiocodes (*).
  The default today uses [233-0, 233-1]
    and, as mentioned above, stable for when English is autodubbed
    and another language is the original.

 (*) to see the full list of CLI parameters for this script together with this docstr,
     run it with --docstr
     (parameter --help shows all parameters with a short description for each)
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

On 2025-08-01:
  the main parts of this script were already in use
On 2025-09-23:
  thinking about an innovation to this script
  introducing the --map CLI parameter
  --map accepts a string like a dict without spaces, e.g.:
    => --map "0:en,1:pt"
  This informs the number sufixes for the audioonlycode and which languages those represent
  Because of that, parameter --audioonlycodes may also be changed:
    FROM: a list of "dashed" number (e.g. "[249-0, 249-1"])
    TO: a number  (e.g. "249")
  --audioonlycodes may become --audiomainnumber

Justification:
  the number of YouTube autodubbed available languages
    not only may vary from video to video (especially in English originals),
    but it may also grow in the future
"""
import argparse
import os.path
import shutil
import subprocess
import sys
import localuserpylib.ytfunctions.yt_str_fs_vids_sufix_lang_map_etc as ytstrfs
import localuserpylib.regexfs.filenamevalidator_cls as fnval  # .FilenameValidator
import localuserpylib.ytfunctions.osentry_class as ose  # ose.OSEntry
OSEntry = ose.OSEntry
DEFAULT_YTIDS_FILENAME = ose.DEFAULT_YTIDS_FILENAME
DEFAULT_AUDIOVIDEO_CODE = ose.DEFAULT_AUDIOVIDEO_CODE
DEFAULT_AUDIOVIDEO_DOT_EXT = ose.DEFAULT_AUDIOVIDEO_DOT_EXT
DEFAULT_AUDIO_ONLY_CODES = ose.DEFAULT_AUDIO_ONLY_CODES
DEFAULT_AUDIO_MAIN_NUMBER = ose.DEFAULT_AUDIO_MAIN_NUMBER
DEFAULT_SFX_W_2LETLNG_MAPDCT = ose.DEFAULT_SFX_W_2LETLNG_MAPDCT
DEFAULT_VIDEO_ONLY_CODE = ose.DEFAULT_VIDEO_ONLY_CODE
VIDEO_DOT_EXTENSIONS = ose.VIDEO_DOT_EXTENSIONS
default_videodld_tmpdir = ose.default_videodld_tmpdir
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--docstr", action="store_true",
                    help="show docstr help and exit")
parser.add_argument("--ytid", type=str,
                    help="the video id")
parser.add_argument("--useinputfile", action='store_true',
                    help="read the default ytids input file")
parser.add_argument("--dirpath", type=str,
                    help="Directory recipient of the download")
parser.add_argument("--voc", type=int, default=f"{DEFAULT_AUDIOVIDEO_CODE}",
                    help="video only code: example: 160")
parser.add_argument("--amn", type=int, default="249",
                    help="audio only codes: example: 233-0,233-1")
parser.add_argument("--nvdseq", type=int, default=1,
                    help="the sequencial number that accompanies the 'vd' namemarker at the last renaming")
parser.add_argument("--map", type=str, default="0:en,1:pt",
                    help="the dictionary-mapping with numbers and the 2-letter language codes (e.g. '0:en,1:pt')")
args = parser.parse_args()


def show_docstrhelp_n_exit():
  print(__doc__)
  sys.exit(0)


class Downloader:

  # class-wide static constants
  DEFAULT_VIDEO_ONLY_CODE = DEFAULT_VIDEO_ONLY_CODE
  DEFAULT_AUDIO_ONLY_CODES = DEFAULT_AUDIO_ONLY_CODES
  DEFAULT_SFX_W_2LETLNG_MAPDCT = DEFAULT_SFX_W_2LETLNG_MAPDCT
  DEFAULT_AUDIO_MAIN_NUMBER = DEFAULT_AUDIO_MAIN_NUMBER
  videodld_tmpdirname = default_videodld_tmpdir
  # class-wide static interpolable-string constants
  comm_line_base = 'yt-dlp -w -f {compositecode} "{videourl}"'
  video_baseurl = 'https://www.youtube.com/watch?v={ytid}'

  def __init__(
      self,
      ytid: str,
      dlddir_abspath: str = None,
      videoonlycode: int = None,
      audiomainnumber: int = None,
      nvdseq: int = None,
      sfx_n_2letlng_dict: dict = None,
    ):
    self.ytid = ytid
    self.nvdseq = nvdseq or 1
    self.dlddir_abspath = dlddir_abspath
    self.videoonlycode = videoonlycode
    self.audiomainnumber = audiomainnumber  # example: 233, 234, 249 etc
    self.sfx_n_2letlng_dict = sfx_n_2letlng_dict
    self.treat_input()
    self.ytsufixlang_o = ytstrfs.SufixLanguageMapFinder(self.sfx_n_2letlng_dict)
    self.b_verified_once_tmpdir_abspath = None
    self.prename = None
    self.previously_existing_filenames_in_tmpdir = []
    self.n_ongoing_lang = 0
    self.lang_map = {}  # this dict has {sufix: 2-letter-langid}
    self.osentry = OSEntry(
      workdir_abspath=self.child_tmpdir_abspath,
      basefilename=None,  # later to be known
      videoonly_or_audio_code=self.videoonlycode
    )
    pass
    print('osentry =', self.osentry)
    # self.va_osentry = []

  def treat_input(self):
    ytstrfs.verify_ytid_validity_or_raise(self.ytid)
    if self.dlddir_abspath is None:
      # default is the current working directory
      self.dlddir_abspath = os.path.abspath('.')
    if self.videoonlycode is None:
      # this is the default for the videocode
      self.videoonlycode = self.DEFAULT_VIDEO_ONLY_CODE
    if self.audiomainnumber is None or not isinstance(self.audiomainnumber, int):
      # this default for the audiocodes generally works when English is autodubbed and another language is the original
      # notice that this script, at the time of writing, does not know about which language is which (@see docstr above)
      self.audiomainnumber = self.DEFAULT_AUDIO_MAIN_NUMBER
    if self.sfx_n_2letlng_dict is None:
      return
    for number in self.sfx_n_2letlng_dict:
      twolettercode = self.sfx_n_2letlng_dict[number]
      if len(twolettercode) != 2:
        errmsg = f"The 2-letter-language-code [{twolettercode}] should have only 2 letter."
        raise ValueError(errmsg)

  @property
  def n_langs(self):
    return len(self.sfx_n_2letlng_dict)

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
    audiocode = self.lang_map.get_first_2lettlangcode()  # index 0 is the first language
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
      if not filename.endswith(tuple(ose.VIDEO_DOT_EXTENSIONS)):  # notice osentry has not yet been initialized at this
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
    Discovers the filename of the downloaded yt-dlp file

    However, when a download is incomplete, the following info is important.

    The discovery process is easy when the download process in not interrupted,
      but tricky if the user is continuing a previous incomplete download.

    When a download process is completed, a prefix is prepended to the filenames.

    When download process is incomplete and the user restarts it,
      this script makes a "strong" supposition", .i.e., one
      to consider the canonical filename, if present, representing the video-only-file.

    * Chances are this is correct, but, if not, the user should restart from an empty directory.

    How to discovery works
    =======================

    Before making the "strong assumption" above, the script compares the directory contents
      looking for a new file (comparasion before versus after). This is the first try.

    The second try starts when, after the first try, a new recent file is not found.
    The second is based on a "strong supposition". This assumption may delineate as follows:
      1 - a previous download happened, but it's incomplete
      2 - a look-up for the canonical file in folder will be interpreted as the video-only-file

    The user should know this detail because if this hypothesis is wrong, the result may be wrong.
    Another hypothesis is a failure in the last renaming of the last run, i.e., the download was completed,
      and the user is restarting a new one actually without need.

    If the second try does not find a file, the third try asks the user which filename
      is the correct one.
    """
    videofilename_soughtfor = None
    allfilenames = os.listdir(self.osentry.workdir_abspath)
    # dot_ext = self.cur_dot_ext
    # ----------
    # first try: folder contents comparison (before versus after)
    # ----------
    videofilenames = filter(lambda f: f.endswith(tuple(VIDEO_DOT_EXTENSIONS)), allfilenames)
    videofilenames_appearing_after = list(
      filter(
        lambda f: f not in self.previously_existing_filenames_in_tmpdir,
        videofilenames
      )
    )
    n_results = len(videofilenames_appearing_after)
    if n_results == 1:
      videofilename_soughtfor = videofilenames_appearing_after[0]
      scrmsg = f"Found downloaded file as [{videofilename_soughtfor}]"
      print(scrmsg)
    else:
      # at this point, some hypotheses come to mind
      # 1 - directory may be empty (which might signal a network failure)
      # 2 - file had already been downloaded before, so the comparison before versus after does not find it
      # 3 - if 2 is so, the second try below may find it, but if this hypothesis is wrong and
      #     an error happened in the final renaming of last run,
      #     this solution will not be the correct one (at any rate, if the user finds it incorrect,
      #     a new start should be done on an empty working directory)
      # ----------
      # second try: look up filename's canonical form
      # ----------
      scrmsg = f"Looking up the downloaded file among {len(allfilenames)} files in folder"
      print(scrmsg)
      for fn in allfilenames:
        # filename is compliant to the "canonical filename", i.e., name[ytid].ext
        validator = fnval.FilenameValidator(filename=fn)
        if validator.is_filename_a_valid_ytdlp and self.ytid == validator.ytid:
          # found it (it has the canonical form and the same ytid, that's it [unique])
          videofilename_soughtfor = fn
          scrmsg = f"Found downloaded file as [{videofilename_soughtfor}]"
          print(scrmsg)
          break
    if videofilename_soughtfor is None:
      # ----------
      # third (and last) try: ask the user
      # ----------
      videofilename_soughtfor = self.fallbackcase_ask_user_what_the_downloaded_filename_is()
    if videofilename_soughtfor is None:
      # oh, oh, can't continue
      errmsg = f"Error: videofilename_soughtfor is None, script could not find it."
      raise OSError(errmsg)
    self.osentry.basefilename = videofilename_soughtfor
    # set found dot_extension to osentry
    _, self.osentry.dot_ext = os.path.splitext(self.osentry.basefilename)
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
      scrmsg = f"""Not renaming to the f-sufixed ({self.osentry.fsufix}) video-only-filename:
         => [{self.osentry.fn_as_name_fsufix_ext}]
       as it already exists in the working directory.
       ---------------
       Script is going to delete the canonical file [{self.osentry.fn_as_name_ext}] 
       so that after the next language download yt-dlp will be able to blend audio with video."""
      print(scrmsg)
      os.remove(self.osentry.fp_for_fn_as_name_ext)
      print('Canonical file deleted. Continuing.')
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
      warnmsg = f"""Command: [{comm}]
       failed with return code: [{e.returncode}]
       => {e}"""
      print(warnmsg)
      # raise ValueError(errmsg)
      return False
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
    extensions = list(self.osentry.video_dot_extensions)
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
        # self.cur_dot_ext = next_dot_ext
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

  def delete_all_lang_subcodes_afterfallback(self):
    """
    Deletes all audioonlycodes after ongoing_index in queue (list)

    This happens when the fallback method is called, which
      means that this script has decided (supposion as designed)
      that the video in question does not have language subcodes.

    For example:
      Suppose an attempt to download audioonlycode 233-0 fails
      returning exit 1. After that it retries with audioonlycode 233
      (audioonlycode without a dash number).
      Okay. Suppose that originally the queue is 233-0, 233-1, 233-2
      But, in this case, all subsequent dash-numbers (-1 and -2)
      in queue must be removed.

      This method does this emptying of the queue.

    Obs: unfortunalety, the way this method was planned got 'disconnected'
      from the main process loop which goes through the array of languages sequentially,
      not looking at the audioonlycodes list.  This may be replanned in the future,
      i.e., looping directly through the audioonlycodes list or testing its size there,
      this was not done yet because the call stack got bigger, so we want to do this
      correction by looking them all. (This problem only affects the download process
      when the video requested does not have the audioonlycode in passing.)
    """
    while self.n_ongoing_lang < len(self.audioonlycodes) - 1:
      _ = self.audioonlycodes.pop()

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
      self.delete_all_lang_subcodes_afterfallback()
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
    try:
      audiocode = self.audioonlycodes[self.n_ongoing_lang - 1]
    except IndexError:
      # can't download without audiocode, return
      scrmsg = (f"audiocode for lang={self.n_ongoing_lang} does not exist at this point,"
                f" due to a fallback to non-dashed-audiocode (which means only one of them)."
                f" Returning.")
      print(scrmsg)
      return
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
      => trying a download without an audiocode with the dashed-sufix
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
    try:
      # this may happen if a fallback to non_dashed_audioonlycode happened previously
      # but maybe this one is not the best solution (to think about)
      audioonlycode = self.audioonlycodes[self.n_ongoing_lang-1]
    except IndexError:
      return
    langprefix = self.get_lang2lettercode_fr_audioonlycode(audioonlycode)
    # "vd1" stands for "video 1", an idea is to make it possible for an increment (ex video 2, 3...) if needed
    langprefix = f"vd{self.nvdseq}-{langprefix}"
    langprefixedfilename = f"{langprefix} {self.osentry.fn_as_name_ext}"
    langprefixedfilepath = os.path.join(self.osentry.workdir_abspath, langprefixedfilename)
    if not os.path.isfile(srccanofilepath):
      # delete the method below when the finding routing gets working in class osentry
      # srccanofilepath = self.find_existfilepath_of_samecanonicalfilename_w_different_ext_or_none()
      self.osentry.find_n_set_the_canonical_with_another_extension()
      srccanofilepath = self.osentry.fp_for_fn_as_name_ext
      srccanofilename = self.osentry.fp_for_fn_as_name_ext
      if srccanofilepath is None:
        # can't rename
        wrnmsg = f"""Cannot rename canonical filename:
          ------------------------------------
          canoname : [{srccanofilename}]
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
      warnmsg = f"""Error when attempting to rename:
      ---------------------------------------
      FROM (canonical)  : [{srccanofilepath}]
      TO (lang-prefixed): [{langprefixedfilename}"]
      ---------------------------------------
      => {e}
      Continuing.
      """
      print(warnmsg)
      # sys.exit(1)

  def check_if_canonicalname_changed_its_extension(self):
    """
    The canonical file is composed as:
      {prename}{one-blank-space}{ytid_within_squarebrackets}{dot_extension}
    At a certain combination (example: when a 249 audio is downloaded with a mp4),
      the canonical name changes its extension from 'mp4' to 'mkv'
    So, this method tries to observe if this extension change happened
    """
    self.osentry.find_n_set_the_canonical_with_another_extension()

  def download_audio_complements(self):
    """
    self.n_on_going_lang is an instance variable that controls lang orderseq throughout the class
    """
    for self.n_ongoing_lang in range(1, self.n_langs + 1):
      self.download_audiopart_to_blend_it_w_videoonly()
      # TODO test if fallback to non_dashed_number_audiocode happened at this point
      # the reason is that on_going_lang is not following the indices of list audioonlycodes
      # an IndexError protection is done inside the next method, but we should still think about a better solution
      # so that a last renaming may happen to the non_dashed_number_audiocode videofile
      # the way it is now, this last renaming is done manually, if he/she wants to, by the user
      self.check_if_canonicalname_changed_its_extension()
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
    if not self.download_video_only():
      # at this point, `subprocess` exitted with non-0 (this also means the videoonlyfile did not download)
      # as the next steps depend on this, script cannot continue returning False from here
      return False
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
    return True


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
  if args.docstr:
    show_docstrhelp_n_exit()
  ytid = args.ytid
  boo_readfile = args.useinputfile
  # default to the current working directory if none is given
  dirpath = args.dirpath or os.path.abspath(".")
  videoonlycode = args.videoonlycode or None
  audiomainnumber = args.amn or DEFAULT_AUDIO_MAIN_NUMBER
  sfx_n_2letlng_dict = args.map or DEFAULT_SFX_W_2LETLNG_MAPDCT
  nvdseq = args.nvdseq or 1
  return ytid, boo_readfile, dirpath, videoonlycode, audiomainnumber, nvdseq, sfx_n_2letlng_dict


def verify_n_trans_sfx_n_2letlng_dict(sfx_n_2letlng_dict):
  return ytstrfs.trans_str_sfx_n_2letlng_map_to_dict_or_raise(sfx_n_2letlng_dict)


def confirm_cli_args_with_user(ytids, dirpath, videoonlycode, audiomainnumber, nvdseq, sfx_n_2letlng_dict):
  if not os.path.isdir(dirpath):
    scrmsg = f"Source directory [{dirpath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  sfx_n_2letlng_dict = verify_n_trans_sfx_n_2letlng_dict(sfx_n_2letlng_dict)
  charrule = '=' * 20
  print(charrule)
  print('Input parameters entered')
  print(charrule)
  scrmsg = f"""
  => ytids = {ytids} | total = {len(ytids)} | sequential sufix for the 'vd' namemarker = {nvdseq} 
  -------------------
  => dirpath = [{dirpath}]
  (confer default subdirectory "{default_videodld_tmpdir}" or other)
  -------------------
  => videoonlycode = {videoonlycode} | audiomainnumber = {audiomainnumber}
  => sfx_n_2letlng_dict = {sfx_n_2letlng_dict}
  """
  print(scrmsg)
  print(charrule)
  scrmsg = "Are the parameters above okay? (Y/n) [ENTER] means Yes "
  ans = input(scrmsg)
  print(charrule)
  confirmed = False
  if ans in ['Y', 'y', '']:
    confirmed = True
  return confirmed, sfx_n_2letlng_dict


def get_default_ytids_filepath(p_dirpath):
  ytids_filename = DEFAULT_YTIDS_FILENAME
  default_ytids_filepath = os.path.join(p_dirpath, ytids_filename)
  if not os.path.isfile(default_ytids_filepath):
    errmsg = f"YTIDs filepath [{default_ytids_filepath}] does not exist. Please, create it and retry."
    raise OSError(errmsg)
  return default_ytids_filepath


def adhoctest1():
  ytid = 'abc+10'
  scrmsg = f'Testing verify_ytid_validity_or_raise({ytid})'
  print(scrmsg)
  ytstrfs.verify_ytid_validity_or_raise(ytid)


def get_cli_params_n_confirm():
  ytid, b_useinputfile, dirpath, videoonlycode, audiomainnumber, nvdseq, sfx_n_2letlng_dict = get_cli_args()
  ytid = ytstrfs.extract_ytid_from_yturl_or_itself_or_none(ytid)
  ytids = []
  if b_useinputfile:
    ytids = ytstrfs.read_ytids_from_file_n_get_as_list(get_default_ytids_filepath(dirpath))
    if ytid:
      ytids.append(ytid)
  else:
    if ytid:
      ytids = [ytid]
  if len(ytids) == 0:
    scrmsg = "No ytid given. Please, enter at least one ytid."
    print(scrmsg)
    return []
  ytids = ytstrfs.trans_list_as_uniq_keeping_order_n_mutable(ytids)
  confirmed, audioonlycodes_as_list = confirm_cli_args_with_user(
    ytids, dirpath, videoonlycode,
    audiomainnumber, nvdseq,
    sfx_n_2letlng_dict
  )
  if not confirmed:
    return None
  params_packed = (
    ytids, dirpath, videoonlycode,
    audiomainnumber, nvdseq,
    sfx_n_2letlng_dict
  )
  return params_packed


def process():
  """
  """
  params_packed = get_cli_params_n_confirm()
  (
   ytids, dirpath,
   videoonlycode, audiomainnumber,
   nvdseq, sfx_n_2letlng_dict
  ) = params_packed
  if ytids is None or len(ytids) == 0:
    return False
  for ytid in ytids:
    downloader = Downloader(
      ytid=ytid,
      dlddir_abspath=dirpath,
      videoonlycode=videoonlycode,
      audiomainnumber=audiomainnumber,
      nvdseq=nvdseq,
      sfx_n_2letlng_dict=sfx_n_2letlng_dict
    )
    _ = downloader.process()  # process() returns a boolean (True | False)
  return True


if __name__ == '__main__':
  """
  adhoctest1()
  adhoctest2()
  """
  process()
