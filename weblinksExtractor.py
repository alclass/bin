#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
'''
import os.path
import glob
import os
import sys
import BeautifulSoup as bs

commBase = 'ffmpeg -i "%(mediaFile)s" -vcodec libx264 "%(mp4)s"'
EXTENSIONS_DEFAULT = ['flv', 'm4v', 'mov']

def extractWeblinks(htmlFile):
  text = open(htmlFile).read()
  bSoup = bs.BeautifulSoup(text)
  aTags = bSoup.findAll('a')
  for eachWeblink in aTags:
    print eachWeblink.get('href')

def main():
  htmlFile = sys.argv[1]
  if not os.path.isfile(htmlFile):
    print htmlFile, 'is not a file on current folder. Please, retry.'
    sys.exit(1)
  extractWeblinks(htmlFile)

if __name__ == '__main__':
  main()
