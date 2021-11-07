#!/usr/bin/env python3
"""
uTubeFindDuplicateIds.py
This script reads the conventioned-named youtube-ids repository.
Inside this textfile, this script looks for duplicate youtube-ids and, if found, prints them out.
"""
import math
import os
import random
import string
import sys
import time
import unittest

FILEPREFIX = 'z_ls-R_contents-'
ENCODE64CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_' + '-'
ACCEPTABLE_EXTENSIONS = ['.mp3', '.mp4', 'webm']


def add_to_countingdict(pkey, pdict):
  if pkey in pdict:
    count = pdict[pkey]
    pdict[pkey] = count + 1
  else:
    pdict[pkey] = 2  # because it's caught from the 2nd occorence onwards


def add_to_strlistdict(pkey, strtolist, pdict):
  if pkey in pdict:
    strlist = pdict[pkey]
    strlist.append(strtolist)
  else:
    pdict[pkey] = [strtolist]


def find_a_possible_ytid_from_name(name):
  try:
    supposed_ytid_with_dash = name[-12:]
    if supposed_ytid_with_dash[0] != '-':
      return None
    supposed_ytid = supposed_ytid_with_dash[1:]
    return return_encode64_or_none(supposed_ytid)
  except IndexError:
    pass
  return None


def return_encode64_or_none(supposed_ytid):
  if supposed_ytid is None:
    # hypothesis 1 -> paramvalue is None itself
    return None
  try:
    if len(supposed_ytid) != 11:
      # hypothesis 2 -> paramvalue has size different than 11 characters
      return None
  except TypeError:
    # hypothesis 3 -> paramvalue is not a string-castable type
    return None
  bool_list = map(lambda c: c in ENCODE64CHARS, supposed_ytid)
  if False in bool_list:
    # hypothesis 4 -> paramvalue has one or more non-ENCODE64 characters
    return None
  # hypothesis 5 -> there should be at least a lowercase char
  bool_list = map(lambda c: c in string.ascii_lowercase, supposed_ytid)
  if True not in bool_list:
    return None
  # hypothesis 6 -> there should be at least an uppercase char
  bool_list = map(lambda c: c in string.ascii_uppercase, supposed_ytid)
  if True not in bool_list:
    return None
  return supposed_ytid


def mount_a_random_ytid():
  random_ytid = ''
  for n in range(11):
    index = random.randint(0, 63)
    random_chr = ENCODE64CHARS[index]
    random_ytid += random_chr
  return random_ytid


def is_extension_acceptable(ext):
  if ext not in ACCEPTABLE_EXTENSIONS:
    return False
  return True


def find_ytid_in_line(line):
  line = line.lstrip(' \t').rstrip(' \t\r\n')
  name, ext = os.path.splitext(line)
  if not is_extension_acceptable(ext):
    return None
  if len(name) < 12:
    return None
  ytid = find_a_possible_ytid_from_name(name)
  return ytid


