#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, time
from BeautifulSoup import BeautifulStoneSoup

letterDict = { \
'c':'Filefactory' , \
'd':'Depositfiles'   , \
'e':'Easy-Share'   , \
'f':'Fileserve' , \
'k':'Freakshare' , \
'j':'Filejungle' , \
'i':'Filesonic' , \
'h':'Hotfile'   , \
'l':'Ul' , \
'm':'Megaupload'   , \
'n':'Netload'   , \
'o':'Oron'   , \
'r':'Rapidshare', \
's':'SharingMatrix', \
't':'Turboshare' , \
'u':'Uploading' , \
'p':'Uploaded' , \
'w':'Wupload' \
}
letters = letterDict.keys()
letters.sort()

def checkConsistency(serverNick, line):
  '''
  Only 2 cases for the moment
  Either it should starts with:
    supposedCase = 'http://' + serverNick + '.'
  or    
    supposedCase = 'http://www.' + serverNick + '.'
  '''
  supposedCase = 'http://' + serverNick + '.'
  if line.startswith(supposedCase):
    return True
  supposedCase = 'http://www.' + serverNick + '.'
  if line.startswith(supposedCase):
    return True
  return False

def explainArgumentAndExit():
  print 'Please, enter one of the letters as an argument: '
  for letter in letters:
    serverNick = letterDict[letter]
    print ' ==>> %(letter)s (%(serverNick)s)' %{'letter':letter,'serverNick':serverNick}
  sys.exit(0)

nOfLoop = 0
def processArg(arg):
  global nOfLoop
  letter = None; nOfLoop+=1
  if nOfLoop > 1:
    time.sleep(5) # wait 5 seconds
  print 'arg', arg,
  if arg and len(arg) > 0:
    letter = arg[0].lower() # should be one digit (one letter), it doesn't care if user typed more
    if letter not in letters:
      explainArgumentAndExit()

  MAX_N_OF_LAUNCHES = 1; flagDoUpdate = False

  # ok, letter is within letters
  serverNick = letterDict[letter].lower()
  DEFAULT_SHARE_SERVER = 'all-servers-share.txt'
  urlsFilename = '%(serverNick)s.txt' %{'serverNick':serverNick}
  if not os.path.isfile(urlsFilename):
    # well, file is not there, let's try the DEFAULT_SHARE_SERVER
    # check existence of DEFAULT_SHARE_SERVER = 'all-servers-share.txt'
    if os.path.isfile(DEFAULT_SHARE_SERVER):
      urlsFilename = DEFAULT_SHARE_SERVER
    else:
      print "Script couldn't find either:"
      print 'file: ', urlsFilename , 'or:'
      print 'file: ', DEFAULT_SHARE_SERVER, '(DEFAULT_SHARE_SERVER)'
      print 'Stopping.'
      sys.exit(0)

  print 'Opening', urlsFilename
  lines = open(urlsFilename).readlines(); nOfLaunches = 0
  for i in range(len(lines)):
    line = lines[i]
    if line.startswith('http://') and checkConsistency(serverNick, line):
      url = line.rstrip('\n').rstrip()
      nOfLaunches += 1
      print nOfLaunches, 'Firefox-launching', url
      os.system('firefox "%s"' %url)
      line = 'x ' + line
      lines[i] = line
      flagDoUpdate = True
      if nOfLaunches == MAX_N_OF_LAUNCHES:
        break

  if flagDoUpdate:
    print 'Updating', urlsFilename
    fileToUpdate = open(urlsFilename, 'w')
    fileToUpdate.writelines(lines)
    fileToUpdate.close()


def process():
  if len(sys.argv) < 2:
    explainArgumentAndExit()

  args = sys.argv[1:]
  for arg in args:
    processArg(arg)


if __name__ == '__main__':
  process()