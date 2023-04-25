#!/usr/bin/env python3
"""
The "hint" to this script was taken originally from a post in askubuntu.com
The post cited command mkvmerge (from package mkvtoolnix)

Basically this script will autoform a command line such as the following:
$ mkvmerge -o outfile,mkv "file1.mp4" \\* "file2.mp4" \\+ "file3.mp4"

Usage:
videosJoin.py [<file_extension>]

WHERE
<file_extension> is a video file extension (e.g. mp4|mkv|webm etc)
If no extension is given, mp4 is the default.

A confirmation yes/no question will be asked for running the autoformed command line.
"""
import glob
import os
import random
import sys
import time

DEFAULT_INPUT_EXT = '.mp4'
DEFAULT_OUTPUT_EXT = '.mkv'
COMM_FFMPEG = 'ffmpeg'
COMM_MKVMERGER = 'mkvmerger'
COMM_MENCODER = 'mencoder'
AVAILABLE_MERGERS = [COMM_FFMPEG, COMM_MKVMERGER, COMM_MENCODER]
DEFAULT_MERGER = COMM_MKVMERGER


def adjust_front_dot_if_needed(ext):
  if not ext.startswith('.'):
    ext = '.' + ext
  return ext


class VideoMerger:

  def __init__(self, whichmerger=None, input_ext=None, output_ext=None):
    self.whichmerger = whichmerger or DEFAULT_MERGER
    if self.whichmerger not in AVAILABLE_MERGERS:
      self.whichmerger = DEFAULT_MERGER
    self.input_ext = input_ext or DEFAULT_INPUT_EXT
    self.input_ext = adjust_front_dot_if_needed(self.input_ext)
    self.output_ext = output_ext or DEFAULT_OUTPUT_EXT
    self.output_ext = adjust_front_dot_if_needed(self.output_ext)

  @staticmethod
  def find_form_n_get_basefoldername():
    """
    Extracts the foldername of the executing path.
    Example:
      e1) suppose executing path is '/Sci/Physics/Quantum' (not coinciding with the script's path)
      e2) this function will find 'Quantum'

    Some OBS
    exec_fullpath =
    Notice that the composition os.path.dirname(os.path.realpath(__file__)), differently from os.getcwd(),
      gives the script's folder (somewhere in PythonPath) not the executing path
    """
    exec_fullpath = os.getcwd()
    basefoldername = os.path.split(exec_fullpath)[1]
    return basefoldername

  def find_form_n_get_outputfilename(self):
    basefoldername = self.find_form_n_get_basefoldername()
    outputfilename = 'joint ' + basefoldername + self.output_ext
    if os.path.isfile(outputfilename):
      error_msg = 'File [%s] already exists.' % outputfilename
      print(error_msg)
      sys.exit(1)
    return outputfilename

  def form_n_get_outfilename_enclosed_by_doublequotes(self):
    outputfilename = self.find_form_n_get_outputfilename()
    outfilename_enclosed = '"' + outputfilename + '"'
    return outfilename_enclosed

  def form_n_get_listfile_each_within_quotes_astext(self):
    files = glob.glob('*' + self.input_ext)
    files.sort()
    filelist_text = ''
    for f in files:
      filelist_text += '"' + f + '" '
    filelist_text = filelist_text.strip(' ')
    return filelist_text

  def textfile_for_ffmpeg_onthefly_commline(self):
    """
    ffmpeg -f concat -i videos.txt -c copy output.mp4
    """
    files = glob.glob('*' + self.input_ext)
    files.sort()
    rand_3dig_str = str(random.randint(0, 999)).zfill(3)
    tmpoutfilename = 'ztmpoutfilename-%s.txt' %rand_3dig_str
    tmpoutfile = open(tmpoutfilename, 'w')
    tmpfiletext = ''
    for f in files:
      tmpfiletext += "file '%s'\n" %f
    tmpoutfile.write(tmpfiletext)
    tmpoutfile.close()
    time.sleep(0.5)  # give a time out for OS save the tmpfile

    outfilename_enclosed = self.form_n_get_outfilename_enclosed_by_doublequotes()
    commline = 'ffmpeg -f concat -i %s -c copy %s' %(tmpoutfilename, outfilename_enclosed)
    return commline

  def textfile_for_ffmpeg_inline_commline(self):
    """
    ffmpeg -i "concat:input1.mp4|input2.mp4|inputn.mp4" -c copy output.mp4
    :return:
    """
    files = glob.glob('*' + self.input_ext)
    files.sort()
    filelist_text = '"concat:'
    for f in files:
      filelist_text += f + '|'
    filelist_text = filelist_text.strip('|')
    filelist_text += '"'
    return filelist_text

  def form_n_get_commline_with_ffmpeg(self):
    """
    ffmpeg -f concat -i videos.txt -c copy output.mp4
    ffmpeg -i "concat:input1.mp4|input2.mp4|inputn.mp4" -c copy output.mp4

    :return:
    """
    commline = 'ffmpeg -i '
    filelist_text = self.textfile_for_ffmpeg_inline_commline()
    commline += filelist_text
    outfilename_enclosed = self.form_n_get_outfilename_enclosed_by_doublequotes()
    commline += ' -c copy ' + outfilename_enclosed
    return commline

  def form_n_get_commline_with_mencoder(self):
    """
    mencoder v1.mp4 v2.mp4 -ovc copy -oac copy -of lavf format=mp4 output_mergedvideo.mp4

    Audio format 0x4134504d is incompatible with '-oac copy', please try '-oac pcm'
       instead or use '-fafmttag' to override it.
    :return:
    """
    inputfiles = self.form_n_get_listfile_each_within_quotes_astext()
    outfilename_enclosed = self.form_n_get_outfilename_enclosed_by_doublequotes()
    commline = 'mencoder %s -ovc copy -oac pcm format=mp4 -o %s'\
               % (inputfiles, outfilename_enclosed)
    return commline

  def form_n_get_commline_with_mkvmerge(self):
    outfilename_enclosed = self.form_n_get_outfilename_enclosed_by_doublequotes()
    commline = 'mkvmerge -o ' + outfilename_enclosed + ' '
    files = glob.glob('*'+self.input_ext)
    files.sort()
    for f in files:
      commline += '"' + f + '" \\+ '
    commline = commline.strip(' \\+ ')
    return commline

  def process(self):
    if self.whichmerger == COMM_FFMPEG:
      # commline = self.form_n_get_commline_with_ffmpeg()
      commline = self.textfile_for_ffmpeg_onthefly_commline()
    elif self.whichmerger == COMM_MKVMERGER:
      commline = self.form_n_get_commline_with_mkvmerge()
    elif self.whichmerger == COMM_MENCODER:
      commline = self.form_n_get_commline_with_mencoder()
    else:
      error_msg = "Logical error: whichmerger should be in list " + str(AVAILABLE_MERGERS)
      raise ValueError(error_msg)
    exec_commline(commline)


def confirm_exec_commline(commline):
  print(commline)
  screen_msg = 'Confirm executing the above line? (Y*/n) [ENTER] means Yes '
  ans = input(screen_msg)
  if ans not in ['', 'Y', 'y']:
    return False
  return True


def exec_commline(commline):
  if confirm_exec_commline(commline):
    print('Running command. Please wait.')
    os.system(commline)


def get_argdict():
  argdict = {'input_ext': None, 'mergercomm': None, 'output_ext': None}
  for arg in sys.argv:
    if arg.startswith('-e='):
      input_ext = arg[len('-e='):]
      argdict['input_ext'] = input_ext
    elif arg.startswith('-o='):
      output_ext = arg[len('-o='):]
      argdict['output_ext'] = output_ext
    elif arg.startswith('-c='):
      mergercomm = arg[len('-c='):]
      argdict['mergercomm'] = mergercomm
  return argdict


def process():
  argdict = get_argdict()
  input_ext = argdict['input_ext']
  output_ext = argdict['output_ext']
  mergercomm = argdict['mergercomm']
  vmerger = VideoMerger(mergercomm, input_ext, output_ext)
  vmerger.process()


if __name__ == '__main__':
  process()
