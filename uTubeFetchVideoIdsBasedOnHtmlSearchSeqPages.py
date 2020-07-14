#!/usr/bin/python3
'''
Usage:
<this_script> [-f=<youtube_videos_filename>]

  Parameters:
    -- help => this message
    -f=<filename> => where <filename> is for a videos page
                  if no videos filename is given, default is named 'a - YouTube 01.html',
                  ie, there should be a videos file on current folder with that name.
    Internally, the script is also able to read full OS filepath,
    but in that case it should be called from another program, prepared to join a path a call the entry function here.
'''
import os, sys
import collections as coll

localfolder = False
prefixBegStr = '{"videoId":"'
posfixEndStr = '"'

def uniquesize(alist):
  od = coll.OrderedDict()
  for e in alist:
    od[e]=1
  return list(od.keys())
  
def extract_videoids(text):
  begpos = text.find(prefixBegStr)
  ytvideoids = []
  while begpos > -1:
    forwardpos = begpos + len(prefixBegStr)
    text = text[ forwardpos : ]
    endpos = text.find(posfixEndStr)
    if endpos > -1:
      ytvideoid = text [ : endpos ]
      ytvideoids.append(ytvideoid)
    text = text [ endpos + 1 : ]
    begpos = text.find(prefixBegStr)
  total_before_uniq = len(ytvideoids)
  # ytvideoids = list(set(ytvideoids))
  ytvideoids = uniquesize(ytvideoids)
  for ytvideoid in ytvideoids:
    print(ytvideoid)
  total_uniq = len(ytvideoids)
  return total_uniq, total_before_uniq

DEFAULT_FILENAME = 'a - YouTube 01.html'
dirpath = "/media/friend/SAMSUNG/z Tmp/YT videos tmp/Soc Sci tmp ytvideos/L Human Languages ytvideos/French Learning ytvideos/GF 100-v n' yyyy Grammaire Française yu Sulex Shana ytpl/"
def make_filepath(infilename=None, dirpath=None):
  if infilename is None:
    filename = DEFAULT_FILENAME
  else:
    filename = infilename
  if localfolder or dirpath is None:
    return filename
  filepath = os.path.join(dirpath, filename)
  return filepath

def go_extract(infilename=None, dirpath=None):
  filepath = make_filepath()
  text = open(filepath, 'r', encoding='utf8').read()
  _ = extract_videoids(text)

def get_args():
  for arg in sys.argv:
    if arg.startswith('-f='):
      infilename = arg[ len('-f=') : ]
      infilename = infilename.lstrip('"').rstrip('"')
      return infilename
    elif arg.startswith('--help'):
      print (__doc__)
      sys.exit()
  return None

def process():
  go_extract(get_args())

if __name__ == '__main__':
  localfolder = True
  process()
