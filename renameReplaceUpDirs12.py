#!/usr/bin/env python3
"""
~/bin/renameReplaceUpDirs12.py
  This script renames replacing a given string (s1) to another one (s2)
    in foldernames with the following characteristics:

   a) s1 can be at the end of foldername, in which case parameter 'as_endswith' should be set
   b) renaming can happen up-dir-tree recursively, in which case parameter 'dirwalk' should be set

  Its application envisages folders, not files. See other scripts here (in this folder) for file-renaming.

Usage: <this_script> -s1="<string1>" -s2="<string2>" [-as_endswith] [-dirwalk] [-basedir="<workdir>"]

Parameters:
  -s1="<string1>" | the from-string
  -s2="<string2>" | the to-string
  -as_endswith | if set, s1 will be searched at the end of foldername
  -dirwalk | if set, all up-directories (up meaning cd'ing inside recursely into subdirectories) will be processed
  -basedir="<target_directory>" | the working directory, if None, it defaults to the current working directory

Examples:

  1) $renameReplaceUpDirs12.py -s1="foo" -s2="bar"
In the example above, any foldername, in the current directory,
  containing the string "foo" in it will have it changed to the string "bar".

  2) $renameReplaceUpDirs12.py -s1="foo" -s2="bar" -as_endswith
As above but s1 string should end foldernames.

  3) $renameReplaceUpDirs12.py -s1="foo" -s2="bar"  -as_endswith -dirwalk
As above but adding recursive cd'ing processing (i.e. the current directory and all its subdirectories).

  4) $renameReplaceUpDirs12.py -s1=" au+vi" -s2="au"  -as_endswith -dirwalk -basedir="/media/disk/Science"
Similar to the one above, adding also parameter -basedir for the current working directory.
"""
import os
import sys


