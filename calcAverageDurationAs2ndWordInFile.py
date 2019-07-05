#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob, sys

DEFAULT_EXTENSION = 'mp4'

def calcAverageDurationAs2ndWordInFile(files):
  '''

  '''
  total_duration = 0
  for eachFile in files:
    try:
      word = eachFile.split()[1]
      if word.find('h') > -1:
        hours, minutes = word.split('h')
        introunded_individual_duration = int(hours)*60 + int(minutes)
      else:
        word = word.strip(" ',;-\r")
        introunded_individual_duration = int(word)
      print(introunded_individual_duration, eachFile)
    except(ValueError, IndexError) as error:
      continue
    total_duration += introunded_individual_duration 
  average = total_duration / len(files)
  average = round(average)
  return average

def show_cli_help():
  print('''
    This scripts calculates the average duration in minutes from
    files that have names based on the following conventions:
    1) the duration is put as a second word in the filename;
    2) the duration is:
      2a) either <minutes>' (ie number of minutes [from 0 to 59] followed by ' (plics) 
          example: 31' (meaning 31 minutes integer rounded)
      2b) or number of hours followed by an "h" followed by number of minutes [from 0 to 59]
          example: 2h17 (meaning 2 hours and 17 minutes, minutes integer rounded)
    
    Argument required:
    The argument required is -e=<extension>
          -e=mp4 (ie, take the average duration for mp4 files,
                  all those in which name convention holds) 
  ''')

def get_extension_from_args():
  ext = None
  for arg in sys.argv:
    if arg in ['-h', '--help']:
      return show_cli_help()
    elif arg.startswith('-e='):
      ext = arg[len('-e=') : ]
  return ext

def get_files_from_args():
  '''

  '''
  ext = get_extension_from_args()
  if ext is None:
    ext = DEFAULT_EXTENSION
  files = glob.glob("*." + ext)
  return files

def process():
  '''

  '''
  files = get_files_from_args()
  print('Calculation duration average calculation with %d files.' %len(files))
  if len(files) > 0:
    average = calcAverageDurationAs2ndWordInFile(files)
    print('Duration average is', average)
  else:
    print('Please use the -e=<extension> to pick up a file extension to be used for the duration average calculation.')
  
if __name__ == '__main__':
  process()
