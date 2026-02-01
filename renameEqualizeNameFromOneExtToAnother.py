#!/usr/bin/env python3
"""
renameEqualizeNameFromOneExtToAnother.py

This script does the following:

suppose one has two files in a directory, say:

 => "History of Ancient Greece vol 1 great book.300pages.pdf"
 => "History of Ancient Greece 1 gb.epub"

Now consider that these two files contain the same book and one wants to rename
  the epub one just as its pdf counterpart is named, ie:

rename:
    from: "History of Ancient Greece 1 gb.epub"
      to: "History of Ancient Greece vol 1 great book.300pages.epub"

This script can do that with the following command line:

prompt$ <this_script> -f=pdf -t=epub
where arguments are:
-f : the from-file_extension
-t : the to-file_extension

Example for the above case:
prompt$ renameEqualizeNameFromOneExtToAnother.py -f=pdf -t=epub

Notice that the case-example supposed the existence of only two files. In fact, the script
  will look up all from-files -- ie all files having the from-extension --, and all to-files.

If any files are to be renamed, a user-confirmation will be asked in the terminal prompt.
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
    # print('c =>', c)
    if len(tolist) == 0:
      break
    if c == tolist[-1]:
      result_prefix += tolist.pop()
    else:
      break
  return result_prefix


def verify_longest_wordsize_unicity(words):
  """
  This function returns either the longest word in a list of words
    or None if there are more than one longest or if the input list is empty or None

  Important: unicity here is not for the string itself, it's for its size
    example: 'abc' and 'def' both have 3 characters; they are not unique in size

  Here is how this function works:
    1) the function here sorts the list on charsize
    2) if the greatest word has a second one with the same size, return None
    3) if the greatest word is greater than the second one in size, return it

  Example 1: there is a longest:
    words ['blah f', 'blah foo', 'blah']
    before sort [('blah f', 6), ('blah foo', 8), ('blah', 4)]
    after sort [('blah', 4), ('blah f', 6), ('blah foo', 8)]
    longest 'blah foo' (longest is unique in list)

  Example 1: there are two longest:
    words ['blah f', 'blah foo', 'blah', 'blah foo']
    before sort [('blah f', 6), ('blah foo', 8), ('blah', 4), ('blah foo', 8)]
    after sort [('blah', 4), ('blah f', 6), ('blah foo', 8), ('blah fo2', 8)]
    longest None (notice longest is not unique in list)

  :param words: list of strings
  :return: longest | None
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
  # print('before sort', list2d)
  list2d = sorted(list2d, key=lambda k: k[1])
  # print('after sort', list2d)
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
    self.dot_from_ext = from_ext
    self.dot_to_ext = to_ext
    self.treat_dot_extensions()
    self.from_filenames = []
    self.candidate_to_filenames = []
    # self.abspath = os.path.dirname(os.path.abspath(__file__))
    self.match_pairs = []
    self.rename_pairs = []
    self.rename_confirmed = None
    self.process_renames()

  def treat_dot_extensions(self):
    try:
      if not self.dot_from_ext.startswith('.'):
        self.dot_from_ext = '.' + self.dot_from_ext
      if not self.dot_to_ext.startswith('.'):
        self.dot_to_ext = '.' + self.dot_to_ext
    except (AttributeError, ValueError):
      errmsg = ("Error: Extension either from or to or both are not valid => from=%s to=%s"
                %(str(self.dot_from_ext), str(self.dot_to_ext)))
      print(errmsg)
      print('Exiting.')
      sys.exit(1)
      # raise ValueError(errmsg)

  def find_fromfiles(self):
    """

    :return:
    """
    param_for_glob = '*' + self.dot_from_ext
    self.from_filenames = glob.glob(param_for_glob)
    self.from_filenames.sort()
    print('found', len(self.from_filenames), 'from_filenames')

  def find_candidate_tofiles(self):
    param_for_glob = '*' + self.dot_to_ext
    self.candidate_to_filenames = glob.glob(param_for_glob)
    self.candidate_to_filenames.sort()
    print('found', len(self.candidate_to_filenames), 'candidate_to_filenames')

  def match_tofiles_if_any(self):
    self.match_pairs = []
    for from_filename in self.from_filenames:
      prefixes_n_tofilenames = []
      for candidate_to_filename in self.candidate_to_filenames:
        prefix = get_the_longest_equal_prefixing_string(from_filename, candidate_to_filename)
        if len(prefix) > 0:
          prefix_n_tofilename = (prefix, candidate_to_filename)
          prefixes_n_tofilenames.append(prefix_n_tofilename)
      if len(prefixes_n_tofilenames) == 0:
        continue
      elif len(prefixes_n_tofilenames) == 1:
        candidate_to_filename = prefixes_n_tofilenames[0][1]
        match_pair = (from_filename, candidate_to_filename)
        self.match_pairs.append(match_pair)
        continue
      else:
        prefixes = [pair[0] for pair in prefixes_n_tofilenames]
        unique = verify_longest_wordsize_unicity(prefixes)
        if unique is None:
          continue
        candidate_tuple = filter(lambda pair: pair[0] == unique, prefixes_n_tofilenames)
        candidate_tuple_first = list(candidate_tuple)[0]
        candidate_to_filename = candidate_tuple_first[1]
        if not isinstance(candidate_to_filename, str):
          errmsg = 'candidate_to_filename %s is not str' % str(candidate_to_filename)
          raise ValueError(errmsg)
        match_pair = (from_filename, candidate_to_filename)
        self.match_pairs.append(match_pair)
        continue
    print('matched', len(self.match_pairs), 'match_pairs')

  def show_match_pairs(self):
    print('@show_match_pairs')
    for match_pair in self.match_pairs:
      print(match_pair)

  def find_trgfilename_by_candidate_prefix(self, candidate_prefix):
    for to_filename in self.candidate_to_filenames:
      if to_filename.startswith(candidate_prefix):
        return to_filename
    return None

  def adjust_trgfilename_based_on_srcfilename(self):
    """
    Notice that the source filename, at this point, is not actually the one to be renamed,
      the one to be renamed, up to this point in the algorithm, is the target filename.
    So an adjustment is needed.
    Ie, the target filename, at this point, will become the source filename,
      no transformation needed.
    The new target filename is based on the former source filename, swapping extensions,
      a transform is needed.

    Example: Suppose the incoming pair:
      src = file 1 great history.epub
      trg = file 1 blah.pdf

    In the example, the adjustment (the outgoing pair) should be:
      src = file 1 blah.pdf
      trg = file 1 great history.pdf

    :return:
    """
    for match_pair in self.match_pairs:
      print('match_pair', match_pair)
      src_filename_at_this_point = match_pair[0]
      srcname_at_this_point, _ = os.path.splitext(src_filename_at_this_point)
      src_filename = match_pair[1]  # trg_becoming_src
      _, trg_dot_ext = os.path.splitext(src_filename)  # the target at this point carries the source extension
      trgname = srcname_at_this_point  # swap source name to target name, not its extension
      trg_filename = trgname + trg_dot_ext  # target filename has the original target extension
      rename_pair = (src_filename, trg_filename)
      self.rename_pairs.append(rename_pair)

  def show_rename_pairs(self):
    print('@show_rename_pairs')
    for i, rename_pair in enumerate(self.rename_pairs):
      src_filename = rename_pair[0]
      trg_filename = rename_pair[1]
      seq = i + 1
      print(seq)
      print('from: ', src_filename)
      print('  to: ', trg_filename)

  def confirm_renames(self):
    """

    :return:
    """
    n_to_rename = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      filename, new_name = rename_pair
      if not os.path.isfile(filename):
        continue
      if os.path.isfile(new_name):
        continue
      n_to_rename += 1
      print(n_to_rename, i+1, ' ======== Rename Pair ========')
      print('FROM: >>>' + filename)
      print('TO:   >>>' + new_name)
    if len(self.rename_pairs) == 0:
      print(''' *** No files are renameable. ***
        ==>>> Either:
        1) no files with renaming extension (%s) in folder;
        2) namesizes are too short or
        3) files already have the duration mark.      
      ''' % self.extension)
    n_renames = len(self.rename_pairs)
    if n_renames > 0:
      msg_for_input = 'Are you sure to  rename these (%d) files? (Y/n) [ENTER] means Yes ' % n_renames
      ans = input(msg_for_input)
      self.rename_confirmed = False
      if ans in ['Y', 'y', '']:
        self.rename_confirmed = True
    return

  def do_renames(self):
    """

    :return:
    """
    if len(self.rename_pairs) == 0:
      print('No filename pairs to rename.')
      return
    if not self.rename_confirmed:
      print('rename not confirmed, returning.')
      return
    n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      src_filename, trg_filename = rename_pair
      if not os.path.isfile(src_filename):
        print('src_filename', src_filename, 'does not exist, not renaming, continuing.')
        continue
      if os.path.isfile(trg_filename):
        print('trg_filename', trg_filename, 'does exist, mot renaming, continuing.')
        continue
      seq = i + 1
      print(seq, 'Renaming:')
      print('from: ', src_filename)
      print('  to: ', trg_filename)
      os.rename(src_filename, trg_filename)
      n_renames += 1
      print(n_renames, 'Renamed.')
    print('Total files renamed: %d' % n_renames)

  def process_renames(self):
    """

    self.form_rename_pair_based_on_tofiles()
    self.show_renames()
    if self.confirm_before_rename:
      do_rename_if_confirmed = self.confirm_renames()
    else:
      do_rename_if_confirmed = True
    if do_rename_if_confirmed:
      self.do_rename_pairs()

    :param self:
    :return:
    """
    self.find_fromfiles()
    self.find_candidate_tofiles()
    self.match_tofiles_if_any()
    # self.show_match_pairs()
    self.adjust_trgfilename_based_on_srcfilename()
    self.confirm_renames()
    self.do_renames()



def adhoc_test():
  s1 = 'this string up to here foo bar'
  s2 = 'this string blah blah'
  longest = get_the_longest_equal_prefixing_string(s1, s2)
  print('s1 => [' + s1 + ']')
  print('s2 => [' + s2 + ']')
  print('longest => [' + longest + ']')
  words = ['blah f', 'blah foo', 'blah', 'blah fo2']
  print('words', words)
  longest = verify_longest_wordsize_unicity(words)
  print('longest', longest)


def get_args():
  from_ext, to_ext = None, None
  for arg in sys.argv:
    if arg.startswith('-h'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-f='):
      from_ext = arg[len('-f='):]
    elif arg.startswith('-t='):
      to_ext = arg[len('-t='):]
  return from_ext, to_ext


def process():
  from_ext, to_ext = get_args()
  Rename(from_ext, to_ext)


if __name__ == '__main__':
  """
  adhoc_test()
  """
  process()
