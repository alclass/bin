#!/usr/bin/env python3
__doc__ = '''
===== Help Screen =====
This script does:

1) collects name-patterned ytids in local files that have the parameterized configured extensions (at this time, hardcoded ones are ['.webm', '.m4a'];

2) reads the ytids 'database' in file [youtube-ids.txt];

3) takes the complement-difference, ie, those that exist in [youtube-ids.txt] but are not present in folder;

4) prints out a shell-script with the youtube-dl commands for the extensions above mentioned;

Obs: this print-out result may be redirected (with the ">" symbol) to a shell-script-file to be manually cleaned up and executed later one.
==================================
'''
import os
import string
import sys

YOUTUBEDL_TXT_FILENAME = 'youtube-ids.txt'
ACCEPTED_EXTENSIONS = ['.webm', '.m4a']
ENCODE64CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-' + '_'
comms_dict = {}
comms_dict['webm'] = 'youtube-dl -w -f 249 https://www.youtube.com/watch?v='
comms_dict['m4a'] = 'youtube-dl -w -f 139 https://www.youtube.com/watch?v='


def verify_encode64(ytid):
  truthies = map(lambda c : c in ENCODE64CHARS, ytid)
  if False in truthies:
    return False
  return True


def get_ytid(filename):
  name, ext = os.path.splitext(filename)
  try:
    ytid = name[-11: ]
    if not verify_encode64(ytid):
      return None
  except IndexError:
    return None
  return ytid


def grab_existing_folders_ytids():
  ytids = []
  entries = os.listdir('.')
  # pick up filenames that have a 'accepted extension'
  entries = filter(lambda e : os.path.splitext(e)[1] in ACCEPTED_EXTENSIONS, entries)
  for entry in entries:
    ytid = get_ytid(entry)
    if ytid is None:
      continue
    ytids.append(ytid)
    # print('ytid', ytid, 'entry', entry)
  return ytids


def grab_txt_dldble_ytids():
  ytids = []
  try:
    text = open(YOUTUBEDL_TXT_FILENAME, 'r').read()
    ytids = text.split('\n')
    ytids = map(lambda i : i.strip(' \t\r\n'), ytids)
    ytids = filter(lambda i : len(i) == 11, ytids)
    ytids = list(ytids)
  except FileNotFoundError:
    return []
  return ytids


def take_difcomplement(dldble_ytids, existing_ytids):
  new_dldble_ytids = []
  for dldble in dldble_ytids:
    if dldble not in existing_ytids:
      new_dldble_ytids.append(dldble)
  return new_dldble_ytids

def printout(dldble_ytids):
  for ext in comms_dict:
    for dldble in dldble_ytids:
      print(comms_dict[ext] + dldble)
    print('='*40)
    

def show_help_if_needed_n_exit():
  for arg in sys.argv:
    if arg == '-h' or arg == '--help':
      print(__doc__)
      sys.exit(0)


def process():
  show_help_if_needed_n_exit()
  existing_ytids = grab_existing_folders_ytids()
  dldble_ytids = grab_txt_dldble_ytids()
  print('ACCEPTED_EXTENSIONS', ACCEPTED_EXTENSIONS)
  print('dldble_ytids', len(dldble_ytids))
  print('existing_ytids', len(existing_ytids))
  print('existing_ytids', existing_ytids)
  print('='*20)
  dldble_ytids = take_difcomplement(dldble_ytids, existing_ytids)
  print('dldble_ytids', len(dldble_ytids))
  print('dldble_ytids', dldble_ytids)
  printout(dldble_ytids)


if __name__ == '__main__':
  process()
