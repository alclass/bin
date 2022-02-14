#!/usr/bin/env python3
import os
import sys
import string
import unittest
"""
Usage:
  uTubeExtractVideoidsFromFile.py <input-filename>

  where <input-filename> is the filename, in the working directory,
  that contains the standardized youtube filenames with a dash 
  followed by the ytid at the end of the name (name before extension).

Example
  uTubeExtractVideoidsFromFile.py names.txt > youtube-ids.txt
Notice the choice of ">", ie the output redirection to another file.  

The rules for checking a ytid at the end of a name are the following:

1) verify that character in position [-12] is a '-' (dash)
   if this fails, name does not carry a valid ytid
2) verify that characters thru position [-11: ] are ENCODING6

The 2 steps above allow some common names to be extracted.
Let's see an example:
-verifying10
012345678901

verifying10 may indeed be a ytid but its probability of being is low.

Because of that an extra STATISTICAL verification is untaken, ie:

3) verify that ytid has at least one lowercase letter and one UPPERCASE.
IMPORTANT: This 3rd rule is an statistical step - it may be changed
           or removed in the future.

# =============== ###
### previous code ###
# =============== ###
#-*-coding:utf-8-*-
import __init__
#import  bin_local_settings as bls
#sys.path.insert(0, bls.UTUBEAPP_PATH)
# from shellclients import extractVideoidsFromATextFileMod as extract_script
"""

ENCODING64CHARS = string.digits + string.ascii_lowercase + \
                  string.ascii_uppercase + '-' + '_'

def check_str_is_encoding64(supposed_ytid):
  bool_result_list = list(map(lambda c: c in ENCODING64CHARS, supposed_ytid))
  if False in bool_result_list:
    return False
  return True


def has_at_least_one_lowercase_letter(supposed_ytid):
  bool_result_list = list(map(lambda c: c in string.ascii_lowercase, supposed_ytid))
  if True in bool_result_list:
    return True
  return False


def has_at_least_one_uppercase_letter(supposed_ytid):
  bool_result_list = list(map(lambda c: c in string.ascii_uppercase, supposed_ytid))
  if True in bool_result_list:
    return True
  return False


def extract_ytid_from_a_filename_line_as_expected(filename):
  """
  if not has_at_least_one_lowercase_letter(supposed_ytid):
    return None
  if not has_at_least_one_uppercase_letter(supposed_ytid):
    return None
  """
  name, ext = os.path.splitext(filename)
  try:
    if name[-12] != '-':
      return None
  except IndexError:
    return None
  supposed_ytid = name[-11: ]
  if not check_str_is_encoding64(supposed_ytid):
    return None
  return supposed_ytid


def extract_ytids_from_input_file():
  filename = sys.argv[1]
  fd = open(filename)
  line = fd.readline()
  while line:
    ytid = extract_ytid_from_a_filename_line_as_expected(line)
    if ytid is None:
      continue
    print (ytid)
    line = fd.readline()


def process():
  extract_ytids_from_input_file()


if __name__ == '__main__':
  process()


class ExtractorTestCase(unittest.TestCase):

  def test1_extract(self):
    """

    :return:
    """
    # a real example
    line = 'Incontro con Piero Benvenuti' \
           ' _ Da Galileo alla cosmologia contemporanea ' \
           'passando per lo spazio-i_yIFkfm4Ww.mp4'
    expected_ytid = 'i_yIFkfm4Ww'
    returned_ytid = extract_ytid_from_a_filename_line_as_expected(line)
    self.assertEqual(expected_ytid, returned_ytid)
    # the same without the pos[-12] "-" (dash caracter)
    line = 'abc=i_yIFkfm4Ww.mp4'
    returned_ytid = extract_ytid_from_a_filename_line_as_expected(line)
    self.assertIsNone(returned_ytid)

  def test1_nonytids(self):
    # negative cases
    # 1) "  Benvenuti" has a space so a None should return
    line = 'Incontro con Piero Benvenuti.mp4'
    returned_ytid = extract_ytid_from_a_filename_line_as_expected(line)
    self.assertIsNone(returned_ytid)
    # 2) missing either a lowercase or an uppercase letter
    line = 'Incontro con Piero -verifying10.mp4'
    returned_ytid = extract_ytid_from_a_filename_line_as_expected(line)
    self.assertIsNone(returned_ytid)
    # 3) missing the '-' (dash) before the ytid
    line = 'Incontro con Piero =i_yIFkfm4Ww.mp4'
    returned_ytid = extract_ytid_from_a_filename_line_as_expected(line)
    self.assertIsNone(returned_ytid)
