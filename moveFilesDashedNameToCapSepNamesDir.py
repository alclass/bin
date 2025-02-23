#!/usr/bin/env python3
"""
~/bin/moveFilesDashedNameToCapSepNamesDir

This script moves files into directories that bind to a certain specified convention.

This convention, not "openly general" at this time, is the following:

1) suppose a filename that has a name-dash-surname (or any word dash another),
   and this name-dash-surname exactly after a word and a space (gap),
   e.g.:
    "50' albert-einstein theory of relativity. ext"
   (notice that the pre-string "50' " is a word plus a space)

2) for this example above, this script will move it to the following directory:
  <base-dir>/A/AL

  ie,
  subdirectory "A" is because first name starts with A ([A]lbert)
  subdirectory "AL", inside "A", is because first name starts with AL ([Al]bert)
  resulting in path "<base-dir>/A/AL"
  where <base-dir> is the absolute directory acting as 'base dir path'

How <base-dir> is given
=======================

If <base-dir> is not given, the script will convention it to be "../..",
ie, the second directory above the executing directory
notice also that the files-to-move must be located in the running directory
(this parameter [source folder for the input files] is not available for the time being)


  1) <base-dir> default (when none is given at the command line):
    as said above, if none <base-dir> is given, it's "../..",
    ie the parent of the parent folder

  1) giving <base-dir> in the command line:
    parameter [-b "<base-dir>"] gives a determined chosen <base-dir>

  Where <base-dir> is the directory from where
    the "alphabet folders (A, B, C...)" are placed on.

Examples:
  $<script> -b /this/videodir

Suppose that in the executing directory one has file
    "50' albert-einstein theory of relativity. ext"

The script will move this file to:
    /this/videodir/"50' albert-einstein theory of relativity. ext"

"""
import glob
import os
import sys
import shutil
from pathlib import Path
default_dot_ext = '.mp4'


def derive_firstletter_capitalized_names_from_dashed_lowercase(dashedname):
  """
  Transforms dashed-name to Capitalized first letter words
    E.g.
      input => "albert-einstein"
      output => "Albert Einstein"

    Notice that "albert-einstein" is a valid "logic" input,
       and "albert -einstein" will result, from the logic in here, in only "Albert" as name.
  """
  # newname = ''
  pp = dashedname.split('-')
  names = []
  for name in pp:
    name = name.strip(' ')
    if name.find(' ') > -1:
      name = name.split(' ')[0]
    names.append(name)
  newname = ''
  for current_word in pp:
    if len(current_word) > 1:
      current_word = current_word[0].upper() + current_word[1:]
    elif len(current_word) == 1:
      current_word = current_word[0].upper()
    else:
      continue
    newname += current_word + ' '
  newname = newname.rstrip(' ')
  print('treat_name_to_move =>', dashedname, '=>', newname)
  return newname


def get_childpath_based_on_secondleveldir_n_name(secondlevel_dirpath, cap_sep_name):
  targetentries = os.listdir(secondlevel_dirpath)
  for entry in targetentries:
    if entry.lower().startswith(cap_sep_name.lower()):
      childpath = os.path.join(secondlevel_dirpath, entry)
      if os.path.isdir(childpath):
        return childpath
  return None


def create_dirpaths(paths_not_existing):
  for ppath in paths_not_existing:
    if os.path.isdir(ppath):
      continue
    print('Creating dirpath', ppath)
    os.makedirs(ppath)

