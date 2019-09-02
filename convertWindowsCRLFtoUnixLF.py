#!/usr/bin/env python3
# --*-- encoding: utf8 --*--
import os, sys

def try_only_slashr(text):
  newText = text.replace('\r', '')
  if newText != text:
    print ('There are slash r.')
    return

def convertCRLFtoLF(filenameIn):
  '''

  :param filenameIn:
  :return:
  '''
  msgLine = 0
  msgLine += 1; print (msgLine, 'Reading', filenameIn)
  text = open(filenameIn).read()
  if not text.find('\r\n')>-1:
    msgLine += 1; print (msgLine, 'Could not detect Windows 2-char style newline.')
    msgLine += 1; print (msgLine, 'File may have already been converted, nothing to do for now.')
    return try_only_slashr(text)
  msgLine += 1; print (msgLine, 'Detected Windows 2-char style newline.')
  msgLine += 1; print (msgLine, 'Converting it to Unix-like newline.')
  text = text.replace('\r\n', '\n')
  textOut = text.replace('\r', '\n')
  if textOut.find('\r\n')>-1:
    msgLine += 1; print (msgLine, 'Something failed, file still has Windows 2-char style newline.')
    msgLine += 1; print (msgLine, 'Giving up now.')
    sys.exit(0)
  msgLine += 1; print (msgLine, 'Backing up the Windows 2-char style newline file.')

  filenameOut = ''; c=2
  while c < 100:
    filenameOut = sys.argv[1] + '.' + str(c).zfill(2)
    msgLine += 1; print (msgLine, 'Attempting to use', filenameOut)
    if os.path.isfile(filenameOut):
      if c >= 100:
        error_msg = 'Error: please delete files named ' + filenameIn + '.xx where xx is from 02 to 99.'
        raise Exception(error_msg)
    else:
      break
  msgLine += 1; print (msgLine, 'OK. Writing', filenameOut)
  fileOut = open(filenameOut, 'w')
  fileOut.write(textOut)
  fileOut.close()

  if os.path.isfile(filenameOut):
    msgLine += 1; print (msgLine, 'Renaming', filenameIn, 'to', filenameIn + '.bak')
    os.rename(filenameIn, filenameIn + '.bak')
    msgLine += 1; print (msgLine, 'Renaming', filenameOut, 'to', filenameIn)
    os.rename(filenameOut, filenameIn)
    msgLine += 1; print ('Finished converting', filenameIn)

def doGlob(globStr):
  import glob
  files = glob.glob(globStr)
  print ('Files', files)
  for filenameIn in files:
    convertCRLFtoLF(filenameIn)

def process():
  if len(sys.argv) < 2:
    print ('No arguments given. Please give it a filename or a glob argument.')
    sys.exit(0)
  argsList = sys.argv[1:]
  print ('argsList', argsList)
  for filenameIn in argsList:
    print ('   [CONVERTING]  ', filenameIn)
    convertCRLFtoLF(filenameIn)


if __name__ == '__main__':
  process()
