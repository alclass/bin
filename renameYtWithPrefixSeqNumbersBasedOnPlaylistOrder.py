#!/usr/bin/env python3
#-*-coding:utf-8-*-
'''
This script renames YouTube videos prefixing them with the 2-digit number
  that is the same as its ordered position in playlist.

For this script to work, there must exist a file in folder named youtube-ids
(or the given by parameter -n="<filename>").

Let's see an example:

if a file is named:
     "file-foobar-XLJN4JfniH4.mp4"
 and if XLJN4JfniH4 occupies the 3rd line in file youtube-ids.txt
 (or the one under -n), the new filename will be:
     "3 file-foobar-XLJN4JfniH4.mp4" (zfill left-zero-padding takes place if necessary)

Created on 03/jul/2018

@author: friend
'''
import glob, os, sys
from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename

charSize = lambda idword: len(idword) == 11 # this lambda is intended to be used in a 'filter', each element is filtered-in if lambda returns True for it (filterOutNon11Char will used this later below)
wordStrip = lambda idword : idword.strip()
def extract_ids(ytids_filename):
  text = open(ytids_filename).read()
  if text is not None:
    ids = text.split('\n')
    stripMap = map(wordStrip, ids)
    ids = [i for i in stripMap]
    filterOutNon11Char = filter(charSize, ids) # only 11-char idwords are allowed, '', '\n' etc. are filtered out
    ids = [i for i in filterOutNon11Char]
    return ids
  return [] # if it has not returned above, text is None

DEFAULT_YTPL_ORDER_TXT_IDS_FILE = 'youtube-ids.txt'
DEFAULT_EXTENSION = 'mp4'
class Arg:
  '''
  Class to find arguments from command line
  '''

  def __init__(self):
    '''

    '''
    self.extension             = DEFAULT_EXTENSION
    self.ytids_filename        = DEFAULT_YTPL_ORDER_TXT_IDS_FILE
    self.confirm_before_rename = True
    self.process_cli_args()

  def print_explanation_and_exit(self):
    print( __doc__ )
    sys.exit(0)

  def process_cli_args(self):
    '''

    :return:
    '''
    for arg in sys.argv:
      if arg in ['-h', '--help']:
        self.print_explanation_and_exit()
      if arg.startswith('-y'):
        self.confirm_before_rename = False
      if arg.startswith('-e='):
          self.extension = arg[ len('-e=') : ]
      if arg.startswith('-n='):
          self.ytids_filename = arg[ len('-n=') : ]


class Rename:

  def __init__(self, arg):
    '''

    :param arg:
    '''
    self.arg = arg
    self.extension      = None
    self.ytids_filename = None
    self.confirm_before_rename = None
    self.ytids = []
    self.rename_pairs = []
    self.processRename()

  def processRename(self):
    '''

    :return:
    '''
    self.transfer_args()
    self.fetch_ytids_from_idsfile()
    self.findRenames()
    self.showRenames()
    bool_confirm = False
    if self.confirm_before_rename:
      bool_confirm = self.confirmRenames()
    if not self.confirm_before_rename:
      bool_confirm = True
    if bool_confirm:
      self.doRenames()

  def transfer_args(self):
    '''

    :return:
    '''
    self.extension = self.arg.dotextension
    if self.extension is None or self.extension == '':
      error_msg = 'extension argument is missing.'
      raise ValueError(error_msg)
    self.ytids_filename = self.arg.ytids_filename
    if self.ytids_filename is None or not os.path.isfile(self.ytids_filename):
      error_msg = 'youtube ids filename (%s) argument is missing.' %self.ytids_filename
      raise ValueError(error_msg)
    self.confirm_before_rename = self.arg.confirm_before_rename
    if self.confirm_before_rename is None:
      self.confirm_before_rename = False
    # delete self.arg
    del(self.arg)

  def fetch_ytids_from_idsfile(self):
    '''

    :return:
    '''
    self.ytids = extract_ids(self.ytids_filename)

  def findRenames(self):
    '''

    :return:
    '''
    filenames = glob.glob('*.' + self.extension)
    # sorted( filenames )
    usedfilenames = []
    n_to_align_left_zeroes = len(str(len(self.ytids))) # another option is to encapsulate a function that uses math.log10()
    for filename in filenames:
      videoid = get_videoid_from_filename(filename)
      if not videoid in self.ytids:
        print('videoid', videoid)
        print('File', filename, 'not found having an equivalent in ids. Skipping to next one if any...')
        continue
      try:
        index = self.ytids.index(videoid)
      except ValueError:
        print('yt-videoid', videoid, 'not found. Skipping next...')
        # this is logically not possible due to previous 'if' (a re-raise is a TODO here)
        raise ValueError
      seqnumber = index + 1
      newName = str(seqnumber).zfill(n_to_align_left_zeroes) + ' ' + filename
      if filename not in usedfilenames:
        rename_tuple = (filename, newName)
        self.rename_pairs.append(rename_tuple)
        usedfilenames.append(filename)

  def showRenames(self):
    '''

    :return:
    '''
    def take_2nd_elem(elem):
      return elem[1]
    sorted( self.rename_pairs, key=take_2nd_elem )
    for i, renameTuple in enumerate(self.rename_pairs):
      seqNumber = i + 1
      currentName, newName = renameTuple
      print('Rename n.', seqNumber)
      print(' => ', currentName)
      print(' => ', newName)

  def confirmRenames(self):
    '''

    :return:
    '''
    if len(self.rename_pairs) > 0:
      msg_for_input = 'Confirm renames above with %d files and %d ids? (Y*/n) ' %(len(self.rename_pairs), len(self.ytids))
      ans = input(msg_for_input)
      if ans.startswith('y') or ans.startswith('Y') or ans == '':
        return True
    return False

  def doRenames(self):
    '''

    :return:
    '''

    nOfRenames = 0
    for i, renameTuple in enumerate(self.rename_pairs):
      oldFilename, newFilename = renameTuple
      if not os.path.isfile(oldFilename):
        continue
      os.rename(oldFilename, newFilename)
      nOfRenames += 1

    print('Total of renames = %d' %nOfRenames)


def process():
  '''

  :return:
  '''
  arg = Arg()
  Rename(arg)

if __name__ == '__main__':
  process()