class FilenameItem:

  conventioned_suffix_for_topdirname = 'yyyy cc'
  def __init__(self, orig_filename):
    self.orig_filename = orig_filename
    self._names = None
    self.dashednames_str = None
    self.set_dashnames_str()
    # self.treat_dashedname(dashedname)

  def set_dashnames_str(self):
    """
    The convention says the dash-names string should be the 2nd word in orig_filename
    Taking this 2nd word, if it doesn't have a 'dash', name is single ie it's a one-word name
    """
    try:
      pp = self.orig_filename.split(' ')
      if len(pp) > 1:
        self.dashednames_str = pp[1]
    except ValueError:
      errmsg = 'orig-filename [%s] does not follow the convention' % self.orig_filename
      raise ValueError(errmsg)

  @property
  def names(self):
    """
    Each name in names should have, if it's not, its first letter capitalized
    """
    if self._names is not None:
      return self._names
    self._names = []
    for name in self.dashednames_str.split('-'):
      if name == '':
        continue
      if name[0] == name[0].lower():
        if len(name) == 1:
          name = name.upper()
        else:
          name = name[0].upper() + name[1:]
      self._names.append(name)
    return self._names

  @property
  def spaced_names_str(self):
    return ' '.join(self.names)

  @property
  def capitalized_letters_from_eachname_aslist(self):
    capletters = []
    for currname in self.names:
      capletters.append(currname[0])
    return capletters

  @property
  def firstcapletter(self):
    if len(self.names) > 0:
      firstname = self.names[0]
      if len(firstname) > 0:
        return firstname[0:1]
    return None

  @property
  def firsttwocapletters(self):
    if len(self.names) > 0:
      firstname = self.names[0]
      if len(firstname) > 1:
        return firstname[0:2]
    return None

  @property
  def letter_n_doubleletter_middledirs(self):
    """
    e.g. Albert-Einsten makes 'A/AL' the AL from [Al]bert
    """
    first = self.firstcapletter
    if first is None:
      return None
    second = self.firsttwocapletters
    # notice that the second lever may not be capitalized, so do it here
    if second is None:
      second = first
    second = second.upper()
    middledirs_str = first + '/' + second
    return middledirs_str

  @property
  def capitalized_firsttwoletters_from_firstname_aslist(self):
    middledirs_convention_str = self.letter_n_doubleletter_middledirs
    if middledirs_convention_str:
      return list(middledirs_convention_str.split('/'))
    return None

  def form_conventioned_topdirname(self):
    return self.spaced_names_str + ' ' + self.conventioned_suffix_for_topdirname

  def form_basedir_plus_lettermiddlepath(self, basedir):
    """
    To be called from an AlphabetMover object, or any one that 'knows' basedir
    The result path may or not exist, the caller should find out (maybe ask its creation...)
    """
    return os.path.join(basedir, self.letter_n_doubleletter_middledirs)

  def form_basedir_lettermiddlepath_n_convention(self, basedir):
    middlepath = self.form_basedir_plus_lettermiddlepath(basedir)
    conventioned_topdirname = self.form_conventioned_topdirname()
    return os.path.join(middlepath, conventioned_topdirname)

  def discover_an_folder_with_a_changedsufix(self, basedir):
    middlepath = self.form_basedir_plus_lettermiddlepath(basedir)
    entries = os.listdir(middlepath)
    direntries = map(lambda e: os.path.join(middlepath, e), entries)
    dirpaths = filter(os.path.isdir, direntries)
    for dirpath in dirpaths:
      _, foldername = os.path.split(dirpath)
      if foldername.startswith(self.spaced_names_str):
        # found !
        return dirpath
    return None

  def get_basedir_lettermiddlepath_name_or_convention(self, basedir):
    dirpath = self.discover_an_folder_with_a_changedsufix(basedir)
    if dirpath is None:
      return self.form_basedir_lettermiddlepath_n_convention(basedir)
    return dirpath

  def as_str_dict(self):
    _as_str_dict = {
      'dashednames_str': {self.dashednames_str},
      'spaced_names_str': {self.spaced_names_str},
      'capitalized_letters_from_eachname_aslist': {str(self.capitalized_letters_from_eachname_aslist)},
      'capitalized_firsttwoletters_from_firstname_aslist': \
        {str(self.capitalized_firsttwoletters_from_firstname_aslist)},
      'names': {str(self.names)},
    }
    return _as_str_dict

  def __str__(self):
    outstr = """
      dashednames_str = [{dashednames_str}] | spaced_names_str = [{spaced_names_str}]
      capitalized_letters_from_eachname_aslist = {capitalized_letters_from_eachname_aslist}
      capitalized_firsttwoletters_from_firstname_aslist = {capitalized_firsttwoletters_from_firstname_aslist}
      names = {names}
    """.format(**self.as_str_dict())
    return outstr


