#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
  This script ...
'''
import sys

def invertString(word):
  invertedWord = ''
  for i in range(len(word)-1, -1, -1):
    invertedWord += word[i]
  return invertedWord
    
def pickUpStringFromSysArg():
  if len(sys.argv) < 2:
    print 'Please, retry entering a word as argument.'
    sys.exit(1)
  return sys.argv[1]

def process():
  word = pickUpStringFromSysArg()
  print invertString(word)

if __name__ == '__main__':
  process()
