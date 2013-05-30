#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation: 
  This script reads a .txt file that have YouTube filenames as given by youtube-dl
  It can also read filenames that have starts with '-' (dash) before the videoid.
  

  Limitations:
    A safe rule to check whether an id is a videoid or not, that has not been implemented.
    For the time being, videoids have to contain 11 characters and not have '%' nor '.'

'''
import glob, logging, os, sys, time


BASE_COMMAND_INDIVUAL_VIDEO = 'youtube-dl -w -f 18 http://www.youtube.com/watch?v=%(videoid)s'

def download_individual_video(videoid, p_seq=1, total_to_go=1):
  retVal = -1; loop_seq = 0
  while retVal <> 0:
    loop_seq += 1
    line_msg = '[%s] Downloading with p_seq = %d of %d' %(time.ctime(), p_seq, total_to_go); print_and_log(line_msg) 
    comm = BASE_COMMAND_INDIVUAL_VIDEO %{'videoid':videoid}
    line_msg = 'loop_seq = %d :: %s' %(loop_seq, comm); print_and_log(line_msg) 
    retVal = os.system(comm)
    line_msg = 'retVal = %d' %(retVal); print_and_log(line_msg)
    if loop_seq > 4:
      # give up
      return 
    if retVal <> 0:
      print 'Pausing for 2 minutes until next issuing of youtube-dl.'
      time.sleep(TWO_MIN_IN_SECS)

def get_videoid(extlessname):
  try:
    videoid = extlessname[-11:]
    return videoid
  except IndexError:
    pass
  return None

def get_videoids_on_file(local_filename):
  videoids_on_file = []
  lines = open(local_filename).readlines()
  for line in lines:
    if line.endswith('\n'):
      line = line.rstrip('\n')
    if line.find('.') < 0:
      continue
    # strip extension and recompose filename without extension
    try:
      extlessname = '.'.join(line.split('.')[:-1])
      videoid = get_videoid(extlessname)
      if videoid == None:
        continue
      elif videoid.find('.') > -1:
        continue
      elif videoid.find('%') > -1:
        continue
      videoids_on_file.append(videoid)
    except IndexError:
      continue
  return videoids_on_file

def checkEveryFileHas11CharId():
  mp4s = glob.glob('*.mp4'); seq=0
  for mp4 in mp4s:
    extlessname = os.path.splitext(mp4)[0]
    prefixedId = extlessname[-12:]
    if prefixedId.startswith('-'): 
      seq += 1
    print seq, prefixedId
  # mp4's total 
  nOfMp4s = len(mp4s)
  print 'nOfMp4s', nOfMp4s

class VideoIdsComparer(object):

  def __init__(self, local_filename):
    self.local_filename = local_filename
    self.store_all_videoids_on_local_dir()

  def store_all_videoids_on_local_dir(self):
    self.all_videoids = []
    mp4s = glob.glob('*.mp4')
    for mp4 in mp4s:
      try:
        extlessname = os.path.splitext(mp4)[0]
        youtubeid = get_videoid(extlessname)
        self.all_videoids.append()
      except IndexError:
        continue

  def compareLocalIdsWithFileDB(self):
    self.missing_videoids = []
    videoids = get_videoids_on_file(self.local_filename); seq = 0
    for videoid in videoids:
      if videoid not in self.all_videoids:
        seq += 1
        # print seq, 'VideoId', videoid, 'in file not on local dir.'
        self.missing_videoids.append(videoid)

  def download_missing_videos(self):
    self.compareLocalIdsWithFileDB()
    print 'Do you want to download the videos below ?'
    print self.missing_videoids
    print 'Total:', len(self.missing_videoids)
    ans = raw_input('(Y/n ? ')
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

