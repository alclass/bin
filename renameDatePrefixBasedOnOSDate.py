#!/usr/bin/env python3
#-*-coding:utf-8-*-
'''
This script renames files prefixing them with its OS-mtime's date as a yyyy-mm-dd prefix.
  Example:
    1) supose there's a filename = 'thisfile.ext'
    2) supose its modified date is decoded in 2018-06-10.
  Then:
    Its newname will become:
      '2018-06-10 thisfile.ext'

Created on 10/jul/2018

@author: friend
'''
import glob, datetime, os, sys
from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename        

def create_renametuplelist(date_n_filename_tuple_list, doRenameThem=False):
  renametuplelist = []
  for date_n_filename_tuple in date_n_filename_tuple_list:
    strDate, oldfilename = date_n_filename_tuple
    newfilename = strDate + ' ' + oldfilename
    renametuple = oldfilename, newfilename
    renametuplelist.append(renametuple)
  return renametuplelist

def doRename(p_renametuplelist=[], doRenameThem=False):
  usedfilenames = []; renametuplelist = []
  for renametuple in p_renametuplelist:
    oldfilename, newfilename = renametuple
    if not os.path.isfile(oldfilename):
      print('File', oldfilename, 'not found having an equivalent in ids. Skipping to next one if any...')
      continue
    if newfilename not in usedfilenames and oldfilename not in usedfilenames:
      renametuplelist.append((oldfilename, newfilename))
      usedfilenames.append(oldfilename)
      usedfilenames.append(newfilename)
    else:
      print('Either', oldfilename, 'or', oldfilename, ' are already in renaming queue. Skipping to next one if any...')
      continue

  nOfRenames = 0
  for i, tupl in enumerate(renametuplelist):
    seqNumber = i + 1
    currentName, newName = tupl
    print('Rename n.', seqNumber)
    print(' => ', currentName)
    print(' => ', newName)

    if doRenameThem:
      os.rename(currentName, newName)
      nOfRenames += 1

  if doRenameThem is True:
      print('nOfRenames = ', nOfRenames) 

  else:  # ie if doRenameThem is False:
    ans = input('Do rename files? [type in y or Y for Yes, anything else for No] ')
    if ans in ['y', 'Y']:
      doRename(renametuplelist, doRenameThem=True)

def doesFilenameAlreadyHaveADatePrefix(eachFile):
  if len(eachFile) < 10:
    return False
  if eachFile[4:5] != '-':
    return False
  if eachFile[7:8] != '-':
    return False
  if eachFile[10:11] != ' ':
    return False
  strYear      = eachFile[0:4]
  str2DigMonth = eachFile[5:7]
  strDay       = eachFile[8:10]
  try:
    int(strYear)
    i = int(str2DigMonth)
    if i < 0 or i > 12:
      return False
    i = int(strDay)
    if i < 0 or i > 31:
      return False
  except ValueError:
    return False
  return True

def extract_date_n_filename_tuple_list(files):
  date_n_filename_tuple_list = []
  for eachFile in files:
    if doesFilenameAlreadyHaveADatePrefix(eachFile):
      continue
    stat = os.stat(eachFile)
    if stat is None:
      continue
    mtime = stat.st_mtime
    mtimeDate = datetime.date.fromtimestamp(mtime)
    strYear, str2DigMonth, strDay = str(mtimeDate.year), str(mtimeDate.month).zfill(2), str(mtimeDate.day).zfill(2)
    strDate = '%s-%s-%s' %(strYear, str2DigMonth, strDay)
    tupl = (strDate, eachFile)
    date_n_filename_tuple_list.append(tupl)
  return date_n_filename_tuple_list

DEFAULT_YTPL_ORDER_TXT_IDS_FILE = 'youtube-ids.txt'
def process():
  files = os.listdir('.')
  if DEFAULT_YTPL_ORDER_TXT_IDS_FILE not in files:
    print('File', DEFAULT_YTPL_ORDER_TXT_IDS_FILE, 'is missing on current folder. Script cannot proceed.')
    sys.exit(1)
  mp4s = glob.glob('*.mp4')
  date_n_filename_tuple_list = extract_date_n_filename_tuple_list(mp4s)
  print('doRename with', len(mp4s), 'files and', len(date_n_filename_tuple_list), 'date_n_filename_tuples')
  renametuplelist = create_renametuplelist(date_n_filename_tuple_list)
  doRename(renametuplelist)
          
if __name__ == '__main__':
  process()
