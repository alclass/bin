#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This script compresses the txt file that keeps ytids.
  The idea is to take the whole text, derive the ytid and
  leave only the ytid in text.

'''
import glob, os, sys

YT_FILE_EXTENSION_LIST = ['mp4', 'mp3']

FORBIDDEN_CHARS = ' "|\!@#$%&*()+=<>:?,.;/][}{ºª§\''
FORBIDDEN_CHARS_LIST = list(FORBIDDEN_CHARS)
forbidden_chars_lambda = lambda c : c in FORBIDDEN_CHARS_LIST
def extractYtId(line):
  '''

  :param line:
  :return:
  '''

  name, ext = os.path.splitext(line)
  # print ('name, ext' , name, ext)
  if len(name) < 11:
    return None

  # this is a RESTRICTION to this program, ie, a filename must have an extension, otherwise None is returned
  # this may be rethought in the future, but for now it's okay
  if ext is None or ext == '':
    return None

  # ext has a leading period ('.') that os.path.splitext() gives to it
  ext = ext.lstrip('.')
  # print (' ===>>> ext', ext)
  if ext not in YT_FILE_EXTENSION_LIST:
    return None

  supposed_ytid = name[-11 :  ]
  #supposed_ytid_list = list(supposed_ytid)
  true_false_list = list(map(forbidden_chars_lambda, supposed_ytid))
  # print (str(filtered))
  if True in true_false_list:
    return None

  if supposed_ytid == supposed_ytid.upper():
    return None

  if supposed_ytid == supposed_ytid.lower():
    return None

  return supposed_ytid

class FileSizeMinimizer:
  '''

  '''

  def __init__(self, inputFiles=[]):
    '''

    :param inputFiles:
    '''
    if len(inputFiles) == 0:
      self.inputFiles = glob.glob('z_ls-R_contents-*.txt')
    else:
      self.inputFiles = list(inputFiles)

    self.process()

  def process(self):
    '''

    :return:
    '''
    for i, inputFile in enumerate(self.inputFiles):
      seqInputFile = i + 1
      print (str(seqInputFile) + ' Processing ' + inputFile)
      newText = ''; saveApplied = False; nOfYtIds = 0
      oldText = open(inputFile).read()
      lines = oldText.split('\n')
      for line in lines:
        ytid = extractYtId(line)
        if ytid is not None and ytid != '' and ytid != line:
          saveApplied = True
          newText += ytid + '\n'
          nOfYtIds += 1
        else:
          continue
      # input file lines roll has finished at this point
      if newText == oldText or not saveApplied:
        print (str(seqInputFile) + ' file:' + inputFile + ' is already minimized or it does not have ytids.')
        continue
      # save applied
      # print (newText)
      print ('File number ' + str(seqInputFile) + ': Writing ' + inputFile + ' to disk.')
      outfile = open(inputFile, 'w')
      newText = newText.strip(' \t\r\n')
      outfile.write(newText)
      outfile.close()
      print ('Written ' + str(nOfYtIds) + ' ytids.')

def adhoc_test():
  fs = []
  fn = 'blah 12345678901.mp4'
  fs.append(fn)
  fn = 'blah 12aA5678901.mp4'
  fs.append(fn)
  fn = 'blah 1234%&5678901.mp4'
  fs.append(fn)
  fn = 'blah 1234 5678901.mp4'
  fs.append(fn)
  for f in fs:
    print (f + ' ... extracting ...')
    ytid = extractYtId(f)
    print (' ... extracting ...' + str(ytid))


def process():
  '''

  :return:
  '''
  if '-t' in sys.argv:
    adhoc_test()
    return
  FileSizeMinimizer()

if __name__ == '__main__':
  process()
