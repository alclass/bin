#!/usr/bin/env python3
"""
~/bin/extractYtidsFromText.py

This script extracts ytids with brackets (the current form of yt-dlp)
  either from a textfile or from stdin

Usage:
  this_script [--useinputfile] [--infile <filename>]

Notice that the two parameters above are optional.
  If the user wants to use stdin (to pipe text in),
  she must be the redirection from the command line
  (@see example below)

Where:
  --useinputfile: a flag to read the text in filenamed youtube-names.txt
  --infile: a filename from which the text will be read

Examples:
  1
  $this_script < inputfile.txt > outputfile.txt

  In this example, no parameter is given
    but input file is piped in and the output is redirected.

  2
  $this_script --useinputfile

  In this example, the program will look for file youtube-ids.txt
    in the current (running) directory. The output will go to stdout
    (the screen).

  3
  $this_script --infile inputfile.txt > youtube-ids.txt

  In this example, the program will read file inputfile.txt
    from the current (running) directory. The output will be redirected
    to file youtube-ids.txt.
"""
import argparse
import os
import sys
import re
restr_ytid_wi_brackets = r"^.*?\[(?P<ytid>[A-Za-z0-9\-_]{11})\].*$"
recmp_ytid_wi_brackets = re.compile(restr_ytid_wi_brackets)
default_filename = "youtube-names.txt"
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--docstr", action="store_true",
                    help="show docstr help and exit")
parser.add_argument("--useinputfile", action='store_true',
                    help="read the default ytids input file")
parser.add_argument("--infile", type=str,
                    help="input filename as a local dir file")
parser.add_argument("--dirpath", type=str,
                    help="Directory recipient of the download")
args = parser.parse_args()


class Extractor:

  def __init__(self):
    self.use_stdin, self.infile, self.useinputfile = get_args()
    self.n_ytids = 0
    self.ytids = []

  def extract_ytids_from_line(self, line):
    mo = recmp_ytid_wi_brackets.match(line)
    if mo:
      ytid = mo.group('ytid')
      self.n_ytids += 1
      self.ytids.append(ytid)
    return None

  def extract_ytids_from_text(self, text):
    lines = text.split('\n')
    for line in lines:
      self.extract_ytids_from_line(line)
    return None

  def extract_ytids_from_stdin(self):
    for line in sys.stdin:
      self.extract_ytids_from_line(line)
    return None

  def fork_process_option(self):
    if self.use_stdin:
      self.extract_ytids_from_stdin()
    elif self.useinputfile:
      text = open(default_filename).read()
      self.extract_ytids_from_text(text)
    elif self.infile and os.path.isfile(self.infile):
      text = open(self.infile).read()
      self.extract_ytids_from_text(text)
    else:
      scrmsg = 'Nothing to do or input file does not exist. If so, set parameters for execution.'
      print(scrmsg)
    # avoiding the use of set() to maintain order

  def process(self):
    self.fork_process_option()
    self.unicize_ytids()
    self.show_ytids()

  def unicize_ytids(self):
    """
    Removes repeats from ytids
    The set() function is avoided here
      so that sequencial order is mantained in the ytids list
    """
    _ytid = []
    for e in self.ytids:
      if e not in _ytid:
        _ytid.append(e)
    self.ytids = _ytid

  def show_ytids(self):
    scrmsg = f'# Total {len(self.ytids)} ytids'
    print(scrmsg)
    for ytid in self.ytids:
      print(ytid)


def adhoctest1():
  t = "Uma ótima semana para os brasileiros (e péssima para o Jair e sua cambada de golpistas) [rDhnusqVXss].f160.mp4"
  mo = recmp_ytid_wi_brackets.match(t)
  if mo:
    print('ytid', mo.group('ytid'))


def get_args():
  use_stdin = True
  infile = args.infile
  useinputfile = args.useinputfile
  if infile is None and useinputfile is None:
    use_stdin = True
  return use_stdin, infile, useinputfile


def process():
  extractor = Extractor()
  extractor.process()


if __name__ == '__main__':
  """
  adhoctest1()
  process()
  """
  process()