class RepoFilesReader:
  """
  Because of possible memory large use, the ytid's will be looked up throughout TWO pass, ie:
  1) the 1st pass is just to filter out the ytid's that repeat.
  2) the 2nd pass will tabulate them ordered by ytid's themselves (instead of order of appearance)
  """

  def __init__(self):
    self.REPEATS_OUTPUT_FILENAME = 'z-results-ytid-repeats.txt'
    self.ytids_repeat_dict = {}
    self.ytids_paths_dict = {}
    self.ytids_found = []
    self.outfile = None

  @staticmethod
  def find_repofiles_on_folder():
    files = os.listdir('.')
    repofiles = filter(lambda n: n.startswith(FILEPREFIX), files)
    return repofiles

  def write_to_repeat_ytid_file(self, ytid, filename, previouspath):
    if self.outfile is None:
      outfilename = 'z-results-ytid-repeats.txt'
      self.outfile = open(outfilename, 'w', encoding='utf8')
    filepath = os.path.join(previouspath, filename)
    outline = ytid + ' | ' + filepath + '\n'
    self.n_repeat_ytids += 1
    self.outfile.write(outline)

  def save_resultsfile_with_ytids_n_paths(self):
    outfile = open(self.REPEATS_OUTPUT_FILENAME, 'w', encoding='utf8')
    print('Writing to file', self.REPEATS_OUTPUT_FILENAME)
    n_lines = 0
    for ytid in self.ytids_paths_dict:
      strlist = self.ytids_paths_dict[ytid]
      for path in strlist:
        outline = path
        outline = outline.rstrip(' \t\r\n') + '\n'  # only one \n should go with line
        n_lines += 1
        outfile.write(outline)
    print('Closing file', self.REPEATS_OUTPUT_FILENAME, 'with', n_lines)
    outfile.close()

  def treat_ytid_in_the_2nd_pass(self, ytid, lineasfilename, previouspath):
    if ytid not in self.ytids_repeat_dict:
      return
    lineasfilename = lineasfilename.lstrip(' \t').lstrip(' \t\r\n')
    filepath = os.path.join(previouspath, lineasfilename)
    add_to_strlistdict(ytid, filepath, self.ytids_paths_dict)

  def run_2nd_pass(self, repofile):
    print('Reading 2nd pass', repofile)
    repofd = open(repofile)
    line = repofd.readline()
    previouspath = None
    while line:
      if line.startswith('./'):
        previouspath = line.rstrip(' \t\r\n')
        previouspath = previouspath.rstrip(':')
      elif len(line) < 17:  # 11 (ytid) + 1 (dash) + 5|4 (.webm | .mp4) + 2|1 (short filename) = 19|17
        pass
      else:
        ytid = self.extract_ytid_from_line_as_filename(line)
        self.treat_ytid_in_the_2nd_pass(ytid, line, previouspath)
      # reads next line and loop
      line = repofd.readline()
    repofd.close()

  @staticmethod
  def extract_ytid_from_line_as_filename(line):
    filename = line.lstrip(' \t').rstrip(' \t\r\n')
    name, ext = os.path.splitext(filename)
    if ext not in ACCEPTABLE_EXTENSIONS:
      return None
    try:
      ytid = find_a_possible_ytid_from_name(name)
      return ytid
    except IndexError:
      pass
    return None

  def print_histogram_ytid_repeats(self):
    for ytid in self.ytids_repeat_dict:
      print(ytid, ' | ', self.ytids_repeat_dict[ytid])
    print('Total:', len(self.ytids_repeat_dict))

  def treat_ytid_in_the_1st_pass(self, ytid):
    if ytid is None:
      return
    if ytid not in self.ytids_found:
      self.ytids_found.append(ytid)
    else:
      add_to_countingdict(ytid, self.ytids_repeat_dict)
      # self.write_to_repeat_ytid_file(ytid, filename, previouspath)

  def run_1st_pass(self, repofile):
    """
    The 1st pass discovers ytid's that repeat and, later in the 2nd pass, writes them with its paths in order
    Details for deleting a large list at the end of the 1st run:
      1) list self.ytids_found helps organize the self.ytids_repeat_dict in the first run
      2) at the end of the 1st run, this list may be safely deleted to save some memory
         (the garbage collector run is not guaranteed)

    :return:
    """
    print('Reading 1st pass', repofile)
    repofd = open(repofile)
    line = repofd.readline()
    while line:
      if line.startswith('./'):
        pass
      elif len(line) < 17:  # 11 (ytid) + 1 (dash) + 5|4 (.webm | .mp4) + 2|1 (short filename) = 19|17
        pass
      else:
        ytid = self.extract_ytid_from_line_as_filename(line)
        self.treat_ytid_in_the_1st_pass(ytid)
      # reads next line and loop
      line = repofd.readline()
    # the ytids_found is a large list, deleting it will help save some memory
    del self.ytids_found
    repofd.close()

  def process_repofile(self, repofile):
    self.run_1st_pass(repofile)
    # self.print_histogram_ytid_repeats()
    self.run_2nd_pass(repofile)
    self.save_resultsfile_with_ytids_n_paths()

  def process(self):
    repofiles = self.find_repofiles_on_folder()
    for repofile in repofiles:
      self.process_repofile(repofile)


