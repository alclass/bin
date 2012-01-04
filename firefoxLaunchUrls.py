#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, time
lines=open('urls.txt').readlines()
tam = len(lines)
'''
if len(lines) > 10:
  print 'please, diminish number of urls. It is %d' %tam
  sys.exit(0)
'''  
c=0
for line in lines:
  if len(line) == 0:
    continue
  if line.startswith('#END'):
    sys.exit(0)
  if line[0]=='#':
    continue
  comm='firefox %s' %line
  c+=1
  print c, 'of', tam, ':: launching', line
  os.system(comm)
  print 'waiting 20 seconds for next url'
  time.sleep(20)