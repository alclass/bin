#!/usr/bin/env python3
"""
~/bin/uTubeShowYtidRepeatsInDirTree.py
  Lists repeat ytids in a directory and also shows a ytid counting statistics.

The DirTree functionality (which would show the counting for the whole directory tree)
  has not yet been done. For the time being, it counts only the current or appointed directory.

The first application (a kind of extended one) of this script was to help find
  the differences of mp3's derived from mp4's in two directories.
  Because the number of files was big, it helped find the missing ones, running this script twice,
  once for each directory (mp3's & mp4's).
"""
import argparse
import os.path
import sys
import lblib.ytfunctions.yt_str_fs_vids_sufix_lang_map_etc as ytfs  # ytfs.is_str_a_ytid()
parser = argparse.ArgumentParser(description="Show ytid stats in a folder or dirtree.")
parser.add_argument("--docstr", action="store_true",
                    help="show docstr help and exit")
parser.add_argument("--dirpath", type=str,
                    help="Directory from which ytid stats will be gather")
args = parser.parse_args()


def show_docstrhelp_n_exit():
  print(__doc__)
  sys.exit(0)


def get_the_3_ytid_filename_pieces_or_nones(filename):
  """
  Returns the 3 conventioned parts (or pieces) of a ytid filename or, in case it fails the convention, a triple None.

  The 3 ytid-conventioned filename parts are:
    1 => the filename's prename
    2 => its ytid
    3 => its dot_ext (though optional, only a single extension is allowed)

  The convention is:
    => any previous name, a dash (hyphen), the 11-char ENC64 string and a dot extension

  Examples:

    1) file1-ABCabc123-_.mp4
      =>
        1-1 its prename is "file1"
        1-2 its ytid is "ABCabc123-_"
        1-3 its dot_ext ".mp4"

    2) "bla foo bar-abc-123_DEF.mp3" => its ytid is "abc-123_DEF"
      =>
        1-1 its prename is "bla foo bar"
        1-2 its ytid is "abc-123_DEF"
        1-3 its dot_ext ".mp3"

  """
  name, dot_ext = os.path.splitext(filename)
  try:
    prename = name[:-12]
    supposed_ytid = name[-12:]
    if not supposed_ytid.startswith('-'):
      return None, None, None
    supposed_ytid = supposed_ytid[1:]
    if ytfs.is_str_a_ytid(supposed_ytid):
      ytid = supposed_ytid
      return prename, ytid, dot_ext
  except IndexError:
    pass
  return None, None, None


def is_filename_a_ytid_conventioned_one(filename):
  _, ytid, _ = get_the_3_ytid_filename_pieces_or_nones(filename)
  if ytid is None:
    return False
  return True


class YtidsInDirLookerUp:

  def __init__(self, dir_abspath=None):
    self.dir_abspath = dir_abspath
    self.filenames = []
    self.n_files = 0
    self.ytid_n_filename_dict = {}
    self.ytid_repeat_set = set()
    self.ytidrepeat_filenames = []
    self.treat_attrs()

  def treat_attrs(self):
    if self.dir_abspath is None or not os.path.isdir(self.dir_abspath):
      self.dir_abspath = os.path.abspath('.')

  @property
  def n_ytid_files(self):
    return len(self.ytid_n_filename_dict)

  @property
  def ytid_repeats(self):
    return list(self.ytid_repeat_set)

  @property
  def n_ytid_repeats(self):
    return len(self.ytidrepeat_filenames)

  @property
  def total_ytid_files(self):
    n1 = self.n_ytid_files
    n2 = self.n_ytid_repeats
    return n1 + n2

  def get_n_store_ytidfilenamesdict_in_dir(self):
    entries = os.listdir(self.dir_abspath)
    for entry in entries:
      # it's assumed a ytid-conventioned dirname is not there
      _, ytid, _ = get_the_3_ytid_filename_pieces_or_nones(entry)
      if ytid is None:
        continue
      if ytid in self.ytid_n_filename_dict:
        self.ytid_repeat_set.add(ytid)
        self.ytidrepeat_filenames.append(entry)
        continue
      self.ytid_n_filename_dict[ytid] = entry

  def process(self):
    print(f'Processing dir {self.dir_abspath}')
    self.get_n_store_ytidfilenamesdict_in_dir()
    print(self)

  def list_all_ytids(self):
    for ytid in self.ytid_n_filename_dict:
      print(ytid)

  def __str__(self):
    outstr = f"""
    n_ytid_files = {self.n_ytid_files}
    total_ytid_files = {self.total_ytid_files}
    ytid_repeats = {self.ytid_repeat_set}
    ytid_filename_repeats = {self.ytidrepeat_filenames}
    n of excess repeats = {len(self.ytidrepeat_filenames)}
    """
    return outstr


def get_args():
  dirpath = args.dirpath or "."
  return dirpath


def adhoctest2():
  test = """
  filename without extension-gD0VfFTu6V8
  """
  lines = test.split('\n')
  for i, line in enumerate(lines):
    line = line.lstrip(' \t').rstrip(' \t\r\n')
    triple = get_the_3_ytid_filename_pieces_or_nones(line)
    prename, ytid, dot_ext = triple
    seq = i + 1
    scrmsg = f"{seq} | prename=[{prename}] ytid={ytid} dot_ext={dot_ext} [{line}]"
    print(scrmsg)


def adhoctest1():
  """
  Notice that the first test below shows that any extension is allowed for the convention,
    but the one that has a double extension (dot_ext + dot_ext) "fails" the convention
  """
  test = """
  248 3' How I see artificial intelligence now (248248)-gD0VfFTu6V8.cnv.mp3
  248 3' How I see artificial intelligence now (248248)-gD0VfFTu6V8.mp3
  248 3' How I see artificial intelligence now (248248)-gD0VfFTu6V8.empty
  """
  lines = test.split('\n')
  for i, line in enumerate(lines):
    line = line.lstrip(' \t').rstrip(' \t\r\n')
    triple = get_the_3_ytid_filename_pieces_or_nones(line)
    prename, ytid, dot_ext = triple
    seq = i + 1
    scrmsg = f"{seq} | prename=[{prename}] ytid={ytid} dot_ext={dot_ext} [{line}]"
    print(scrmsg)


def process():
  """


  :return:
  """
  dirpath = get_args()
  looker = YtidsInDirLookerUp(dir_abspath=dirpath)
  looker.process()
  # looker.list_all_ytids()


if __name__ == '__main__':
  """
  process()
  adhoctest1()
  adhoctest2()
  """
  process()
