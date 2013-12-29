#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, logging, os, sys, time
'''
Explanation: 
  This is a simple script that wraps up youtube-dl with the following 2 extra functionalities:
  1) it sets --playlist-start to the number of local folder mp4 files minus 1
     (minus 1 because the last one may be incomplete, though the id's change due to new submitted videos and some videos may end up incomplete)
  2) if youtube-dl breaks out, generally this happens when the connection breaks, 
     it pauses for 2 minutes and loops back up again rerunning youtube-dl
'''

logging.basicConfig(filename='youtubedl-reissue-os.system.log',level=logging.INFO)

def print_and_log(line_msg):
  print line_msg 
  logging.info(line_msg)

def get_start_n():
  mp4s = glob.glob('*.mp4')
  start_n = len(mp4s) - 1 
  return start_n   

#start_n = int(sys.argv[1])
BASE_COMMAND = 'youtube-dl -w -f 18 --playlist-start %(start_n)d http://www.youtube.com/user/provafinal/'
TWO_MIN_IN_SECS = 120

def continue_youtubedl_until_retval_is_zero():
  retVal = -1; loop_seq = 0
  while retVal <> 0:
    loop_seq += 1
    start_n = get_start_n()
    line_msg = '%s Downloading with start_n = %d' %(time.ctime(), start_n); print_and_log(line_msg) 
    comm = BASE_COMMAND %{'start_n':start_n}
    line_msg = 'seq = %d :: %s' %(loop_seq, comm); print_and_log(line_msg) 
    retVal = os.system(comm)
    line_msg = 'retVal = %d' %(retVal); print_and_log(line_msg) 
    if retVal <> 0:
      print 'Pausing for 2 minutes until next issuing of youtube-dl.'
      time.sleep(TWO_MIN_IN_SECS)

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

if __name__ == '__main__':
  continue_youtubedl_until_retval_is_zero()
