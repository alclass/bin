#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation

This script ...
'''
import glob, os, sys

prompt_for_confirm = True

def get_mp3filename_based_on_foldername():
  '''

  :return:
  '''
  wholepath = os.path.abspath('.')
  wholepath.rstrip('/.')
  foldername_applied_to_mp3 = wholepath.split('/')[-1] + '.mp3'
  return foldername_applied_to_mp3

def mount_mp3s_concat_str():
  '''

  :return:
  '''
  mp3s = glob.glob('*.mp3')
  if len(mp3s) == 0:
    return None
  mp3s.sort()
  mp3s_concat_str = 'concat:'
  for mp3 in mp3s:
    mp3s_concat_str += "%s|" %mp3
  mp3s_concat_str = mp3s_concat_str.rstrip('|')
  return mp3s_concat_str

def execute_os_comm(foldername_applied_to_mp3, mp3s_concat_str):
  '''

  :param foldername_applied_to_mp3:
  :param mp3s_concat_str:
  :return:
  '''
  comm = '''ffmpeg -i "%(mp3s_concat_str)s" -acodec copy "%(foldername_applied_to_mp3)s" ''' \
    %{ \
      'mp3s_concat_str':mp3s_concat_str, \
      'foldername_applied_to_mp3':foldername_applied_to_mp3, \
    }
  print comm
  if prompt_for_confirm:
    ans = raw_input('Confirm the mp3-joint ? (Y/n) ')
    if ans in ['N','n']:
      return
  os.system(comm)

def join_the_mp3s_creating_mp3name_based_on_foldername():
  '''

  :return:
  '''
  foldername_applied_to_mp3 = get_mp3filename_based_on_foldername()
  if os.path.isfile(foldername_applied_to_mp3):
    print 'Mp3 %s already exists. Continuing or returning.' %foldername_applied_to_mp3
    return
  mp3s_concat_str = mount_mp3s_concat_str()
  if mp3s_concat_str == None:
    print 'No mp3 files in this folder. Continuing or returning.'
    return
  execute_os_comm(foldername_applied_to_mp3, mp3s_concat_str)


def inspect_args_to_check_for_later_prompt_confirm():
  global prompt_for_confirm
  for arg in sys.argv:
    if arg == '-Y':
      prompt_for_confirm = False

def process():
  inspect_args_to_check_for_later_prompt_confirm()
  join_the_mp3s_creating_mp3name_based_on_foldername()

if __name__ == '__main__':
  process()
