#!/usr/bin/env python3
"""
~/bin/renameNumberPrefixToAnotherPartByRegex.py

Renames the number prefix in files in a folder
  replacing these numbers with another part in file that is captured by a certain regex
At the time of writing, the captured regex is a number within parentheses and its last 3 digits are discarded.
  TODO improve this captured regex so that it can be input from the CLI parameters
"""
import argparse
import glob
import os
import re
import sys
# the regex contains an arbitrary first piece ".+?", then a gap "[ ]", then any numbers within parentheses "\((\d+?)\)"
# which also makes up a group (group(1)), then a hyphen "\-", then an arbitrary last piece ".+?"
# example: "bla foo bar (9812453452524352)- bla foo bar"
# group(1) will match "9812453452524352"
DEFAULT_FILE_EXTENSION = 'mp4'
middle_regex_str = r".+?[ ]\((\d+?)\)\-.+?"
middle_regex_cmp = re.compile(middle_regex_str)
beginning_regex_str = r"^(\d+)[ ].+?"
beginning_regex_cmp = re.compile(beginning_regex_str)
number_of_rightsided_fixed_digits_to_stripout = 3
# only the 3 first digits are sought for (this run has a following 200, it should become an input parameter)
# actually, this last constant was discontinued for the rightside digit count above
rightstrip_from_middle_number = '200'
parser = argparse.ArgumentParser(description="Rename a prefix with info in another part.")
parser.add_argument("--docstr", action="store_true",
                    help="show docstr help and exit")
parser.add_argument("--rundir", type=str, default=".",
                    help="Directory in which this script willl execute, default to current dir.")
parser.add_argument("--ext", type=str, default=DEFAULT_FILE_EXTENSION,
                    help="Directory in which this script willl execute, default to current dir.")
args = parser.parse_args()


class Renamer:

  def __init__(self, basedir_abspath=None, dot_ext=None):
    self.basedir_abspath = basedir_abspath
    self.dot_ext = dot_ext or DEFAULT_FILE_EXTENSION  # it will get a prepended dot if missing
    self.filenames = []
    self.rename_pairs = []
    self.renaming_confirmed = False
    self.n_renamed = 0
    self.treat_attrs()

  def treat_attrs(self):
    if self.basedir_abspath is None or not os.path.isdir(self.basedir_abspath):
      self.basedir_abspath = os.path.abspath('.')
    if not self.dot_ext.startswith('.'):
      self.dot_ext = '.' + self.dot_ext

  def find_dot_ext_files_in_folder(self):
    files = glob.glob(self.basedir_abspath + '/*' + self.dot_ext)
    self.filenames = list(map(lambda p: os.path.split(p)[1], files))

  def form_rename_pairs(self):
    self.find_dot_ext_files_in_folder()
    total = len(self.filenames)
    for i, filename in enumerate(self.filenames):
      match = beginning_regex_cmp.match(filename)
      if not match:
        continue
      # actually, it's not needed to form the new-name, but might be used to check filename starts with a 3-digit number
      first_number = match.group(1)
      match = middle_regex_cmp.match(filename)
      if not match:
        continue
      middle_number = match.group(1)
      # middle_number = middle_number.rstrip(rightstrip_from_middle_number)
      middle_number = middle_number[: -number_of_rightsided_fixed_digits_to_stripout]
      # check if they are equal, if so, don't go on, loop-continue
      try:
        first = int(first_number)
        middle = int(middle_number)
        if first == middle:
          #  they are equal, nothing to do
          continue
        # reconstitute middle_number with zfill equals to the rightsided_fixed_digits
        middle_number = str(middle).zfill(number_of_rightsided_fixed_digits_to_stripout)
      except ValueError:
        continue
      newname = middle_number + ' ' + filename[4:]
      if filename == newname:
        continue
      rename_pair = (filename, newname)
      seq = i + 1
      scrmsg = f"""{seq}/{total} Renames:"
      FROM [{filename}]
      TO   [{newname}]
      """
      print(scrmsg)
      self.rename_pairs.append(rename_pair)

  def confirm_renames(self):
    self.renaming_confirmed = False
    scrmsg = f" Confirm the {len(self.rename_pairs)} renames above ? [Y, n] [ENTER] means Yes "
    ans = input(scrmsg)
    if ans in ['Y', 'y', '']:
      self.renaming_confirmed = True

  def do_rename(self):
    if not self.renaming_confirmed:
      print('No renames. Returning.')
      return
    for rename_pair in self.rename_pairs:
      filename, newname = rename_pair
      print('rename_pair', rename_pair)
      oldfilepath = os.path.join(self.basedir_abspath, filename)
      newfilepath = os.path.join(self.basedir_abspath, newname)
      if not os.path.isfile(oldfilepath):
        continue
      if os.path.isfile(newfilepath):
        continue
      os.rename(oldfilepath, newfilepath)
      print('renamed!')
      self.n_renamed += 1

  def process(self):
    print('Process Renaming')
    print('='*40)
    self.form_rename_pairs()
    self.confirm_renames()
    self.do_rename()


def show_docstrhelp_n_exit():
  print(__doc__)
  sys.exit(0)


def get_cli_args():
  """
  Required parameters:
    src_rootdir_abspath & trg_rootdir_abspath

  Optional parameter:
    resolution_tuple

  :return: srctree_abspath, trg_rootdir_abspath, resolution_tuple
  """
  if args.docstr:
    show_docstrhelp_n_exit()
  rundir = args.rundir  # if not given, it defaults to "."
  dot_ext = args.ext  # if not given, it defaults to "mp4" or DEFAULT_FILE_EXTENSION
  if not dot_ext.startswith('.'):
    dot_ext = '.' + dot_ext
  return rundir, dot_ext


def confirm_cli_args_with_user(ytids, dirpath, videoonlycode, audioonlycodes, nvdseq):
  if not os.path.isdir(dirpath):
    scrmsg = f"Source directory [{dirpath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  try:
    int(videoonlycode)
  except ValueError:
    scrmsg = f"videoonlycode [{videoonlycode}] should be a number. Please, retry"
    print(scrmsg)
    return False
  try:
    audioonlycodes = audioonlycodes.split(',')
  except ValueError:
    scrmsg = (f"audioonlycodes [{audioonlycodes}] should be a number list with possible sufixes."
              f" (@see also docstr for more info). Please, retry.")
    print(scrmsg)
    return False
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
  => videoonlycode = {videoonlycode} | audioonlycodes = {audioonlycodes} 
  """
  print(scrmsg)
  print(charrule)
  scrmsg = "Are the parameters above okay? (Y/n) [ENTER] means Yes "
  ans = input(scrmsg)
  print(charrule)
  confirmed = False
  if ans in ['Y', 'y', '']:
    confirmed = True
  return confirmed, audioonlycodes


def adhoctest1():
  s = "123 3' Competition among different schemata (179200)-7Ns8ktpL6FQ"
  print(s)
  print('middle_ matching...')
  matchobj = middle_regex_cmp.match(s)
  print(matchobj)
  if matchobj:
    print(matchobj.group(1))
  print(s)
  print('beginning_ matching...')
  matchobj = beginning_regex_cmp.match(s)
  print(matchobj)
  if matchobj:
    print(matchobj.group(1))


def process():
  rundir, dot_ext = get_cli_args()
  renamer = Renamer(
    basedir_abspath=rundir,
    dot_ext=dot_ext
  )
  renamer.process()


if __name__ == '__main__':
  """
  adhoctest1()
  process()
  """
  process()
