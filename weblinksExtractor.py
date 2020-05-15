#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Explanation
'''
import os.path
import glob
import os
import sys
# import BeautifulSoup as bs # obsolete way, when this script was run under Python2
import bs4 as bs

commBase = 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mp4)s"'
EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mov']

def getWeblinksAsATags(htmlFile):
  text = open(htmlFile).read()
  # the features parameter below was not necessary before, in the past, when this script was run under Python2
  bSoup = bs.BeautifulSoup(text, features='lxml') # parser 'lxml' covers html and is installed with PIP system-wide
  aTags = bSoup.find_all('a') # when used in Python2, in the past, methodname was findAll()
  return aTags

def getWeblinksAsHRefs(htmlFile):
  urls = []
  aTags = getWeblinksAsATags(htmlFile)
  for eachWeblink in aTags:
    url = eachWeblink.get('href')
    urls.append(url)
  return urls

def extractWeblinks(htmlFile):
  urls = getWeblinksAsHRefs(htmlFile)
  for url in urls:
    print (url)

def main():
  htmlFile = sys.argv[1]
  if not os.path.isfile(htmlFile):
    print (htmlFile, 'is not a file on current folder. Please, retry.')
    sys.exit(1)
  extractWeblinks(htmlFile)

if __name__ == '__main__':
  main()

