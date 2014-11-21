#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys, time

DEFAULT_PAUSE_BETWEEN_DOWNLOADS = 5 # seconds
commbase = 'wget -c "http://www.youtube.com/results?search_query=%(artist_1st_name)s+%(artist_2nd_name)s&page=%(seq)d" -O "%(artist_1st_name)s %(artist_2nd_name)s - YouTube %(seq)d.html"'

def issueWgetToFetchPages(artist_tuple, pause_in_between_downloads = None):
  artist_1st_name = artist_tuple[0]  
  artist_2nd_name = artist_tuple[1]   
  start_page      = int(artist_tuple[2])
  end_page        = int(artist_tuple[3])
  comm_dict = {'artist_1st_name':artist_1st_name, 'artist_2nd_name':artist_2nd_name}
  if pause_in_between_downloads == None:
    pause_in_between_downloads = DEFAULT_PAUSE_BETWEEN_DOWNLOADS 
  for seq in range(start_page, end_page+1):
    comm_dict['seq'] = seq
    comm = commbase %comm_dict
    print 'Downloading:'
    os.system(comm)
    time.sleep(pause_in_between_downloads)

def find_start_page_if_any():
  start_page = 1
  for index, arg in enumerate(sys.argv):
    if arg.startswith('-s='):
      try:
        start_page = int( arg[ len('-s=') : ] )
        del sys.argv[index]
        break
      except IndexError:
        pass
      except ValueError:
        pass
  return start_page

def process():
  start_page = find_start_page_if_any()
  artist_1st_name = sys.argv[1]  
  artist_2nd_name = sys.argv[2]   
  end_page        = int(sys.argv[3])
  artist_tuple = artist_1st_name, artist_2nd_name, start_page, end_page
  issueWgetToFetchPages(artist_tuple)

if __name__ == '__main__':
  process()
