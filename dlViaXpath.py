#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, time
'''


'''

from lxml import etree
def process():
  text = open('/home/friend/Téléchargements/ndvpyconau2013.xml').read()
  root = etree.XML(text)
  nodes = root.xpath('//Key')
  for node in nodes:
    mediafilename = node.text
    if mediafilename.endswith('.mp4'):
      print mediafilename

if __name__ == '__main__':
  process()
