#!/usr/bin/env python3
"""
renameYtDlpBracketConventionToFormer.py

This script aims to rename filenames under the yt-dlp naming convention to the yt-dl's older one.
This yt-dlp convention is the following:
 => filename[ytid].ext
    ie, the 11-char ENC64 ytid is enclosed within brackets ('[' & ']') at end before the dot-extension

Thus, the renaming changes the convention above to yt-dl's former one, ie:
 => filename-ytid.ext

Example: file "abc [ytid].ext" is renamed to "abc-ytid.ext" where ytid is an 11-char ENC64 string
"""
import glob
import os
import string
ENC64CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'


def is_str_an_enc64(word):
  bool_list = map(lambda c: c in ENC64CHARS, word)
  if False in bool_list:
    return False
  return True


def extract_ytid_from_filename_on_ytdlp_convention_or_none(filename):
  try:
    name, _ = os.path.splitext(filename)
  except TypeError:
    return None
  if len(name) < 11+2+1:
    return None
  if name[-1] != ']':
    return None
  if name[-13] != '[':
    return None
  supposed_ytid = name[-12: -1]
  boolres = is_str_an_enc64(supposed_ytid)
  if boolres:
    ytid = supposed_ytid
    return ytid
  return None


def generate_newfilename(fn):
  """

  :param fn:
  :return:
  """
  # the extracting may have been done before, but it's repeated here as precaution
  ytid = extract_ytid_from_filename_on_ytdlp_convention_or_none(fn)
  if ytid is None:
    return None
  name, dotext = os.path.splitext(fn)
  new_fn = name[: -13]
  new_fn = new_fn.rstrip(' \t\r\n')
  new_fn = new_fn + '-' + ytid + dotext
  new_fn = new_fn.replace('：', '')
  new_fn = new_fn.replace('?', '')
  new_fn = new_fn.replace('!', '')
  new_fn = new_fn.replace('|', '')
  return new_fn


class Renamer:
  
  def __init__(self):
    self.rename_pairs = []
    self.renamed_n = 0
    self.process()

  def fetch_folder_files(self):
    filenames = glob.glob('*')
    for fn in filenames:
      ytid = extract_ytid_from_filename_on_ytdlp_convention_or_none(fn)
      if ytid is None:
        continue
      new_fn = generate_newfilename(fn)
      if os.path.isfile(new_fn):
        continue
      rename_tuple = (fn, new_fn)
      self.rename_pairs.append(rename_tuple)

  def confirm_renames(self):
    if len(self.rename_pairs) == 0:
      print('No files to rename.')
      return False
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      old_name, new_name = rename_pair
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
    ans = input('Confirm the %d renames above ? (y/N) [ENTER] means Yes ' % len(self.rename_pairs))
    if ans.lower() in ['y', '']:
      return True
    print('No renames were done.')
    return False
    
  def do_renames(self):
    self.renamed_n = 0
    print('-'*40)
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      old_name, new_name = rename_pair
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
      if os.path.isfile(new_name):
        continue
      if not os.path.isfile(old_name):
        continue
      os.rename(old_name, new_name)
      self.renamed_n += 1
    print('-'*40)
    print('Total to be renamed = %d' % len(self.rename_pairs))
    print('Total renamed = %d' % self.renamed_n)

  def process(self):
    self.fetch_folder_files()
    if self.confirm_renames():
      self.do_renames()


def test_re():
  """
    res = recomp.match(t1)
  if res:
    print(res.group(1))
  print(res)

  :return:
  """
  t1 = 'balasddkhgkghkgkjglfa [eRh1SwlPwdc].ext'
  ytid_or_none = extract_ytid_from_filename_on_ytdlp_convention_or_none(t1)
  print('test 1', t1, ytid_or_none)
  t2 = "2023-02-16 5' Reinaldo： É legal divulgar cartão de vacinação de Bolsonaro, além de ético [IjYUmUwDt98].webm"
  ytid_or_none = extract_ytid_from_filename_on_ytdlp_convention_or_none(t2)
  print('test 2', t2, ytid_or_none)
  new_t2 = generate_newfilename(t2)
  print('test 2', t2, ytid_or_none)
  print('new_t2', new_t2)
  t3 = "blash ddvvn op434j34389 ~~´´ sasdf"
  ytid_or_none = extract_ytid_from_filename_on_ytdlp_convention_or_none(t3)
  print('test 3', t3, ytid_or_none)
  t4 = 'balasddkhgkghkgkjglfa [eRh1SçlPwdc].ext'
  ytid_or_none = extract_ytid_from_filename_on_ytdlp_convention_or_none(t4)
  new_t4 = generate_newfilename(t4)
  print('test 4', t4, ytid_or_none)
  print('new_t4', new_t4)
  word = 'eRh1SçlPwdc'
  ans = is_str_an_enc64(word)
  print(word, ans)


def process():
  """

  :return:
  """
  Renamer()


if __name__ == '__main__':
  # test_re()
  process()
