#!/usr/bin/env python3
"""
renameReplaceWordsToDigitNumbersUpTo99.py
This script transforms a phrase written number, limited to 99, to its digit-form.

Examples:
  'Twenty Seven Metallic Glass.26p.pdf' becomes '27 Metallic Glass.26p.pdf'
  'Three Properties of Silicon Crystals.21p.pdf' becomes '3 Properties of Silicon Crystals.21p.pdf'

At this version, it works for separated words such "Twenty Seven", not with "Twenty-Seven" separated with a dash (-)
  TO-DO: (for a next version) allow dashed separated phrase numbers such as Twenty-Seven or thirty-nine

Usage:
$ renameReplaceWordsToDigitNumbersUpTo99.py [-p=<basefolder_absdir>] [-e=<extension>] [-y|Y]

Where the all three optional parameters are:
  1) -p=<basefolder_absdir> is the directory where the renaming will take place (default is the local folder)
  2) [-e=<extension>] is the file extension where renaming will happen (e.g. "pdf", also the default one)
  3) -y or -Y means "yes" autoren_no_cli_confirm ie no CLI confirmation will be asked for renaming (default is "no")

Example:
$ renameReplaceWordsToDigitNumbersUpTo99.py -p="/home/datafiles/book1" -e=txt -y
"""
import os
import sys
first_nineteen = [
  'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
  'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
]
dozens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninty']


def get_number_from_phrase_upto99(phrase):
  """
  This function works limited to a phrase written number up to 99.
  Also composed number must be separated by a space (gap), example: twenty seven (instead of twenty-seven)
  :param phrase:
  :return:
  """
  try:
    pp = phrase.split(' ')
  except ValueError:
    return None, phrase
  if len(pp) < 2:
    return None, phrase
  left_word = pp[0].lower()
  if left_word in first_nineteen:
    unit_number = first_nineteen.index(left_word)  # returns unit number as a digit (0, 1, 2, 3..., 9)
    newphase = str(unit_number) + ' ' + ' '.join(pp[1:])
    return unit_number, newphase
  # dozen_number = 0
  if left_word in dozens:
    dozen_number = dozens.index(left_word) * 10
  else:
    return None, phrase
  right_word = pp[1].lower()
  unit_number = 0
  if right_word in first_nineteen:
    unit_number = first_nineteen.index(right_word)
  twodigitnumber = dozen_number + unit_number
  if unit_number == 0:
    remainder = ' '.join(pp[1:])  # notice twenty (thirty etc) is not written twenty zero ie the second word is not used
  else:
    remainder = ' '.join(pp[2:])
  newphrase = str(twodigitnumber) + ' ' + remainder
  return twodigitnumber, newphrase


