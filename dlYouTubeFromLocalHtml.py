#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import os, re, sys

urlBase = 'www.youtube.com/watch?v=%s'
commBase = 'youtube-dl "%s"'

def getLocalHtmlFileFromSysArg():
  htmlFilename = sys.argv[1]
  if os.path.isfile(htmlFilename):
    return htmlFilename
  print 'file', htmlFilename, 'is not here on local folder.'
  sys.exit(1)

filesOnCurrentDir = os.listdir('.')
def isItOnCurrentDir(uTubeIds):
  for eachFile in filesOnCurrentDir:
    if eachFile.find(uTubeIds) > -1:
      return True
  return False
  
def youtubeDownload():
  htmlFilename = getLocalHtmlFileFromSysArg()
  reStr = '/watch[?]v[=](\w+)&'
  reComp = re.compile(reStr)
  iterObj = reComp.findall(open(htmlFilename).read())
  total = len(iterObj); seq = 0; uTubeIdsList = []
  for uTubeIds in iterObj:
    if uTubeIds in uTubeIdsList:
      total -= 1; print 'Video repeat, moving on to next one', seq+1, 'of', total 
      continue
    if isItOnCurrentDir(uTubeIds):
      total -= 1; print 'There is a video with the same id %s, moving on to next one' %uTubeIds, seq+1, 'of', total 
      continue
    uTubeIdsList.append(uTubeIds)
    seq += 1
    print seq, 'of', total, uTubeIds
    url = urlBase %uTubeIds
    comm = commBase %url
    os.system(comm)

if __name__ == '__main__':
  # copyToUsb()
  youtubeDownload()
