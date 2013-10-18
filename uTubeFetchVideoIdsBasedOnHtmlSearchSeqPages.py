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

commbase = 'weblinksExtractor.py "%(youtube_search_file)s" | grep watch > %(seq)d.txt'
def process():
  youtube_search_files = find_youtube_sequenced_htmls(); seq = 0
  for youtube_search_file in youtube_search_files:
    seq += 1
    comm = commbase %{'youtube_search_file': youtube_search_file, 'seq':seq}
    print comm
    os.system(comm)
  comm = 'cat ?.txt > youtube-ids.txt'  
  os.system(comm)

  text = open('youtube-ids.txt').read()
  text = text.replace('/watch?v=','')
  f_output = open('youtube-ids.txt','w')
  f_output.write(text)
  f_output.close()


if __name__ == '__main__':
  process()
