#!/usr/bin/env python3
"""
~/bin/dlYouTubeRecupFSufixLeftovers.py

This script looks up incomplete downloaded files in a folder,
  fetches their video-format-lists and then outputs videoids that are
  autodubbed into an output textfile and
  those that are not autodubbed into another output.

These outputfiles become input for another script that will
  try to finish the incomplete downloads, observing:

a) the autodubbed videos may be downloaded with the parameter --useinputfile
  of script dlYouTubeWhenThereAreDubbed.py
  (the script here does a copying from the fsufix file (available) to the canonical filename)
  (this operation is necessary for the download continuation with dlYouTubeWhenThereAreDubbed.py)

b) the non-autodubbed videos are, in a simpler manner, downloaded
  with script "dlYouTubeWithIdsOnTxtFile2.py <format-combination>"

Notice this script does not continue the downloads, just prepare the output textfiles
  for the two options above. The user needs to run the follow-up scripts mentioned.

"""
import os.path
import re
# import shutil
# import subprocess
# import sys
# import localuserpylib.ytfunctions.yt_str_fs_vids_sufix_lang_map_etc as ytstrfs
# import localuserpylib.regexfs.filenamevalidator_cls as fnval  # .FilenameValidator
import localuserpylib.ytfunctions.osentry_class as ose  # ose.OSEntry
# import localuserpylib.ytfunctions.cliparams_for_utubewhendub as clip  # clip.CliParam
# DEFAULT_AUDIOVIDEO_DOT_EXT = ose.DEFAULT_AUDIOVIDEO_DOT_EXT
# OSEntry = ose.OSEntry
# default_videodld_tmpdir = ose.default_videodld_tmpdir
VIDEO_DOT_EXTENSIONS = ose.VIDEO_DOT_EXTENSIONS
restr_fsufix_n_dotext = r"(^.*?)(\.f\d+?)(\.[A-Za-z0-9]+)$"
recmp_fsufix_n_dotext = re.compile(restr_fsufix_n_dotext)
restr_ending_ytid = r"^.*?[ ]\[([A-Za-z0-9_\-]{11})\]$"
recmp_ending_ytid = re.compile(restr_ending_ytid)


class VideoNameAttr:

  def __init__(self, filename):
    self.filename = filename
    self._name = None
    self._dot_ext = None
    self._fsufix = None
    self._ytid = None

  def try_regexp_match(self):
    matchsufixes = recmp_fsufix_n_dotext.match(self.filename)
    if matchsufixes:
      self._name = matchsufixes.group(1)
      self._fsufix = matchsufixes.group(2)
      self._dot_ext = matchsufixes.group(3)
      matchytid = recmp_ending_ytid.match(self._name)
      if matchytid:
        self._ytid = matchytid.group(1)
        # the ytid is already valid because it comes from a regexp
        # so this following part may be commented-out
        # if not ytstrfs.is_str_a_ytid(self._ytid):
        #   errmsg = f"Error: [{self._ytid}] is not a valid ytid."
        #   raise ValueError(errmsg)

  @property
  def fsufix(self):
    if self._fsufix is None:
      self.try_regexp_match()
    return self._fsufix

  @property
  def dot_ext(self):
    if self._dot_ext is None:
      self.try_regexp_match()
    return self._dot_ext

  @property
  def name(self):
    if self._name is None:
      self.try_regexp_match()
    return self._name

  @property
  def ytid(self):
    if self._ytid is None:
      self.try_regexp_match()
    return self._ytid

  def is_complete(self):
    if self.ytid and self.name and self.dot_ext:
      return True
    return False

  def is_ytid_autodubbed_by_formatfile(self):
    """

    :return:
    """
    videoformat_fn = f"{self.ytid}.txt"
    _ = open(videoformat_fn).read()
    # the idea is to instropect read filetext so that autodubbed codes are found or not
    return False

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    filename = {self.filename}
    name = {self.name}
    fsufix = {self.fsufix}
    dot_ext = {self.dot_ext}
    ytid = {self.ytid}
    """
    return outstr


class AutodubbedFinder:

  def __init__(self, dirpath=None):
    self.dirpath = dirpath
    self.incompl_vfilenames = []
    self.autodubbed_ytids = []
    self.nonautodubbed_ytids = []
    if self.dirpath is None:
      self.dirpath = os.path.abspath('.')

  def fetch_videofiles_in_dir(self):
    entries = os.listdir(self.dirpath)
    self.incompl_vfilenames = filter(lambda fn: fn.endswith(tuple(VIDEO_DOT_EXTENSIONS)), entries)

  def listfiles(self):
    self.fetch_videofiles_in_dir()
    for i, fn in enumerate(self.incompl_vfilenames):
      print(i+1, fn)
    print(self.dirpath)

  def copy_fsufix_file_to_canonical(self):
    pass

  def onlinefetch_video_formats(self):
    for i, fn in enumerate(self.incompl_vfilenames):
      attr_o = VideoNameAttr(fn)
      if not attr_o.is_complete():
        continue
      comm = f"yt-dlp -F {attr_o.ytid} > {attr_o.ytid}.txt"
      print(comm)
      os.system(comm)
      if attr_o.is_ytid_autodubbed_by_formatfile():
        self.copy_fsufix_file_to_canonical()
        self.autodubbed_ytids.append(attr_o.ytid)
      else:
        self.nonautodubbed_ytids.append(attr_o.ytid)

  def save_autodubbed_ytids(self):
    pass

  def save_nonautodubbed_ytids(self):
    pass

  def save_ytids_textfiles(self):
    self.save_autodubbed_ytids()
    self.save_nonautodubbed_ytids()

  def process(self):
    self.fetch_videofiles_in_dir()
    self.onlinefetch_video_formats()
    self.save_ytids_textfiles()


def adhoctest2():
  fn = ("2025-08-08 1' Rodrigo Vianna comenta a cronologia de ações"
        " golpistas do bolsonarismo feita por Paulo Motoryn [bFYD24JM6dI].f160.mp4")
  attr_o = VideoNameAttr(fn)
  print(attr_o)
  print('is complete', attr_o.is_complete())


def adhoctest1():
  fn = ("2025-08-08 1' Rodrigo Vianna comenta a cronologia de ações"
        " golpistas do bolsonarismo feita por Paulo Motoryn [bFYD24JM6dI].f160.mp4")
  matchobj = recmp_fsufix_n_dotext.match(fn)
  print(fn)
  print('match', matchobj)
  if matchobj:
    name = matchobj.group(1)
    fsufix = matchobj.group(2)
    dot_ext = matchobj.group(3)
    print('name', name)
    print('fsufix', fsufix)
    print('dot_ext', dot_ext)
    match2 = recmp_ending_ytid.match(name)
    if match2:
      ytid = match2.group(1)
      print('match2', match2)
      print('ytid', ytid)


def process():
  """
  """
  finder = AutodubbedFinder()
  finder.listfiles()


if __name__ == '__main__':
  """
  adhoctest2()
  """
  # process()
  adhoctest2()
