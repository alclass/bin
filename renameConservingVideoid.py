#!/usr/bin/env python3
"""
~/bin/renameConservingVideoid.py
  Renames files in a folder conserving their youtube-video-id's (already in them)
    and their dot-extension suffix,
    prepending, for the new filenames, the "phrases" in an input text file.
  The renaming follows the alphanumerical ordering.

Example of this functionality:
  Suppose a folder has one file: "file-abc_123-ABC.mp4"
  Suppose also that in the input text file there is found: "This is the new name"
  The renaming that this script does should be:
    from: "file-abc_123-ABC.mp4"
    to:   "This is the new name-abc_123-ABC.mp4
  i.e., the original video-id (abc_123-ABC) and its extension (mp4) are conserved.

Limitation:
  This script only works with one extension at time.

Caution:
  The renamings with this script cannot be undone. Use it with care.

Important:
  Care must also be taken in another sense. The new filenames will 'prepend', so to say,
  the old filenames conserving their ytid's. The renaming pair ordering is alphanumerical,
  so care must be taken here. The ytid is never lost (because it continues as-is after rename) but
  the ordering may end up not being the one desired
    (especially in cases where "10 " comes before "2 "), so take a revision before rename-confirming.

  The ideal case happens when both sides (files in directory) and names (in the input file) have some
  number-prefix sequencing, respecting left-zeroes if needed ("10 " comes after "02 "),
  because ordering is much clearer in these cases.

Dependencies:
  This script requires Python 3.4 or later.
  And a local library module for youtube-id-functions (@see imports).

Usage:
  $renameConservingVideoid.py [-e=<ext>] [-n=<newnames_input_filename>] [-dp=<'/home/user1/sci_videos'>]

Arguments:
  -e=<extension> => the file extension: examples: mp4 or webm
  -n=<newnames_input_filename> => a text file with has the new name for renaming
  -dp=<dir_path> => the directory path where renames occur

Example 1:
  $renameConservingVideoid.py -dp='/home/user1/sci_videos'

In above example, CLI the arguments will be:
  1 extension => default extension will be 'mp4'
  2 input filename => default new names textfile is 'z-titles.txt'
  3 directory path => '/home/user1/sci_videos'

Then, the script will fetch the names inside z-titles.txt and, in alphanumerical order,
  add to each one the dash-ytid-dot-extension, composing the new filenames for renaming.

Example 2:
  $renameConservingVideoid.py -e=mp3 =n=course-titles.txt -dp="/media/disk/Science"

In this example, CLI the arguments will be:
  1 extension => default extension will be 'mp3'
  2 input filename => 'course-titles.txt'
  3 directory path => '/media/disk/Science'

"""
import os
import sys
import lblib.ytfunctions.yt_str_fs_vids_sufix_lang_map_etc as ytfs  # ytfs.does_basename_end_with_dash_ytid()
DEFAULT_DOTEXTENSION = '.mp4'
DEFAULT_WORKDIR = '.'
DEFAULT_NAMES_FILENAME = 'z-titles.txt'
YT_VIDEOID_CHARSIZE = 11


def check_n_clean_or_none_as_extension_startswithadot(dotextension):
  try:
    dotextension = str(dotextension)
    extension_after_dot = dotextension.split('.')[-1]
    dotextension = '.' + extension_after_dot
    return dotextension
  except IndexError:
    return None


