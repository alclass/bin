#!/usr/bin/env python3
"""

"""
import glob
import json
import os
import string
import subprocess
import sys

DEFAULT_EXTENSION = 'mp4'


def print_explanation_and_exit():
  print('''
  Script's function:
  ==================

  This script ...
  
  Example:
  
  Suppose current folder has the following file:
  (...)
  
  Supposing it has 11 minutes duration, the script will rename it to:
  "This 11' video is about Physics.mp4"
  ie, it puts a ((11')) (an eleven [one one] and a plics)
      in-between "This" and "video".
    
  Arguments to the script:
  =======================

  -e=<file-extension> (if not given, default is %s [do not use the dot '.' before extension])
  -y avoids confirmation, ie, it does the renaming without asking a confirm Yes or No
  -h or --help prints this help message
''') % DEFAULT_EXTENSION
  sys.exit(0)


def get_the_longest_equal_prefixing_string(fromstring, tostring):
  result_prefix = ''
  tolist = list(reversed(tostring))
  for c in fromstring:
    print('c =>', c)
    if len(tolist) == 0:
      break
    if c == tolist[-1]:
      result_prefix += tolist.pop()
    else:
      break
  return result_prefix


def verify_longest_word_unicity(words):
  """
  words is a list of strings
  Here is how this function works:
    1) the function here sorts the list on charsize
    2) if the greatest word has a second one with the same size, return None
    3) if the greatest word is greater than the second one in size, return it
  Example:

  :param words:
  :return:
  """
  if len(words) == 0:
    # list is empty, there is no longest
    return None
  elif len(words) == 1:
    # list has only one element, this is its longest
    return words[0]
  list2d = []
  for word in words:
    length = len(word)
    pair = (word, length)
    list2d.append(pair)
  sorted(list2d, key=lambda k: k[1])
  # test the first 2, but notice the sort above is ascending, so look up its tail
  first = list2d[-1][1]
  second = list2d[-2][1]
  if first == second:
    # there is no unique longest (ie, there are more than one), return None
    return None
  longest = list2d[-1][0]
  return longest



class Rename:
  """
  This class aims to rename files in the following tactic, ie:

  1) names from files with 'from_ext' become a list for matching with files with 'to_ext'
  2) if files with 'to_ext' match the starting string in names (ie, name without extension)
     and no collsion occurs (ie no other file has the same starting name)
     these files will pair, one by one, with the 'from_ext' files
  Example:

    Suppose the two 'from_ext' files on local folder:
      file abc this first one.pdf
      file def this second one.pdf

    Suppose the two 'to_ext' files on local folder:
      file abc blah.epub
      file def foo bar.epub

    This script will end up matching the following pairs:
      (file abc this first one.pdf, file abc blah.epub)
      (file def this second one.pdf, file def foo bar.epub)

    The rename result will be:
      (file abc blah.epub, file abc this first one.epub)
      (file def foo bar.epub, file def this second one.epub)

  How the algorithm works:
    Notice in pair:
      (file abc this first one.pdf, file abc blah.epub)
    the longest coincind string in target is "file abc "
    then the script checks up if another files also has the prefix "file abc "
    if no other one exists -- the case in this example --, a rename pair can be formed, ie
      (file abc this first one.pdf, file abc blah.epub)
  """

  def __init__(self, from_ext, to_ext):
    """

    """
    self.from_ext = from_ext
    self.to_ext = to_ext
    self.confirm_before_rename = args.confirm_before_rename
    # self.abspath = os.path.dirname(os.path.abspath(__file__))
    self.abspath = os.getcwd()
    self.rename_pairs = []
    self.process_renames()

  def process_renames(self):
    """

    :param self:
    :return:
    """
    self.find_fromfiles()
    self.match_tofiles_if_any()
    self.form_rename_pair_based_on_tofiles()
    self.show_renames()
    if self.confirm_before_rename:
      do_rename = self.confirm_renames()
    else:
      do_rename = True
    if do_rename:
      self.do_rename_pairs()

  def find_from_files(self):
    """

    :return:
    """
    param_for_glob = '*.' + self.dot_from_extension
    from_filenames = glob.glob(param_for_glob)
    sorted(from_filenames)
    for filename in from_filenames:
      name, dot_ext = os.path.splitext(filename)
      if ext is None or ext == '':
        continue
      words = filename.split(' ')
      if len(words) < 2:
        continue
      fileabspath = os.path.join(self.abspath, filename)
      duration_str = get_duration_str(fileabspath)  # probe_n_return_json
      # if (duration_str) exists in source filename, do not buffer it to rename_pairs tuple list
      if duration_str == words[1]:
        continue
      new_name = words[0] + ' ' + duration_str + " " + ' '.join(words[1:])
      rename_tuple = (filename, new_name)
      self.rename_pairs.append(rename_tuple)

  def match_tofiles_if_any(self):
    self.match_pairs = []
    prefixes = []
    for from_filename in self.from_filenames:
      for to_filename in to_filenames:
        prefix = get_the_longest_equal_prefixing_string(from_filename, to_filename)
        if len(prefix) > 0:
          prefixes.append(prefix)
      unique = verify_prefix_unicity(prefixes)
      if unique is None:
        continue
      self.match_pairs = (from_filename, prefix)

  def show_renames(self):
    """

    :return:
    """
    for i, rename_pair in enumerate(self.rename_pairs):
      filename, new_name = rename_pair
      print(i+1, ' ======== Rename Pair ========')
      print('FROM: >>>' + filename)
      print('TO:   >>>' + new_name)
    if len(self.rename_pairs) == 0:
      print(''' *** No files are renameable. ***
        ==>>> Either:
        1) no files with renaming extension (%s) in folder;
        2) namesizes are too short or
        3) files already have the duration mark.      
      ''' % self.extension)

  def confirm_renames(self):
    """

    :return:
    """
    n_renames = len(self.rename_pairs)
    if n_renames > 0:
      msg_for_input = 'Are you sure to  rename these (%d) files? (Y/n) ' % n_renames
      ans = input(msg_for_input)
      if ans in ['n', 'N']:
        return False
    return True

  def do_rename_pairs(self):
    """

    :return:
    """
    n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      filename, newname = rename_pair
      if os.path.isfile(filename) and not os.path.isfile(newname):
        os.rename(filename, newname)
        n_renames += 1
    print('Total files renamed: %d' % n_renames)


def adhoc_test():
  s1 = 'this string up to here foo bar'
  s2 = 'this string blah blah'
  longest = get_the_longest_equal_prefixing_string(s1, s2)
  print('s1 => [' + s1 + ']')
  print('s2 => [' + s2 + ']')
  print('longest => [' + longest + ']')
  words = ['blah foo', 'blah f', 'blah']
  print('words', words)
  longest = verify_longest_word_unicity(words)
  print('longest', longest)


def get_args():
  from_ext, to_ext = None, None
  for arg in sys.argv:
    if arg.startswith('-h'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-f='):
      from_ext = arg[len('-f=')]
    elif arg.startswith('-f='):
      to_ext = arg[len('-f=')]
  return from_ext, to_ext


def process():
  from_ext, to_ext = get_args()
  Rename(from_ext, to_ext)


if __name__ == '__main__':
  """
  process()
  """
  adhoc_test()
