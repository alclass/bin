#!/usr/bin/env python3
"""
~/bin/extractLinesWithNumberDashNumber.py

"""
import re
import sys
# from extractYtidsFromText import get_args
restr_beginsdashednumber = r"^(?P<dashednumber>\d{1,3}\-\d{1,2})"  # [ ].*$"
recmp_beginsdashednumber = re.compile(restr_beginsdashednumber)
DEFAUT_VIDEOFORMAT_FILENAME = 'yt_videoformat_output.txt'


class LinesExtractor:

  def __init__(self, infilename=None, workdir=None, do_stdin=False, text=None):
    self.n_found = 0
    self.infilename = infilename
    self.workdir = workdir
    self.do_stdin = do_stdin
    self.lines = []
    if self.do_stdin:
      for line in sys.stdin:
        line = line.strip()
        self.lines.append(line)
    elif text:
      self.lines = text.split('\n')
    else:
      self.lines = open(infilename, 'r').readlines()
    _ = self.lines

  def extractline_ifso(self, line):
    # print('looking up', self.n_found, line)
    m_obj = recmp_beginsdashednumber.match(line)
    if m_obj:
      self.n_found += 1
      matchstr = m_obj.group('dashednumber')
      scrmsg = f'matched {matchstr}'
      print(scrmsg)

  def loop_lines(self):
    for line in self.lines:
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      self.extractline_ifso(line)

  def process(self):
    self.loop_lines()


def adhoctest1():
  text = """
  12-0 bla
  32-4
  adfadfa
  452452
  32-32
  """
  extractor = LinesExtractor(text=text)
  extractor.process()


def get_args():
  infilename, workdir, do_stdin = None, None, False
  for arg in sys.argv[1:]:
    if arg.startswith("-h"):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith("-if"):
      infilename = arg[len("-if"):]  # if a '=' follows, it expects a filename
      if infilename == '':
        infilename = DEFAUT_VIDEOFORMAT_FILENAME
      infilename.strip('=')
    elif arg.startswith("-wd="):
      workdir = arg[len("-wd="):]
    elif arg.startswith("-stdin"):
      do_stdin = True
      break
  return infilename, workdir, do_stdin


def process():
  infilename, workdir, do_stdin = get_args()
  extractor = LinesExtractor(
    infilename=infilename,
    workdir=workdir,
    do_stdin=do_stdin,
  )
  extractor.process()


if __name__ == "__main__":
  """
  adhoctest1()
  process()
  """
  adhoctest1()
