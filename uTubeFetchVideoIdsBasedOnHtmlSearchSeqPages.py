#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script has two functionalities:

  1) when used without arguments, it reads an html YouTube page and outputs
    a file named youtube-ids.txt
    Obs: youtube-ids.txt is input for a second script that reuses youtube-dl and
        download the youtube videos by their id's, one at a time.
  Eg. $uTubeFetchVideoIdsBasedOnHtmlSearchSeqPages.py

  2) when used with a sole argument, this argument is
    a filename on the current directory that has, on each line, filenames that
    adhere to the convention of a dash and the 11-char ytid, ending with a dot and extension.
  Eg. $uTubeFetchVideoIdsBasedOnHtmlSearchSeqPages.py z-filenames.txt
  If a non-existing filename is used, the script will fall back to
    the default filename which is [[z-filenames.txt]].

  3) when used with either -h or --help arguments, this script will print out
    this docpage.
'''
import glob, os, sys
import local_settings as bls
sys.path.insert(0, os.path.abspath(bls.UTUBEAPP_PATH))
import uTubeOurApps.shellclients.uTubeFetchVideoIdsBasedOnHtmlSearchSeqPages as ytvidsFetcher
import uTubeOurApps.shellclients.uTubeExtractIdsFromFilenames as ytIdsExtractor

FILENAMES_WITH_YTIDS__DEFAULT_FILENAME = 'z-filenames.txt'
class Arg:

  def __init__(self):
    self.filenames_filename = None
    self.get_args()

  def get_filenames_filename(self):
    if self.filenames_filename is None or self.filenames_filename == '' or type(self.filenames_filename)!=str:
      return FILENAMES_WITH_YTIDS__DEFAULT_FILENAME
    return self.filenames_filename

  def get_filenames_filepath(self):
    folderpath = os.getcwd()
    filepath = os.path.join(folderpath, self.get_filenames_filename())
    return filepath

  # self.filenames_filename = FILENAMES_WITH_YTIDS__DEFAULT_FILENAME

  def verify_n_set_filepath(self):
    '''
      # folderpath = os.path.dirname(os.path.realpath(__file__))
      # folderpath = os.path.dirname(sys.argv[0])

    error_msg = 'self.filenames_filename ("%s") is missing.' % self.filenames_filename
    error_msg += '\n'
    folderpath = os.getcwd()

    :return:
    '''
    filepath = self.get_filenames_filepath()
    if not os.path.isfile(filepath):
      if self.filenames_filename != FILENAMES_WITH_YTIDS__DEFAULT_FILENAME:
        self.filenames_filename = FILENAMES_WITH_YTIDS__DEFAULT_FILENAME
        filepath = self.get_filenames_filepath()
        if not os.path.isfile(filepath):
          error_msg = '''
   The following filepath:
   -----------------------------------------------
   %s
   -----------------------------------------------
   does not exist. (Type -h or --help for printing out the script's docpage.)
''' %filepath
          raise IOError(error_msg)

  def get_args(self):
    for arg in sys.argv[1:]:
      if arg == '-h' or arg == '--help':
        print __doc__
        sys.exit(0)
      elif arg.startswith('-'):
        continue
      else:
        self.filenames_filename = arg
        self.verify_n_set_filepath()

# 1st functionality
def extract_ytids_from_html():
  ytvidsFetcher.process()

# 2nd functionality
def extract_ytids_from_filenames_filename(filenames_filepath):
  ytids = ytIdsExtractor.extract_ytids_from_filenames(filenames_filepath)
  for ytid in ytids:
    print ytid

def process():
  arg_obj = Arg()
  if arg_obj.filenames_filename is None:
    extract_ytids_from_html()
  else:
    filenames_filepath = arg_obj.get_filenames_filepath()
    # print ('filenames_filepath', filenames_filepath)
    extract_ytids_from_filenames_filename(filenames_filepath)

if __name__ == '__main__':
  process()
