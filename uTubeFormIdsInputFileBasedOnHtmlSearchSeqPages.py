#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script forms file youtube-ids.txt which is input for a second script that reuses youtube-dl and download the youtube videos by their id's, one at a time
'''
import os, sys

# input tuple
sys.path.insert(0, '.')
import uTubeFormIdsInputFileBasedOnHtmlSearchSeqPages_tuple_input_data as input_data
filename_with_increment_interpolation, n_total_pages = input_data.filename_with_increment_interpolation, input_data.n_total_pages

commbase = 'weblinksExtractor.py "%(filename_with_increment_interpolation)s"' %{'filename_with_increment_interpolation':filename_with_increment_interpolation} + ' | grep watch > %(seq)d.txt'
def process():
  for seq in range(1, n_total_pages + 1):
    comm = commbase %{'seq':seq}
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