class WordsToDigitsReplaceRenamer:
  DEFAULT_DOTEXTENSION = '.pdf'

  def __init__(self, p_basefolder_absdir=None, p_extension=None, p_autoren_no_cli_confirm=False):
    self.seq = 0
    self.total_pdfs_in_folder = 0
    self.filenames = []  # this attribute is to be deleted after use
    self.renamepairs = []
    self.total_renames = 0
    self.dotextension = p_extension
    self.autoren_no_cli_confirm = p_autoren_no_cli_confirm
    self.basefolder_absdir = p_basefolder_absdir
    self.treat_dotextension()
    self.treat_basefolder_absdir()

  def treat_dotextension(self):
    if self.dotextension is None:
      self.dotextension = self.DEFAULT_DOTEXTENSION
      return
    self.dotextension = str(self.dotextension)
    self.dotextension.lstrip('.')  # in case there are more than one dot (eg '....pdf')
    self.dotextension = '. ' + self.dotextension  # restablish the starting dot '.'

  def treat_basefolder_absdir(self):
    try:
      if os.path.isdir(self.basefolder_absdir):
        # it's okay, return
        return
      else:
        # folder does not exist and exception has not been raised, set it to local 'running' folder and return
        self.basefolder_absdir = os.path.abspath('.')
        return
    except (TypeError, ValueError):
      # exception has been raised, set it to local 'running' folder (return happens in following)
      self.basefolder_absdir = os.path.abspath('.')

  def select_files_in_folder(self):
    filenames = os.listdir(self.basefolder_absdir)
    filenames = list(filter(lambda f: f.endswith(self.dotextension), filenames))
    files = [os.path.join(self.basefolder_absdir, fn) for fn in filenames]
    files = list(filter(lambda f: os.path.isfile(f), files))
    sorted(files)
    self.filenames = [os.path.split(f)[1] for f in files]

  def process_n_form_renamepairs(self):
    for filename in self.filenames:
      _, newfilename = get_number_from_phrase_upto99(filename)
      if newfilename == filename:
        continue
      renamepair = (filename, newfilename)
      self.renamepairs.append(renamepair)
    # self.filenames is no longer necessary from here, for translated files, if any, were stored in self.renamepairs
    del self.filenames

  def show_pairs(self):
    """

    :return:
    """
    for i, renamepair in enumerate(self.renamepairs):
      seq = i + 1
      print('-'*30)
      old_filename, new_filename = renamepair
      print(seq, '/', len(self.renamepairs), 'To Confirm-Rename:')
      print('\t [', old_filename, ']')
      print('\t [', new_filename, ']')
    print('In folder:', self.basefolder_absdir)

  def confirm_renames(self):
    if len(self.renamepairs) == 0:
      print('No files found to rename.')
      print('-'*30)
      return
    print('There are %d renamable files in the target folder.' % len(self.renamepairs))
    print('-'*30)
    self.show_pairs()
    if self.autoren_no_cli_confirm:
      return True
    screen_msg = 'Confirm the %d renames above ? (*Y/n) [y, Y or empty-ENTER means yes] ' % len(self.renamepairs)
    ans = input(screen_msg)
    if ans in ['Y', 'y', '']:
      return True
    return False

  def rename_pairs(self):
    for i, renamepair in enumerate(self.renamepairs):
      seq = i + 1
      old_filename, new_filename = renamepair
      oldfile = os.path.join(self.basefolder_absdir, old_filename)
      newfile = os.path.join(self.basefolder_absdir, new_filename)
      if not os.path.isfile(oldfile):
        print('missing file', oldfile, ':: looping to next.')
        continue
      if os.path.isfile(newfile):
        print('same name file', newfile, ':: looping to next.')
        continue
      print(seq, '/', len(self.renamepairs), 'Renaming:')
      print(seq, old_filename)
      print(seq, new_filename)
      os.rename(oldfile, newfile)
      self.total_renames += 1
    print('Total renamed =', self.total_renames)

  def process(self):
    self.select_files_in_folder()
    self.process_n_form_renamepairs()
    if self.confirm_renames():
      self.rename_pairs()


def adhoc_test():
  t = 'Twenty Seven Metallic Glass.26p'
  ans = get_number_from_phrase_upto99(t)
  print('prase', t)
  print('result', ans)
  t = 'Three Properties of Silicon Crystals.21p'
  ans = get_number_from_phrase_upto99(t)
  print('prase', t)
  print('result', ans)


def get_args():
  p_basefolder_absdir = None
  p_extension = None
  p_autoren_no_cli_confirm = False
  for arg in sys.argv:
    if arg.startswith('-p='):
      p_basefolder_absdir = arg[len('-p='):]
    elif arg.startswith('-e='):
      p_extension = arg[len('-e='):]
    elif arg in ['-y', '-Y']:
      p_autoren_no_cli_confirm = True
  return p_basefolder_absdir, p_extension, p_autoren_no_cli_confirm


if __name__ == '__main__':
  """
  adhoc_test()
  """
  basefolder_absdir, extension, autoren_no_cli_confirm = get_args()
  renamer = WordsToDigitsReplaceRenamer(basefolder_absdir, extension, autoren_no_cli_confirm)
  renamer.process()