class Renamer(object):

  DEFAULT_DOTEXTENSION = DEFAULT_DOTEXTENSION
  DEFAULT_WORKDIR = DEFAULT_WORKDIR
  DEFAULT_NAMES_FILENAME = DEFAULT_NAMES_FILENAME

  def __init__(self, extension=None, names_filename=None, absdirpath=None):
    self.renames_confirmed = False
    self.files = []
    self.filenames = []
    self.rename_pairs = []
    self.new_filenames_w_ytid_n_dotext = []
    self.dotextension = extension
    self.names_filename = names_filename
    self.absdirpath = absdirpath
    self.treat_workdir_names_n_extension()
    # self.process()

  @property
  def ytids_in_order(self):
    ytids = []
    for fn in self.filenames:
      ytid = ytfs.extract_ytid_from_fn_w_0_or_1_ext_having_dash_ytid_sufix(fn)
      ytids.append(ytid)
    return ytids

  @property
  def new_filenames(self):
    """
    Two list ordering must be coherent, they are:
      1 the alphanumerical order of filenames (with also gets the ytid's)
      2 the alphanumerical order of names in the input file
    Because the names in the input file will replace the filenames in folder suffixing their ytid and extension
    """
    new_fns = []
    for i, pre_fn in enumerate(self.new_filenames_w_ytid_n_dotext):
      ytid = self.ytids_in_order[i]
      new_filename = f"{pre_fn}-{ytid}{self.dotextension}"
      new_fns.append(new_filename)
    return new_fns

  @property
  def names_file(self):
    return os.path.join(self.absdirpath, self.names_filename)

  def treat_workdir_names_n_extension(self):
    """
    self.dotextension = extension
    self.names_filename = names_filename
    self.absdirpath = absdirpath
    """
    self.treat_dotextension()
    self.treat_workdirpath()
    self.treat_names_filename()

  def treat_names_filename(self):
    if self.names_filename is None:
      self.names_filename = self.DEFAULT_NAMES_FILENAME
    else:
      try:
        self.names_filename = str(self.names_filename)
      except ValueError:
        self.names_filename = self.DEFAULT_NAMES_FILENAME
    if not os.path.isfile(self.names_file):
      errmsg = f"names file does not exist: [{self.names_file}]"
      raise OSError(errmsg)

  def treat_dotextension(self):
    self.dotextension = check_n_clean_or_none_as_extension_startswithadot(self.dotextension)
    if self.dotextension is None:
      self.dotextension = self.DEFAULT_DOTEXTENSION

  def treat_workdirpath(self):
    if self.absdirpath is None or not os.path.isdir(self.absdirpath):
      self.absdirpath = os.path.abspath(self.DEFAULT_WORKDIR)

  @property
  def sufix_charsize(self):
    """b
    The YouTube filename this script aims at follows the following convention:
      name + '-' + a-11-char-enc64-string + '.ext'
    In the above case, integer 11 should be attributed to constant VIDEOID_CHARSIZE

    Obs: if a different convention is followed, this script will not work (or work partially).

    In the example:
      filename = "this-is-a-videotitle-abc1-2_3def.mp4"
      This function should return "this-is-a-videotitle"
    :return:
    """
    charsize = 1 + YT_VIDEOID_CHARSIZE + len(self.dotextension)
    return charsize
    
  def get_sufixstr_ytvideoid_plus_dotext_ending(self, old_filename):
    if len(old_filename) < self.sufix_charsize + 1:
      return None
    if old_filename[-self.sufix_charsize] != '-':  # it's -16 with .mp4, ie, it's = 11 + 4 + 1
      return None
    prefix_fn = old_filename[-self.sufix_charsize:]  # this will be appended after the "new name" under renaming
    return prefix_fn

  def confirm_rename_pairs(self):
    self.renames_confirmed = False
    print('='*40)
    total_to_rename = len(self.rename_pairs)
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      old_file = rename_pair[0]
      new_file = rename_pair[1]
      old_filename = os.path.split(old_file)[1]
      new_filename = os.path.split(new_file)[1]
      print(seq, '/', total_to_rename, 'Rename:')
      print('FROM: >>>', old_filename)
      print('TO:   >>>', new_filename)
    print('='*40)
    print('In directory:', self.absdirpath)
    ans = input('Confirm the %d renames above (Y*/n)? [ENTER] means Yes' % len(self.rename_pairs))
    if ans in ['Y', 'y', '']:
      self.renames_confirmed = True

  def do_rename_if_confirmed(self):
    if not self.renames_confirmed:
      print('No confirmation or no files to renamed.')
      return
    total_to_rename = len(self.rename_pairs)
    for i, rename_pair in enumerate(self.rename_pairs):
      scrmsg = f"{i+1}/{total_to_rename} Renaming:, old_filename, 'TO', new_filename"
      print(scrmsg)
      old_filename = rename_pair[0]
      new_filename = rename_pair[1]
      old_file = os.path.join(self.absdirpath, old_filename)
      new_file = os.path.join(self.absdirpath, new_filename)
      scrmsg = f"\tfrom:  [{old_filename}]"
      print(scrmsg)
      scrmsg = f"\tto:    [{new_filename}]"
      print(scrmsg)
      scrmsg = f"\t\tin:    [{self.absdirpath}]"
      print(scrmsg)
      os.rename(old_file, new_file)
    scrmsg = ' => %d files were renamed.' % len(self.rename_pairs)
    print(scrmsg)

  def generate_renamepairs(self):
    newfilenames = self.new_filenames
    self.rename_pairs = []
    for i, filename in enumerate(self.filenames):
      newfilename = newfilenames[i]
      rename_pair = (filename, newfilename)
      self.rename_pairs.append(rename_pair)

  def the_two_lists_must_have_same_size_or_raise(self):
    if len(self.new_filenames_w_ytid_n_dotext) != len(self.filenames):
      errmsg = f"Error: the number of both filenames (in dir) and names in the inputfile must be the same" \
       f"(n_files={len(self.filenames)}<>in_input={len(self.new_filenames_w_ytid_n_dotext)})."
      raise ValueError(errmsg)

  def get_names_from_input_textfile(self):
    lines = open(self.names_file).readlines()
    for i, new_title in enumerate(lines):
      new_title = new_title.lstrip(' \t').rstrip(' \t\r\n')
      if new_title == '':
        continue
      self.new_filenames_w_ytid_n_dotext.append(new_title)
    self.the_two_lists_must_have_same_size_or_raise()

  def grab_target_files_n_their_ytids(self):
    """
    Picks up the files in absdirpath that ends with the given dot_extension
    The result is stored in instance variable (self) 'filenames': 'files' is a property (i.e. it's derivable)
    """
    entries = os.listdir(self.absdirpath)
    entries = list(filter(lambda e: e.endswith(self.dotextension), entries))
    fullentries = list(map(lambda f: os.path.join(self.absdirpath, f), entries))
    _files = list(filter(lambda f: os.path.isfile(f), fullentries))
    filenames = [os.path.split(abspathfile)[1] for abspathfile in _files]
    # filenames must end with dash-ytid plus dot-extension
    filenames = filter(lambda fn: ytfs.does_fn_w_0_or_1_ext_have_a_dash_ytid_sufix(fn), filenames)
    self.filenames = sorted(filenames)

  def process(self):
    self.grab_target_files_n_their_ytids()
    self.get_names_from_input_textfile()
    self.generate_renamepairs()
    self.confirm_rename_pairs()
    self.do_rename_if_confirmed()


def show_help():
  txt = '''
  This script
  1) takes files with a certain extension (defaulted to mp4, use parameter [-e=ext])
  2) sorts them alphabetically
  3) reads the new titles in file [[ z-rename.txt ]]
  4) forms the new filenames using the new titles conserving the videoid plus the extension
  5) ask for renaming confirmation
  6) if confirmed (ie, if n or N is not pressed), rename will occur.
  '''
  print(txt)


def get_args():
  extension = None
  names_filename = None
  dpath = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[len('-e='):]
    elif arg.startswith('--help') or arg.startswith('-h'):
      show_help()
      sys.exit(0)
    elif arg.startswith('-n='):
      names_filename = arg[len('-n='):]
    elif arg.startswith('-dp='):
      dpath = arg[len('-dp='):]
  return extension, names_filename, dpath


def process():
  extension, names_filename, dpath = get_args()
  scrmsg = f'-e="{extension}" -n="{names_filename}" -dp="{dpath}"'
  print(scrmsg)
  renamer = Renamer(extension, names_filename, dpath)
  renamer.process()


if __name__ == '__main__':
  process()
