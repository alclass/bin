#!/usr/bin/env python3
"""
Example:
  Original name:
  05 10' w1_L2 07_Week_12.6_General_Stability_Criteria_and_Implicit_Schemes_10-10.mp4.mp4

  To rename as:
  05-1-2-7 10' General Stability Criteria and Implicit Schemes.mp4
"""
import glob
import re
import os


FILE_EXTENSION = 'mp4'
DOT_FILE_EXTENSION = '.mp4'


def fetch_files_on_folder(ext):
  files = glob.glob('*.' + ext)
  print('Fetched', len(files), 'files')
  return files


def trunk_string_from_number_dash_number(remainder):
  """

  :param remainder:
  :return:
  """
  pattern_number_dash_number = r".*(\d{1,2}\-\d{1,2}).*"  # -\-()
  res = re.match(pattern_number_dash_number, remainder)
  if res is None:
    return remainder
  poss = res.span(1)  # throw_away_number
  firstpos = poss[0]
  trunked_remainder = remainder[:firstpos]
  return trunked_remainder


def transform_rename(ori_filename=None):
  """
  name = "05 10' w1_L2 07_Week_12.6_General ..."
  pattern1 = "(\\d{1,2}) (\\d{1,2})' w(\\d{1})_L(\\d{1,2})\b{1}\\d{1,2}_Week_\\d{1,2}\\.\\d{1}"  # ex ww1_L2

  RE Groups are:
    first_num = int(res.group(1))
    duration = int(res.group(2))
    week_num = int(res.group(3))
    lesson_num = int(res.group(4))
    seq_num = int(res.group(5))

  :return:
  """
  if ori_filename is None:
    return None
  pattern1 = r"^(\d{1,2}) (\d{1,2})' w(\d{1,2})_L(\d{1,2}) (\d{1,2})_Week_\d+.(\d)"
  trg_filename = None
  res = re.match(pattern1, ori_filename)
  if res:
    first_num = int(res.group(1))
    duration = int(res.group(2))
    week_num = int(res.group(3))
    lesson_num = int(res.group(4))
    seq_num = int(res.group(5))
    poss = res.span(6)  # throw_away_number
    lastpos = poss[1]
    newname_template = "%(first_num)02dW%(week_num)02dL%(lesson_num)02dS%(seq_num)02d %(duration)d'"
    trg_filename = newname_template \
        % {
          'first_num': first_num, 'week_num': week_num,
          'lesson_num': lesson_num, 'seq_num': seq_num, 'duration': duration
        }
    remainder = ori_filename[lastpos+1:]
    remainder = trunk_string_from_number_dash_number(remainder)
    remainder = remainder.replace('_', ' ')
    if remainder.endswith('.mp4.mp4'):
      remainder = remainder.replace('.mp4.mp4', '.mp4')
    elif not remainder.endswith('.mp4'):
      remainder = remainder + '.mp4'
    remainder = remainder.replace(' .', '.')
    trg_filename = trg_filename + ' ' + remainder
    # print(trg_filename)
  return trg_filename


class Renamer:

  def __init__(self, noconfirm=False):
    self.rename_pairs = []
    self.noconfirm = noconfirm
    self.files = fetch_files_on_folder(FILE_EXTENSION)

  def prepare_rename(self):
    file_counter = 0
    for eachFile in self.files:
      newname = transform_rename(eachFile)
      if newname is None:
        continue
      pair = (eachFile, newname)
      self.rename_pairs.append(pair)
      file_counter += 1
      print('Listing', file_counter, '===============')
      print('FROM:', eachFile)
      print('TO:  ', newname)

  def confirm_rename(self):
    n_to_rename = len(self.rename_pairs)
    if n_to_rename == 0:
      print('No files to rename.')
      return False
    confirm_question = 'Confirm the above %d renames? (*Y/n) ' % n_to_rename
    ans = input(confirm_question)
    if ans not in ['', 'Y', 'y']:
      print('Not renaming', n_to_rename, 'files,')
      return False
    print('To rename', n_to_rename, 'files => ')
    return True

  def do_rename(self):
    n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      oldname, newname = rename_pair
      if not os.path.isfile(oldname):
        print(seq, 'File [' + oldname + '] does not exist.')
        continue
      if os.path.isfile(newname):
        print(seq, 'File [' + newname + '] already exists.')
        continue
      print('Renaming', seq, '===============')
      print('FROM:', oldname)
      print('TO:  ', newname)
      os.rename(oldname, newname)
      n_renames += 1
    print('n_renames', n_renames)

  def process_rename(self):
    self.prepare_rename()
    if self.noconfirm:
      self.do_rename()
    elif self.confirm_rename():
      self.do_rename()
    else:
      print('No files renamed.')


def process():
  renamer = Renamer()
  renamer.process_rename()


if __name__ == '__main__':
  process()