class AlphabetFileMover:

  def __init__(self, basedir, dot_ext=None, sourcedir=None):
    self.dot_ext = dot_ext
    self.treat_dot_ext()
    self.sourcedir = sourcedir
    self.treat_sourcedir()
    self.src_filenames = []
    self.move_pair_list = []
    self.paths_not_existing = []
    self.basedir = basedir
    self.treat_basedir()
    # 3) find among target folder paths those that do not exist

  def verify_target_folders_existence(self):
    """
    This function looks up all target dirpaths checking its existence
    It stores all non-existing to an attribute that will be used
      next on in the object's processing order
    """
    self.paths_not_existing = []
    for movepair in self.move_pair_list:
      targetpath = movepair[1]
      if not os.path.isdir(targetpath):
        self.paths_not_existing.append(targetpath)

  def create_target_folders_if_needed(self):
    """
    # user confirmation
    """
    if len(self.paths_not_existing) == 0:
      return
    for i, targetpath in enumerate(self.paths_not_existing):
      n_path = i + 1
      scrmsg = '%d targetpath [%s] does not exist.' % (n_path, targetpath)
      print(scrmsg)
    scrmsg = 'Confirm creation of the %d paths above ? (Y/n) [ENTER] means Yes ' % \
             len(self.paths_not_existing)
    ans = input(scrmsg)
    if ans in ['Y', 'y', '']:
      create_dirpaths(self.paths_not_existing)


  def move_source_files_to_target_folders(self):
    if len(self.move_pair_list) == 0:
      print('No files to move.')
      return
    for i, movepair in enumerate(self.move_pair_list):
      seq = i + 1
      filename = movepair[0]
      sourcefilepath = os.path.join(self.sourcedir, filename)
      targetpath = movepair[1]
      if os.path.isfile(sourcefilepath) and os.path.isdir(targetpath):
        print(seq, 'Moving')
        print('\tFROM :', sourcefilepath)
        print('\tTO   :', targetpath)
    scrmsg = 'Confirm moving the %d files above ? (Y/n) [ENTER] means Yes ' % len(self.move_pair_list)
    ans = input(scrmsg)
    if ans not in ['Y', 'y', '']:
      print('Not moving and returning.')
      return
    print('='*40)
    print('Initiating moving')
    print('='*40)
    for i, movepair in enumerate(self.move_pair_list):
      seq = i + 1
      filename = movepair[0]
      sourcefilepath = os.path.join(self.sourcedir, filename)
      targetpath = movepair[1]
      shutil.move(sourcefilepath, targetpath)
      print(seq, 'Moved')
      print('\tFROM :', sourcefilepath)
      print('\tTO   :', targetpath)

  def treat_dot_ext(self):
    if self.dot_ext is None:
      self.dot_ext = default_dot_ext
    if not self.dot_ext.startswith('.'):
      self.dot_ext = '.' + self.dot_ext

  def treat_sourcedir(self):
    if self.sourcedir is None:
      # default to current (running) directory
      self.sourcedir = os.path.abspath(os.curdir)
    if not os.path.isdir(self.sourcedir):
      errmsg = 'Source directory [%s] does not exist.' % self.sourcedir
      raise OSError(errmsg)

  def treat_basedir(self):
    if self.basedir is None:
      # default to parent's parent directory
      self.basedir = os.path.abspath('../..')
    if not os.path.isdir(self.basedir):
      errmsg = 'base directory [%s] does not exist.' % self.basedir
      raise OSError(errmsg)

  def deduce_target_folderpaths_file_by_file(self):
    """
    Step 2: deduce_target_folderpaths_file_by_file
    """
    for eachfile in self.src_filenames:
      fileitem = FilenameItem(eachfile)
      move_to_dir = fileitem.form_basedir_lettermiddlepath_n_convention(self.basedir)
      pair = (eachfile, move_to_dir)
      self.move_pair_list.append(pair)


  def gather_source_files_to_move_to_dirs(self):
    """
    Step 1: gather_source_files_to_move_to_dirs
    """
    filenames = os.listdir(self.sourcedir)
    self.src_filenames = list(filter(lambda f: f.endswith(self.dot_ext), filenames))

  def process_move(self):
    # 1) gather local dir source files
    self.gather_source_files_to_move_to_dirs()
    # 2) deduce target folder paths
    self.deduce_target_folderpaths_file_by_file()
    # 3) find among target folder paths those that do not exist
    self.verify_target_folders_existence()
    # 4) if any target folder paths does not exist, confirm ask it creation
    self.create_target_folders_if_needed()
    # 5) move source files to target folders
    self.move_source_files_to_target_folders()

  def as_str_dict(self):
    _as_str_dict = {
      'basedir': {self.basedir},
      'dot_ext': {self.dot_ext},
      'sourcedir':  {self.sourcedir},
    }
    return _as_str_dict

  @property
  def filenamelist_str(self):
    _filenamelist_str = ''
    for eachfile in self.src_filenames:
      _filenamelist_str += eachfile + '\n'
    return _filenamelist_str

  @property
  def movepairlist_str(self):
    _movepairlist_str = ''
    for eachpair in self.move_pair_list:
      _movepairlist_str += str(eachpair) + '\n'
    return _movepairlist_str

  def __str__(self):
    header = """
    basedir = {basedir}
    dot_ext = {dot_ext}
    sourcedir = {sourcedir}
    """.format(**self.as_str_dict())
    outstr = header + '\n' + self.filenamelist_str
    outstr = outstr + '\n' + self.movepairlist_str
    return outstr


