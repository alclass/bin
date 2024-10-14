#!/usr/bin/env python3
"""
# -*- coding: utf-8 -*-

"""
import glob
import os
import sys


class Renamer(object):
  
  def __init__(self, extension=None):
    if extension is None:
      raise ValueError('Extension should be entered.')
    self.extension = extension
    self.rename_pairs = []
    self.process()

  def process(self):
    self.search_renames()
    if self.confirm_renames():
      self.do_renames()
    
  def search_renames(self):
    files = glob.glob('*')
    for old_name in files:
      new_name = old_name + '.%s' % self.extension
      rename_pair = (old_name, new_name)
      self.rename_pairs.append(rename_pair)

  def confirm_renames(self):
    for i, rename_pair in enumerate(self.rename_pairs):
      old_name, new_name = rename_pair
      seq = i + 1
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
    ans = input('Confirm the %d renames above ? (y/N) ' % len(self.rename_pairs))
    if ans.lower() == 'y':
      return True
    print('No renames were done.')
    return False
    
  def do_renames(self):
    print('-'*40)
    for i, rename_pair in enumerate(self.rename_pairs):
      old_name, new_name = rename_pair
      seq = i + 1
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
      os.rename(old_name, new_name)
    print('-'*40)
    print('Finished %d renames.' % len(self.rename_pairs))
    

def process():
  """

  :return:
  """
  Renamer(sys.argv[1])


if __name__ == '__main__':
  process()
