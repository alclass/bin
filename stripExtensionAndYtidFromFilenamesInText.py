#!/usr/bin/python3
"""
~/bin/stripExtensionAndYtidFromFilenamesInText.py
Removes the ending string of a filename that
   consists in the dash-prefixed-ytid plus a dot-extension.

Example of this tail-string removal:
  a) suppose a filename as "abc-bla-foo-bar-123_abc-ABC.mp4"
  b) its trailing-string then is "-123_abc-ABC.mp4"
     i.e.
     b-1 a beginning "-" (dash),
     b-2 then ytid "123_abc-ABC",
     b-3 then its dot_extension ".mp4"
  c) the result (the stripped name) is "abc-bla-foo-bar"

  The above is for a one-line, procesing will encompass all filelines.

Usage:
  #stripExtensionAndYtidFromFilenamesInText.py [<filename>] --workdir=[<workdir>]

Both (filename & wordir) arguments are optional,
  their defaults are:
  -> filename = 'z-names.txt'
  -> workdir = '.'

Example:
 #stripExtensionAndYtidFromFilenamesInText.py [<filename>] --workdir=[<workdir>]

"""
import argparse
import os
import sys
import lblib.ytfunctions.yt_str_fs_vids_sufix_lang_map_etc as ytfs  # .is_str_a_ytid
DEFAULT_FILENAME = 'z-names.txt'
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--docstr", action="store_true",
                    help="show docstr help and exit")
parser.add_argument("--fn", type=str,
                    help="data content filename for processing")
parser.add_argument("--wd", type=str,
                    help="the working directory where process will happen")
args = parser.parse_args()


def strip_trailingtext_ifithappens(line):
  basename, dot_ext = os.path.splitext(line)
  if len(basename) > 12:
    sup_ytid = basename[-11:]
    if ytfs.is_str_a_ytid(sup_ytid):
      return basename[: -12]
  return None


class TrailingTextStripper:

  def __init__(self, p_filename=None, p_workdir=None):
    self.lines = []
    self.newlines = []
    self.filename = p_filename or DEFAULT_FILENAME
    self.workdir = p_workdir
    self.treat_osentries()
    # self.process()

  def treat_osentries(self):
    self.treat_workdir()
    self.treat_filepath()

  def treat_workdir(self):
    if self.workdir is None or not os.path.isdir(self.workdir):
      self.workdir = os.path.abspath('.')

  def treat_filepath(self):
    if not os.path.isfile(self.file_abspath):
      warn_msg = " => Cannot process. Missing content file:"
      print(warn_msg)
      warn_msg = f"\t filename => [{self.filename}]."
      print(warn_msg)
      warn_msg = f"\t filepath => [{self.file_abspath}]."
      print(warn_msg)
      print("="*40)
      warn_msg = "For CLI arguments, run with --help or --docstr."
      print(warn_msg)


  @property
  def file_abspath(self):
    return os.path.join(self.workdir, self.filename)

  def read_input_file(self):
    if not os.path.isfile(self.filename):
      # content file does not exist
      self.lines = []
      return
    text = open(self.filename, encoding='utf8').read()
    self.lines = text.split('\n')

  def process_lines(self):
    self.newlines = []
    for line in self.lines:
      newline = strip_trailingtext_ifithappens(line)
      if newline is None:
        continue
      self.newlines.append(newline)

  def process(self):
    self.read_input_file()
    self.process_lines()
    self.printout()

  def printout(self):
    for newline in self.newlines:
      print(newline)
    if len(self.newlines) == 0:
      if os.path.isfile(self.file_abspath):
        print("Content file is empty.")


def get_cli_args():
  """
  """
  if args.docstr:
    print(__doc__)
    sys.exit(0)
  filename = args.fn or None
  workdir = args.wd or None
  return filename, workdir


def process():
  filename, workdir = get_cli_args()
  name_cutter = TrailingTextStripper(filename, workdir)
  name_cutter.process()


if __name__ == '__main__':
  process()
