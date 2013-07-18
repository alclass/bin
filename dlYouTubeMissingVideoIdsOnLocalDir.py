#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
dlYouTubeMissingVideoIdsOnLocalDir.py

Explanation: 
  This script reads a .txt file, which has a hardcoded name z-filenames.txt
  that has YouTube filenames as given by youtube-dl
  (this filename is the video title, a '-' (dash), its videoid, then the dot extension)
  It can also read filenames that have starts with '-' (dash) before the videoid, ie,
  filenames that do not have the title part.
  

  Limitations:
  
    A safe rule to check whether an id is a valid videoid or not, that has not been implemented.
    For the time being, videoids have the following checking (in function return_videoid_if_good_or_None(videoid)):
    + it must contain 11 characters;
    + it must not have the following characters: ' ' (blank), '%' nor '.';
    + it must have at least one lowercase letter and one UPPERCASE letter.

'''
import glob, logging, os, sys, time

def print_and_log(line_msg):
  print line_msg 
  logging.info(line_msg)

BASE_COMMAND_INDIVUAL_VIDEO = 'youtube-dl -w -f 18 http://www.youtube.com/watch?v=%(videoid)s'
TWO_MIN_IN_SECS = 2 * 60

def download_individual_video(videoid, p_seq=1, total_to_go=1):
  retVal = -1; loop_seq = 0
  while retVal <> 0:
    loop_seq += 1
    line_msg = '[%s] Downloading with p_seq = %d of %d' %(time.ctime(), p_seq, total_to_go); print_and_log(line_msg) 
    comm = BASE_COMMAND_INDIVUAL_VIDEO %{'videoid':videoid}
    line_msg = 'loop_seq = %d :: %s' %(loop_seq, comm); print_and_log(line_msg) 
    retVal = os.system(comm)
    line_msg = 'retVal = %d' %(retVal); print_and_log(line_msg)
    if loop_seq > 2: # ie, it tries 3 times!
      # give up
      return 
    if retVal <> 0:
      print 'Pausing for 2 minutes until next issuing of youtube-dl.'
      time.sleep(TWO_MIN_IN_SECS)

def get_videoid_from_extless_filename(extlessname):
  try:
    videoid = extlessname[-11:]
    return videoid
  except IndexError:
    pass
  return None

def get_videoid_from_filename(filename):
  try:
    extlessname = '.'.join(filename.split('.')[:-1])
    return get_videoid_from_extless_filename(extlessname)
  except IndexError:
    pass
  return None
  
import string
has_lowercase_lambda = lambda c : c in string.lowercase
has_UPPERCASE_lambda = lambda c : c in string.uppercase

def return_videoid_if_good_or_None(videoid):
  if videoid == None:
    return None
  elif len(videoid) != 11:
    return None
  elif videoid.find(' ') > -1:
    return None
  elif videoid.find('.') > -1:
    return None
  elif videoid.find('%') > -1:
    return None
  boolean_list_result = map(has_lowercase_lambda, videoid)
  if True not in boolean_list_result:
    return None
  boolean_list_result = map(has_UPPERCASE_lambda, videoid)
  if True not in boolean_list_result:
    return None
  return videoid

class VideoIdsOnFile(object):

  def __init__(self, local_filename):
    self.local_filename = local_filename
    self.find_videoids_on_file()

  def find_videoids_on_file(self):
    self.videoids_on_file = []
    lines = open(self.local_filename).readlines()
    for line in lines:
      if line.endswith('\n'):
        line = line.rstrip('\n')
      if line.find('.') < 0:
        continue
      # strip extension and recompose filename without extension
      try:
        videoid = get_videoid_from_filename(line)
        videoid = return_videoid_if_good_or_None(videoid)
        if videoid == None:
          continue
        if videoid not in self.videoids_on_file:
          self.videoids_on_file.append(videoid)
      except IndexError:
        continue

  def get_videoids_on_file(self):
    return self.videoids_on_file

def checkEveryFileHas11CharId():
  mp4s = glob.glob('*.mp4'); seq=0
  for mp4 in mp4s:
    try:
      extlessname = os.path.splitext(mp4)[0]
      prefixedId = extlessname[-12:]
    except IndexError:
      continue
    if prefixedId.startswith('-'): 
      seq += 1
    print seq, prefixedId
  # mp4's total 
  nOfMp4s = len(mp4s)
  print 'nOfMp4s', nOfMp4s

class VideoIdsComparer(object):

  def __init__(self, local_filename = 'z-filenames.txt'):
    self.local_filename = local_filename
    self.store_all_videoids_on_local_dir()

  def store_all_videoids_on_local_dir(self):
    self.all_videoids = []
    mp4s = glob.glob('*.mp4')
    for mp4 in mp4s:
      try:
        #extlessname = os.path.splitext(mp4)[0]
        #youtubeid = get_videoid(extlessname)
        youtubeid = get_videoid_from_filename(mp4)
        self.all_videoids.append(youtubeid)
      except IndexError:
        continue

  def get_all_mp4_videoids_on_local_dir(self):
    return self.all_videoids

  def compareLocalIdsWithFileDB(self):
    self.missing_videoids = []; n_missing = 0
    videoidsObj = VideoIdsOnFile(self.local_filename)
    for videoid in videoidsObj.get_videoids_on_file():
      if videoid not in self.all_videoids:
        n_missing += 1
        # print n_missing, 'VideoId', videoid, 'in file not on local dir.'
        self.missing_videoids.append(videoid)

  def download_missing_videos(self):
    self.compareLocalIdsWithFileDB()
    print 'Do you want to download the videos below ?'
    print self.missing_videoids
    print 'Total:', len(self.missing_videoids)
    ans = raw_input('(Y/n) ? ')
    if ans in ['n', 'N']:
      return
    total_to_go = len(self.missing_videoids)
    for i, missing_videoid in enumerate(self.missing_videoids):
      p_seq = i + 1 
      download_individual_video(missing_videoid, p_seq, total_to_go)

def download_missing_videoids():
  video_comparer = VideoIdsComparer(local_filename = 'z-filenames.txt')
  video_comparer.download_missing_videos()

def process():
  if len(sys.argv) < 2: # ie, sys.argv[0] contains the script's name and no parameter is present
    download_missing_videoids()
  elif sys.argv[1] == '--checkids':
    checkEveryFileHas11CharId()
  
if __name__ == '__main__':
  process()
