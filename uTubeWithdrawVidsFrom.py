#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
This script does 2 things:

1) if only the base videoids file is given, this file will clean repeats, ie, it will setify, so to say, the videoids so they come out unique each one
2) if a withdraw videoids file is given, the videoids in it will be taken out from the base videoids file

Only ONE assumption here:
1) the 11-char videoids are placed at the beginning of each line (if they are not, this script will not work properly)

Usage:

1)
  script basefilevideoids.txt takeout_videoids.txt > result_takeout_videoids_-_if_any_-_are_not_in_here.txt

2)
  script basefilevideoids.txt > result_filtered_out_repeats_if_any.txt

'''
import sys
#import os, sys, time

# import __init__
# import  bin_local_settings as bls
# sys.path.insert(0, bls.UTUBEAPP_PATH)

from shellclients import extractVideoidsFromATextFileMod as extract_script

def get_vids_from_file(videoids_filename):
  videoids = []
  lines = open(videoids_filename, 'r').readlines()
  for line in lines:
    line = line.lstrip(' \t').rstrip(' \t\r\n')
    if len(line) < 11:
      continue
    line = line[:11]
    if line.find(' ') > -1:
      continue
    # act like a "set", ie, don't append repeats
    if line not in videoids:
      videoids.append(line)
  # the non-repeat feature is done above, line below is not used due to 1) need to maintain the ordering; 2) probable performance worsening, but not measured,
  # videoids = list(set(videoids))
  return videoids

def extract_diff_videoids_between_2_lists(base_videoids, takeout_videoids):
  '''
  Return the diff result

  3) filter the basefile videoid list against the takeout videoid list

  '''
  result_videoids = []
  for videoid in base_videoids:
    if videoid not in takeout_videoids:
      result_videoids.append(videoid)
  return result_videoids

def get_processed_videoids(videoids_filename, withdraw_videoids_filename=None):
  '''
  Organize process chain
  (...)
  2) read files and get videoid lists
  3) filter the basefile videoid list against the takeout videoid list
  (...)
  '''
  base_videoids = get_vids_from_file(videoids_filename)

  if withdraw_videoids_filename == None:
    return base_videoids
  takeout_videoids = get_vids_from_file(withdraw_videoids_filename)
  if len(takeout_videoids) == 0:
    return base_videoids
  result_videoids = extract_diff_videoids_between_2_lists(base_videoids, takeout_videoids)
  return result_videoids

def get_base_and_withdraw_filenames():
  '''
  Organize process chain
  1) pick up filenames
  (...)
  '''
  videoids_filename = sys.argv[1]
  withdraw_videoids_filename = None
  try:
    withdraw_videoids_filename = sys.argv[2]
  except IndexError:
    pass
  return  videoids_filename, withdraw_videoids_filename

def process():
  '''
  Organize process chain
  1) pick up filenames
  2) read files and get videoid lists
  3) filter the basefile videoid list against the takeout videoid list
  4) send result list to standard output (a simple print will do it)
  '''
  videoids_filename, withdraw_videoids_filename = get_base_and_withdraw_filenames()
  result_videoids = get_processed_videoids(videoids_filename, withdraw_videoids_filename)
  for videoid in result_videoids:
    print videoid

if __name__ == '__main__':
  process()