def find_second_level_dirpath_from_name(self, cap_sep_name):
  """
  maybe incomplete as yet
  """
  if cap_sep_name is None:
    return None
  firstletter = cap_sep_name[0]
  firstdir = os.path.join(self.basedir, firstletter)
  if not os.path.isdir(firstdir):
    return None
  print('firstdir =>', firstdir)
  if not os.path.isdir(second_level_dirpath):
    return None
  print('seconddir =>', second_level_dirpath)
  return second_level_dirpath


def move_pairs(move_pair_list):
  for i, move_pair in enumerate(move_pair_list):
    filename, cap_sep_name = move_pair
    targetentry = find_n_get_folder(cap_sep_name)
    seq = i + 1
    print(seq)
    print('FROM: ', filename)
    print('TO:   ', targetentry)
    if targetentry is not None:
      print('Moving...')
      shutil.move(filename, targetentry)
  
def get_args():
  basedir = None
  dot_ext = None
  sourcedir = None
  for arg in sys.argv:
    print(arg)
    if arg.startswith('-b='):
      basedir = arg[len('-b='):]
    elif arg.startswith('-e='):
      dot_ext = arg[len('-e='):]
      if not dot_ext.startswith('.'):
        dot_ext = '.' + dot_ext
    elif arg.startswith('-s='):
      sourcedir = arg[len('-s='):]
  return basedir, dot_ext, sourcedir


def adhoc_test1():
  it = FilenameItem("'10' albert-einstein relativity.")
  print(it)
  dirpath = it.form_basedir_plus_lettermiddlepath('/dados/Science/Phy')
  print(dirpath)

def process():
  """
  """
  basedir, dot_ext, sourcedir = get_args()
  print('Params')
  print('basedir | dot_ext | sourcedir', basedir, ' | ', dot_ext, ' | ', sourcedir)
  alphabetmover = AlphabetFileMover(basedir, dot_ext, sourcedir)
  alphabetmover.process_move()


if __name__ == '__main__':
  process()