def adhoc_test1():
  known_ytid = 'Ço-jk4kVtE8'
  returned_ytid = return_encode64_or_none(known_ytid)
  print('known_ytid', known_ytid, 'returned_ytid', returned_ytid)
  print(ENCODE64CHARS)
  bool_list = map(lambda c: c in ENCODE64CHARS, known_ytid)
  print(list(bool_list))


def process():
  """
  adhoc_test1()

  :return:
  """
  reporeader = RepoFilesReader()
  reporeader.process()


if __name__ == '__main__':
  process()


class YtIdsTest(unittest.TestCase):

  def test1_the64chars(self):
    # ENCODE64CHARS has to have 64 chars
    self.assertEqual(64, len(ENCODE64CHARS))
    # mounting another ENCODE64CHARS string
    the64chars = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_' + '-'
    self.assertEqual(64, len(the64chars))
    expect_true_bool_list = []
    for c in the64chars:
      expect_true_bool_list.append(c in ENCODE64CHARS)
    list64trues = [True]*64
    # each char in the mounted 64CHARS must get a True when compared to the original ENCODE64CHARS
    self.assertEqual(list64trues, expect_true_bool_list)

  def test2_invalid_sample_ytids(self):
    # hypothesis 1 -> invalid by being none itself
    invalid_ytid = None
    returned_ytid = return_encode64_or_none(invalid_ytid)
    self.assertIsNone(returned_ytid)
    # hypothesis 2 -> invalid by having size different than 11 characters
    invalid_ytid = 'Zo-jk4kVtE8' + 'anything'
    returned_ytid = return_encode64_or_none(invalid_ytid)
    self.assertIsNone(returned_ytid)
    # hypothesis 3 -> invalid by having a non-ENCODING64 character
    invalid_ytid = 'ço-jk4kVtE8'
    returned_ytid = return_encode64_or_none(invalid_ytid)
    self.assertIsNone(returned_ytid)
    # hypothesis 4 -> invalid by not having a string-like (castable) type

    def get_hidden_numtype():  # this is to deceive the IDE into thinking it sent a non-string
      mixtypeslist = ['str', 'str', 12, 'str', 'str']
      return mixtypeslist[math.floor(len(mixtypeslist)/2)]  # ie get the middle element (which is an int there)
    returned_ytid = return_encode64_or_none(get_hidden_numtype())
    self.assertIsNone(returned_ytid)
    # hypothesis 5 -> missing a lowercase char
    invalid_ytid = '1'*10 + 'A'
    returned_ytid = return_encode64_or_none(invalid_ytid)
    self.assertIsNone(returned_ytid)
    # hypothesis 6 -> missing an uppercase char
    invalid_ytid = '1'*10 + 'a'
    returned_ytid = return_encode64_or_none(invalid_ytid)
    self.assertIsNone(returned_ytid)

  def test3_sample_ytids(self):
    known_ytid = 'Zo-jk4kVtE8'
    self.assertEqual(11, len(known_ytid))
    returned_ytid = return_encode64_or_none(known_ytid)
    self.assertEqual(known_ytid, returned_ytid)
    known_ytid = 'omvx0ID1TGo'
    self.assertEqual(11, len(known_ytid))
    returned_ytid = return_encode64_or_none(known_ytid)
    self.assertEqual(known_ytid, returned_ytid)

  def test4_simple_ytids(self):
    # simple ones though not easily foundable (perhaps some are filtered out by the full YouTube algorithm)
    valid_enc64 = '1'*9 + 'Aa'
    returned_ytid = return_encode64_or_none(valid_enc64)
    self.assertEqual(valid_enc64, returned_ytid)
    valid_enc64 = '-_'*4 + 'Aa1'
    returned_ytid = return_encode64_or_none(valid_enc64)
    self.assertEqual(valid_enc64, returned_ytid)

  def test5_randomly_formed_ytids(self):
    random_ytid = mount_a_random_ytid()
    returned_ytid = return_encode64_or_none(random_ytid)
    # a randomly_formed_ytid should be a valid ytid
    self.assertEqual(random_ytid, returned_ytid)
    random_ytid2 = mount_a_random_ytid()
    # a second randomly_formed_ytid should in theory be different than the one previously generated
    self.assertNotEqual(random_ytid, random_ytid2)
    returned_ytid = return_encode64_or_none(random_ytid2)
    # the second randomly_formed_ytid should be a validl ytid
    self.assertEqual(random_ytid2, returned_ytid)

  def test6_find_a_ytid_in_a_line(self):
    line = "    2020-11-18 21' Exploring The Human-Ape Paradox \
    - Iain Davidson - Art, Story, Mind-nDrtXuw0ubQ.mp4          "
    should_found_ytid = 'nDrtXuw0ubQ'
    extracted_ytid_from_line = find_ytid_in_line(line)
    self.assertEqual(extracted_ytid_from_line, should_found_ytid)
    returned_ytid = return_encode64_or_none(extracted_ytid_from_line)
    self.assertEqual(extracted_ytid_from_line, returned_ytid)

  def test7_find_a_ytid_in_a_line_2ndway(self):
    name = "2020-11-18 21' Exploring The Human-Ape Paradox \
    - Iain Davidson - Art, Story, Mind-nDrtXuw0ubQ"
    should_found_ytid = 'nDrtXuw0ubQ'
    extracted_ytid_from_name = find_a_possible_ytid_from_name(name)
    self.assertEqual(extracted_ytid_from_name, should_found_ytid)
    # the 2nd test here changes the '-' before ytid to an equal sign (=) - case in which ytid returns as None
    name = "2020-11-18 21' Exploring The Human-Ape Paradox \
    - Iain Davidson - Art, Story, Mind=nDrtXuw0ubQ"  # notice the missing '-' (changed to '=' here)_
    # should_found_ytid = 'nDrtXuw0ubQ'
    extracted_ytid_from_name = find_a_possible_ytid_from_name(name)
    self.assertIsNone(extracted_ytid_from_name)

  def test8_find_a_ytid_in_a_line(self):
    line = "    2020-11-18 21' Exploring The Human-Ape Paradox \
    - Iain Davidson - Art, Story, Mind-nDrtXuw0ubQ.mp4          "
    line = line.lstrip(' \t').rstrip(' \t\r\n')
    name, ext = os.path.splitext(line)
    returned_bool = is_extension_acceptable(ext)
    # mp4 is an acceptable extension
    self.assertTrue(returned_bool)
    expected_name = "2020-11-18 21' Exploring The Human-Ape Paradox \
    - Iain Davidson - Art, Story, Mind-nDrtXuw0ubQ"
    # two operations are expected: 1) the leftstrip()/rightstrip() one and 2) the os.path.splitext()
    self.assertEqual(expected_name, name)
    filename = 'blah.txt'
    name, ext = os.path.splitext(filename)
    returned_bool = is_extension_acceptable(ext)
    # txt is not an acceptable extension
    self.assertFalse(returned_bool)
    expected_name = 'blah'
    self.assertEqual(expected_name, name)

  def test9_add_to_countingdict(self):
    pdict = {}
    pkey = 'anykey'
    add_to_countingdict(pkey, pdict)
    self.assertEqual(pdict, {'anykey': 2})
    add_to_countingdict(pkey, pdict)
    self.assertEqual(pdict, {'anykey': 3})
    pkey = '2ndkey'
    add_to_countingdict(pkey, pdict)
    self.assertEqual(pdict, {'anykey': 3, '2ndkey': 2})

  def test10_add_to_strlistdict(self):
    pdict = {}
    pkey = 'anykey'
    ppath = '/path/to/file1'
    expected_list = [ppath]
    add_to_strlistdict(pkey, ppath, pdict)
    expected_dict = {'anykey': expected_list}
    self.assertEqual(pdict, expected_dict)
    ppath = '/path/to/file2'
    expected_list.append(ppath)
    add_to_strlistdict(pkey, ppath, pdict)
    self.assertEqual(pdict, expected_dict)
