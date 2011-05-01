#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from BeautifulSoup import BeautifulStoneSoup

if len(sys.argv) < 2:
  print 'xmlRss Filename argument is missing.'
  sys.exit(0)

xmlRss = sys.argv[1]
if not os.path.isfile(xmlRss):
  print 'xmlRss Filename %s was not found.' %(xmlRss)
  sys.exit(0)

text = open(xmlRss).read()
bSoup = BeautifulStoneSoup(text)
# print bSoup.prettify()
trunksFound = bSoup.findAll('enclosure')
for trunk in trunksFound:
  url = trunk['url']
  # the purpose is the redirect output to a file
  # and download the url's with "wget -c --input-file=<file>"
  print url
