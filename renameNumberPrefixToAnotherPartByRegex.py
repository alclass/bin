#!/usr/bin/env python3
"""
~/bin/renameNumberPrefixToAnotherPartByRegex.py

Renames the number prefix in files in a folder
  replacing these numbers with another part in file that is captured by a certain regex
At the time of writing, the captured regex is a number within parentheses and its last 3 digits are discarded.
  TODO improve this captured regex so that it can be input from the CLI parameters
"""
import glob
import os
import re
# the regex contains an arbitrary first piece ".+?", then a gap "[ ]", then any numbers within parentheses "\((\d+?)\)"
# which also makes up a group (group(1)), then a hyphen "\-", then an arbitrary last piece ".+?"
# example: "bla foo bar (9812453452524352)- bla foo bar"
# group(1) will match "9812453452524352"
default_dot_ext = '.mp4'
middle_regex_str = r".+?[ ]\((\d+?)\)\-.+?"
middle_regex_cmp = re.compile(middle_regex_str)
beginning_regex_str = r"^(\d+)[ ].+?"
beginning_regex_cmp = re.compile(beginning_regex_str)
number_of_rightsided_fixed_digits_to_stripout = 3
# only the 3 first digits are sought for (this run has a following 200, it should become an input parameter)
# actually, this last constant was discontinued for the rightside digit count above
rightstrip_from_middle_number = '200'


class Renamer:

  def __init__(self, basedir_abspath=None, dot_ext=None):
    self.basedir_abspath = basedir_abspath
    self.dot_ext = dot_ext or default_dot_ext
    self.filenames = []
    self.rename_pairs = []
    self.renaming_confirmed = False
    self.n_renamed = 0
    self.treat_attrs()

  def treat_attrs(self):
    if self.basedir_abspath is None or not os.path.isdir(self.basedir_abspath):
      self.basedir_abspath = os.path.abspath('.')
    if not self.dot_ext.startswith('.'):
      self.dot_ext = '+' + self.dot_ext

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
      # first_number = match.group(1)
      match = middle_regex_cmp.match(filename)
      if not match:
        continue
      middle_number = match.group(1)
      # middle_number = middle_number.rstrip(rightstrip_from_middle_number)
      middle_number = middle_number[: -number_of_rightsided_fixed_digits_to_stripout]
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
  renamer = Renamer()
  renamer.process()


if __name__ == '__main__':
  """
  adhoctest1()
  process()
  """
  process()
