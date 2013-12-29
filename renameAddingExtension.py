#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os

files = glob.glob('*')
for i in range(1, 37):
  iStr = '%02d' %i
  mp3 = glob.glob('%s*' %iStr)[0]
  if not mp3.endswith('.mp3'):
    os.rename(mp3, mp3 + '.mp3')
  