#!/usr/bin/env python
import glob, os, sys

DEFAULT_EXTENSION = 'txt'

def printFormatted(files):
  line = ''; n=0
  for fil in files:
    printFil = fil
    if len(fil) > 35:
      printFil = fil[:35]
    space = 5 + (35 - len(printFil))
    n += 1
    if n % 3 == 1:
      print line
      line = ''
    line += str(n).zfill(2) + '  ' + printFil + ' '*space
  print line
  print
  
def convertEncoding(files):
  for fileToConvEncoding in files:
    tmpName = fileToConvEncoding + '.iso8859-1'
    if os.path.isfile(tmpName):
      print 'file', tmpName, 'already exists, skipping...'
      continue
    os.rename(fileToConvEncoding, tmpName)
    comm = 'iconv -f iso8859-1 -t utf8 "' + tmpName + '" --output="' + fileToConvEncoding + '"'
    retValue = os.system(comm)
    print comm
    print 'RETURNS', retValue

def prepareForConversion(extension = DEFAULT_EXTENSION):
  if len(sys.argv) > 1:
    extension = sys.argv[1]
  files=glob.glob('*.' + extension)
  nOfFiles=len(files)
  if nOfFiles < 1:
    print 'No files with the extension', extension
    sys.exit(0)
  print ' Operation will be on files with extension', extension,':'
  printFormatted(files)
  ans = raw_input('Are you sure to encoding-convert these ' + str(nOfFiles) + ' files? (y/n) ')
  if ans != 'y':
    sys.exit(0)
  convertEncoding(files)

if __name__ == '__main__':
  prepareForConversion()
