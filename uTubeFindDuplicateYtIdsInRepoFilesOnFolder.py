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
  supposed_ytid = name[-11:]
  ytid = return_encode64_or_none(supposed_ytid)
  return ytid


class RepoFilesReader:

  def __init__(self):
    self.repeat_counter = 0
    self.ytid_dict = {}
    self.ytids = []
    self.repeat_ytids = []

  @staticmethod
  def find_repofiles_on_folder():
    files = os.listdir('.')
    repofiles = filter(lambda n: n.startswith(FILEPREFIX), files)
    return repofiles

  def find_repeat_ytids_in_file(self, repofile):
    print('reading', repofile)
    repofd = open(repofile)
    line = repofd.readline()
    while line:
      # print(line)
      ytid = find_ytid_in_line(line)
      if ytid is not None:
        if ytid in self.ytids:
          if 'z Extra/' in line:
            pass
          else:
            self.repeat_counter += 1
            self.repeat_ytids.append(ytid)
            # print(line)
        else:
          self.ytids.append(ytid)
      line = repofd.readline()

  def process(self):
    repofiles = self.find_repofiles_on_folder()
    for repofile in repofiles:
      self.find_repeat_ytids_in_file(repofile)
    print('number of unique ytids =>', len(self.ytids))
    for ytid in self.repeat_ytids:
      print('repeat ytid', ytid)
    print('repeat_counter =>', self.repeat_counter)


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

  def test7_find_a_ytid_in_a_line(self):
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
