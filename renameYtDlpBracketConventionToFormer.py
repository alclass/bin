#!/usr/bin/env python3
"""
renameYtDlpBracketConventionToFormer.py

This script aims to rename filenames (in folder or in a text file) under the yt-dlp naming convention
  to the yt-dl's older one.
  => Use CLI-parameter -tf for running the renaming inside a text file (defaulted to 'z-names.txt')

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
import sys

ENC64CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'
CHARS_TO_REMOVE_FROM_NAMES = ['：', '？', '?', '!', '|','｜', '＂', '.', '⧸']  # ⧸ is not / [⧸/]


def remove_exclchars_n_doublesps(word):
  for c in CHARS_TO_REMOVE_FROM_NAMES:
    word = word.replace(c, '')
  while word.find('  ') > -1:
    word = word.replace('  ', ' ')
  return word


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
	fn as input must be a
	  name-ending-with-bracket-ytid-bracket
	ie a name where:
	  1) name[-14] is a left-brack ('[')
	  2) name[-13:-2] is an ENC64 11-char string
	  3) name[-1] is a right-brack (']')
	function extract_ytid_from_filename_on_ytdlp_convention_or_none(fn)
	  checks/guards it (fn)
  :return:
    new_fn is the converted filename
  """
  # the extracting may have been done before, but it's repeated here as precaution
  ytid = extract_ytid_from_filename_on_ytdlp_convention_or_none(fn)
  if ytid is None:
    return None
  name, dotext = os.path.splitext(fn)
  dotext = dotext.rstrip(' \t\r\n')
  new_fn = name[: -13]
  new_fn = new_fn.rstrip(' \t\r\n')
  new_fn = remove_exclchars_n_doublesps(new_fn)
  new_fn = new_fn + '-' + ytid + dotext
  return new_fn


class RenamerInTextFile:

  def __init__(self, textfilename=None):
    self.newtext = ''
    if textfilename is None:
      self.textfilename = 'z-names.txt'
    else:
      self.textfilename = textfilename
    if not os.path.isfile(self.textfilename):
      print('File', self.textfilename, 'does not exist. Please, reenter it.')
      sys.exit(1)
    self.current_text = open(self.textfilename).read()
    self.process()

  def process_textfile(self):
    self.newtext = ''
    lines = self.current_text.split('\n')
    for line in lines:
      fn = line.rstrip(' \t\r\n')
      ytid = extract_ytid_from_filename_on_ytdlp_convention_or_none(fn)
      if ytid is None:
        continue
      new_fn = generate_newfilename(fn)
      self.newtext += new_fn + '\n'
    self.newtext = self.newtext.rstrip(' \t\r\n')

  def confirm_filewrite(self):
    if len(self.newtext) == 0:
      print('New file is empty, not writing it.')
      return False
    text = self.newtext
    text = text.lstrip(' ').rstrip(' \t\r\n')
    if len(text) == 0:
      print('New file is empty, not writing it.')
      return False
    print('File to be save in folder:')
    print('-'*40)
    print(self.newtext)
    print('='*40)
    ans = input('Confirm file [%s] writing ? (y/N) [ENTER] means Yes ' % self.textfilename)
    if ans.lower() in ['y', '']:
      return True
    print('No writing on file ' + self.textfilename)
    return False

  def process(self):
    self.process_textfile()
    if self.confirm_filewrite():
      fd = open(self.textfilename, 'w')
      fd.write(self.newtext)
      fd.close()
      print('Script wrote file', self.textfilename)
    print(' === process end ===')


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


def if_cli_help_show_n_exit():
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)


def is_it_in_a_textfile():
  for arg in sys.argv:
    if arg.startswith('-tf'):
      return True
  return False


def process():
  """

  :return:
  """
  if_cli_help_show_n_exit()
  if not is_it_in_a_textfile():
    Renamer()
  else:
    RenamerInTextFile()


if __name__ == '__main__':
  # adoc_test()
  process()


def adoc_test():
  """
  Reg Exp approach was changed for a simpler char-index-look-up one
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
