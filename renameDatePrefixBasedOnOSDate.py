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
# from dlYouTubeMissingVideoIdsOnLocalDir import get_videoid_from_filename        

DEFAULT_EXTENSION = 'mp4'

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


class Rename:

  def __init__(self, targetfiles, boolForInputAskingRenames=True):
    self.targetfiles = targetfiles
    self.date_n_filename_tuple_list = []
    self.renametuplelist = []
    self.boolForInputAskingRenames = boolForInputAskingRenames
    self.boolConfirmedRenames = None
    self.processRename()

  def processRename(self):
    '''

    :return:
    '''
    self.date_n_filename_tuple_list = extract_date_n_filename_tuple_list(self.targetfiles)
    print('Renames with', len(self.targetfiles), 'files and', len(self.date_n_filename_tuple_list), 'date_n_filename_tuples')
    if len(self.date_n_filename_tuple_list) == 0:
      print ('No pair of files to renames. Either directory is empty or files already are date-prefixed.')
      return False # end of class-processing
    self.create_renametuplelist()
    self.printOutRenames()
    self.boolConfirmedRenames = True
    if self.boolForInputAskingRenames:
      self.askInputConfirmRenames()
    if self.boolConfirmedRenames:
      self.doRename()
    return True # end of class-processing

  def create_renametuplelist(self):
    '''

    :return:
    '''
    localRenametuplelist = []
    for date_n_filename_tuple in self.date_n_filename_tuple_list:
      strDate, oldfilename = date_n_filename_tuple
      newfilename = strDate + ' ' + oldfilename
      renametuple = oldfilename, newfilename
      localRenametuplelist.append(renametuple)

    usedfilenames = []
    self.renametuplelist = []
    for renametuple in localRenametuplelist:
      oldfilename, newfilename = renametuple
      if not os.path.isfile(oldfilename):
        print('File', oldfilename, 'not found having an equivalent in ids. Skipping to next one if any...')
        continue
      if newfilename not in usedfilenames and oldfilename not in usedfilenames:
        self.renametuplelist.append((oldfilename, newfilename))
        usedfilenames.append(oldfilename)
        usedfilenames.append(newfilename)
      else:
        print('Either', oldfilename, 'or', oldfilename, ' are already in renaming queue. Skipping to next one if any...')
        continue

  def printOutRenames(self):

    for i, tupl in enumerate(self.renametuplelist):
      seqNumber = i + 1
      currentName, newName = tupl
      print('Rename n.', seqNumber)
      print(' => ', currentName)
      print(' => ', newName)

  def askInputConfirmRenames(self):
    ans = input('Do rename files? (Y/n) ')
    self.boolConfirmedRenames = True
    if ans in ['n', 'N']:
      self.boolConfirmedRenames = False

  def doRename(self):

    if not self.boolConfirmedRenames:
      return

    nOfRenames = 0
    for renametuple in self.renametuplelist:
      oldfilename, newfilename = renametuple
      os.rename(oldfilename, newfilename)
      nOfRenames += 1

    print('nOfRenames = ', nOfRenames)


def find_file_extensions_in_args():
  ext_list_in_args = [DEFAULT_EXTENSION] # default
  boolForInputAskingRenames = True
  for arg in sys.argv:
    if arg.startswith('-y'):
      boolForInputAskingRenames = False
    if arg.startswith('-e='):
      # notice if user enters more than -e, only the last one will hold
      ext_args_str = arg[ len('-e=') : ]
      ext_list_in_args = ext_args_str.split(',') # no spacing is allowed in cli params
      # break # no break, wait in case a -y may appear
  args_dict = {'ext_list_in_args': ext_list_in_args, 'boolForInputAskingRenames':boolForInputAskingRenames}
  return args_dict

def process():
  args_dict = find_file_extensions_in_args()
  ext_list_in_args = args_dict['ext_list_in_args']
  boolForInputAskingRenames = args_dict['boolForInputAskingRenames']
  targetfiles = []
  for ext in ext_list_in_args:
    targetfiles += glob.glob('*.' + ext)
  # renameObj
  _ = Rename(targetfiles, boolForInputAskingRenames)

if __name__ == '__main__':
  process()
