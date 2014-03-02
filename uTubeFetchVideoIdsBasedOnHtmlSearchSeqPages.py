#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script forms file youtube-ids.txt which is input for a second script that reuses youtube-dl and download the youtube videos by their id's, one at a time
'''
import glob, os #, sys

# input tuple
#sys.path.insert(0, '.')
#import uTubeFormIdsInputFileBasedOnHtmlSearchSeqPages_tuple_input_data as input_data
#filename_with_increment_interpolation, n_total_pages = input_data.filename_with_increment_interpolation, input_data.n_total_pages

def find_youtube_sequenced_htmls():
  youtube_search_files = []
  htmls = glob.glob('*.html') + glob.glob('*.htm')
  for html in htmls:
    pos = html.find(' - YouTube ')
    if pos > -1:
      name, ext = os.path.splitext(html)
      remaining = name[ pos + len(' - YouTube ') : ]
      try:
        int(remaining)
      except ValueError:
        continue
      youtube_search_files.append(html)
  youtube_search_files.sort()
  return youtube_search_files      

def cleanup_line_beginning_blanks(text):
  lines = text.split('\n')
  newtext = ''
  for line in lines:
    newline = line.lstrip(' \t')
    newtext += newline + '\n'
  return newtext

def delete_sequential_txt_files(n_of_seq_txt_files):
  '''
  These files are SAFE to delete because they were created with the ">" Unix-redirection artifice
  ie, delete those files created with "> %(seq)d.txt" 
    after the "grep" for the "watch" string inside the YouTube videoid links
  '''
  for seq in xrange(1, n_of_seq_txt_files+1):
    comm = 'rm %(seq)d.txt' %{'seq':seq}
    print comm
    os.system(comm)

txtfilename_interpolaton = '%(seq)d.txt'
commbase = 'weblinksExtractor.py "%(youtube_search_file)s" | grep watch > %(txtfilename)s'
def process():
  youtube_search_files = find_youtube_sequenced_htmls()
  n_of_seq_txt_files = len(youtube_search_files)
  if n_of_seq_txt_files == 0:
    print '''No processing occurred.  The following messages are informative:
    + There are no youtube_search_files on this folder (they should end with " - YouTube <n>.htm[l]" where <n> is a number).
    + Please look into the directory listing to verify there is at least one of them. (In case there are any of them, please report a bug in this program.'''
    return
  for i, youtube_search_file in enumerate(youtube_search_files):
    seq = i + 1
    txtfilename = txtfilename_interpolaton %{'seq':seq}
    if os.path.isfile(txtfilename):
      print '''Processing  cannot continue.  The following messages are informative:
      + There is a file on this folder that would be overwritten if processing continued. (This file is named "%s").
      + Please, delete it or move it outside this folder and then rerun this program.''' %txtfilename
      return
    comm = commbase %{'youtube_search_file':youtube_search_file, 'txtfilename':txtfilename}
    print comm
    os.system(comm)
  comm = 'cat ?.txt > youtube-ids.txt'
  os.system(comm)
  delete_sequential_txt_files(n_of_seq_txt_files)  # ie, delete those files created with "> %(seq)d.txt" after the grep above

  text = open('youtube-ids.txt').read()
  text = text.replace('/watch?v=','')
  text = cleanup_line_beginning_blanks(text)
  f_output = open('youtube-ids.txt','w')
  f_output.write(text)
  f_output.close()


if __name__ == '__main__':
  process()
