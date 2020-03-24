#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This script was originally written for Python2 at a moment Python3 did not yet exist
  or, at least, was not amply adopted.

Below, a historical change (on March 14, 2020) is noted:

=> In the former version, the working variable was instantiated as:
      from BeautifulSoup import BeautifulStoneSoup
      bSoup = BeautifulStoneSoup(text)

=> Years later, the working variable moved to be instantiated as:
      from bs4 import BeautifulSoup
      bSoup = BeautifulSoup(text, 'xml')

The "finding" method is still the same, ie:
      trunksFound = bSoup.findAll('enclosure')

In fact, the above findAll() method is the heart of this script,
  because the <enclosure> tag is where the media URL is located.
'''
import os
import sys
# from BeautifulSoup import BeautifulStoneSoup
from bs4 import BeautifulSoup

def checkFilenameInput():
  if len(sys.argv) < 2:
    print ('xmlRss Filename argument is missing.')
    sys.exit(0)

def pickUpXmlRssFilename():
  xmlRssFilename = sys.argv[1]
  if not os.path.isfile(xmlRssFilename):
    error_msg = 'xmlRss Filename %s was not found.' %(xmlRssFilename)
    print (error_msg)
    sys.exit(0)
  return xmlRssFilename

def printOutUrlsFoundInsideEnclosure(xmlRssFilename):
  text = open(xmlRssFilename).read()
  # bSoup = BeautifulStoneSoup(text)
  bSoup = BeautifulSoup(text, 'xml')
  # print bSoup.prettify()
  trunksFound = bSoup.findAll('enclosure')
  for trunk in trunksFound:
    url = trunk['url']
    # one purpose for this script's user is to redirect output to a file
    # and download the url's with "wget -c --input-file=<file>"
    print (url)

def process():
  checkFilenameInput()
  xmlRssFilename = pickUpXmlRssFilename()
  printOutUrlsFoundInsideEnclosure(xmlRssFilename) 

if __name__ == '__main__':
  process()
