#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from BeautifulSoup import BeautifulStoneSoup

def checkFilenameInput():
  if len(sys.argv) < 2:
    print 'xmlRss Filename argument is missing.'
    sys.exit(0)

def pickUpXmlRssFilename():
  xmlRssFilename = sys.argv[1]
  if not os.path.isfile(xmlRssFilename):
    print 'xmlRss Filename %s was not found.' %(xmlRssFilename)
    sys.exit(0)
  return xmlRssFilename

def printOutUrlsFoundInsideEnclosure(xmlRssFilename):
  text = open(xmlRssFilename).read()
  bSoup = BeautifulStoneSoup(text)
  # print bSoup.prettify()
  trunksFound = bSoup.findAll('enclosure')
  for trunk in trunksFound:
    url = trunk['url']
    # one purpose for this script's user is to redirect output to a file
    # and download the url's with "wget -c --input-file=<file>"
    print url

def process():
  checkFilenameInput()
  xmlRssFilename = pickUpXmlRssFilename()
  printOutUrlsFoundInsideEnclosure(xmlRssFilename) 

if __name__ == '__main__':
  process()