class Renamer:

  def __init__(self, s1, s2, as_endswith=False, dirwalk=False, base_absdir=None, autoconfirmed=False):
    self.n_renamed = 0
    self.rename_pairs = []
    self.curr_absdir = None
    self.rule40 = '-' * 40
    self.s1 = s1
    self.s2 = s2
    self.as_endswith = as_endswith
    self.dirwalk = dirwalk
    self.base_absdir = base_absdir
    self.autoconfirmed = autoconfirmed  # has not been implemented yet, it'd work as a pre-confirmed renaming
    self.user_confirmed = False
    self.treat_basedir()

  def treat_basedir(self):
    if self.base_absdir is None or not os.path.isdir(self.base_absdir):
      self.base_absdir = os.path.abspath('.')

  def do_rename(self):
    """
    Renames here are approached in the tradicional way with os.rename()

    Two other approaches are:
      1 pathlib.Path.rename()
        This one has an object-oriented approach, example:
          oldfolder = Path(oldpath)
          newfolder = Path(newpath)
          oldfoder.rename(newfolder)
      2 shutil.move()
        It has the same procedural approach of os.rename()
        It works across filesystems, but this script is supposed to only rename (not exactly move across filesystems)
    """
    if not self.user_confirmed:
      print('No renamings or not confirmed. Returning.')
      return False
    self.n_renamed = 0
    total_to_rename = len(self.rename_pairs)
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      scrmsg = f"{seq}/{total_to_rename} renaming | {self.n_renamed} renamed"
      print(scrmsg)
      print(self.rule40)
      # from_abspath
      from_abspath = rename_pair[0]
      scrmsg = f"\tfrom: [{from_abspath}]"
      print(scrmsg)
      # from_abspath
      to_abspath = rename_pair[1]
      scrmsg = f"\tto:   [{to_abspath}]"
      print(scrmsg)
      print(self.rule40)
      os.rename(from_abspath, to_abspath)
      self.n_renamed += 1
    print('total renames:', self.n_renamed)
    return True

  def confirm_renames(self):
    """
    The user, if autoconfirm is False, is asked for confirmation.
    """
    if self.autoconfirmed:
      self.user_confirmed = True
      return
    self.user_confirmed = False
    total_to_rename = len(self.rename_pairs)
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      from_abspath = rename_pair[0]
      to_abspath = rename_pair[1]
      scrmsg = f"{seq}/{total_to_rename} pair to rename"
      print(scrmsg)
      print(self.rule40)
      scrmsg = f"\tfrom: [{from_abspath}]"
      print(scrmsg)
      scrmsg = f"\tto:   [{to_abspath}]"
      print(scrmsg)
      print(self.rule40)
    scrmsg = f"Confirm the {len(self.rename_pairs)} renames above? (*Y/n) [ENTER] means Yes."
    ans = input(scrmsg)
    if ans in ['', 'Y', 'y']:
      self.user_confirmed = True
    return

  def invert_rename_queue(self):
    """
    The rename queue must be inverted (order-reversed) because 'outter' subdirectories must be renamed first,
      or, in other words, renaming should 'happen' downward. The following example make this clear:

    Suppose the renames are:
      ("basedir/Science au+vi", "basedir/Science au"),
      ("basedir/Science au+vi/Physics au+vi", "basedir/Science au/Physics au"),
      ("basedir/Science au+vi/Physics au+vi/Quantum au+vi", "basedir/Science au/Physics au/Quantum au"),

    If the above list is processing from first to last,
      the second rename will have a source-directory (rename-from) that does no longer exist, ie:

        -> after 1st rename: "basedir/Science au+vi" became "basedir/Science au"

      at the moment the second rename will happen, it will search for "basedir/Science au+vi/Physics au+vi",
        but, the middle foldername no longer exists, because it was renamed to "basedir/Science au/Physics au+vi"

    Then, one solution (perhaps the simplest) is to invert (order-reverse) the renaming list.
    """
    self.rename_pairs.reverse()

  def gather_folders(self, foldernames):
    """
    self.as_endswith = as_endswith
    """
    for foldername in foldernames:
      found = False
      if self.as_endswith:
        if foldername.endswith(self.s1):
          found = True
      else:
        if foldername.find(self.s1) > -1:
          found = True
      if not found:
        continue
      new_foldername = foldername.replace(self.s1, self.s2)
      from_abspath = os.path.join(self.curr_absdir, foldername)
      to_abspath = os.path.join(self.curr_absdir, new_foldername)
      rename_pair = (from_abspath, to_abspath)
      self.rename_pairs.append(rename_pair)

  def walkup_dirs(self):
    """
    self.dirwalk = dirwalk
    """
    for self.curr_absdir, foldernames, _ in os.walk(self.base_absdir):
      self.gather_folders(foldernames)
      if not self.dirwalk:
        # if not dirwalk, the current directory has already been gathered, do not loop on
        break

  def process(self):
    self.walkup_dirs()
    self.invert_rename_queue()
    self.confirm_renames()
    self.do_rename()


def get_args():
  """
  Module argparse could be used in the future, refactoring this one.
  But, for the time being, this approach seems fine.
  """
  s1, s2, as_endswith, dirwalk, basedir = None, None, False, False, None
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-s1='):
      s1 = arg[len('-s1='):]
    elif arg.startswith('-s2='):
      s2 = arg[len('-s2='):]
    elif arg.startswith('-as_endswith'):
      as_endswith = True
    elif arg.startswith('-dirwalk'):
      dirwalk = True
    elif arg.startswith('-basedir'):
      basedir = arg[len('-basedir='):]
  args_dict = {'s1': s1, 's2': s2, 'as_endswith': as_endswith, 'dirwalk': dirwalk, 'basedir': basedir}
  return args_dict


def adhoc_test():
  pass


def process():
  args_dict = get_args()
  ad = args_dict
  s1, s2, as_endswith, dirwalk, basedir = ad['s1'], ad['s2'], ad['as_endswith'], ad['dirwalk'], ad['basedir']
  scrmsg = f"s1={s1} | s2={s2} | as_endswith={as_endswith} | dirwalk={dirwalk} | basedir={basedir}"
  print(scrmsg)
  renamer = Renamer(s1, s2, as_endswith, dirwalk, basedir)
  renamer.process()


if __name__ == '__main__':
  # adhoc_test()
  process()
