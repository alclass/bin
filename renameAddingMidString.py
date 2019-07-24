#!/usr/bin/env python3
# No longer need in Python3: -*- coding: utf-8 -*-
import glob, os, sys

DEFAULT_EXTENSION = 'mp4'

class Renamer:
  '''

  '''
  
  def __init__(self, includeStr, extList=None, pos=0):
    '''

    :param extList:
    :param pos:
    '''
    self.rename_pairs = []
    if (includeStr is None or includeStr == '' or type(includeStr)!= str):
      error_msg = ' Error:\n Cannot continue without an include string.\n Please retry entering an include string.'
      # raise ValueError(error_msg)
      print (error_msg)
      return
    else:
      self.includeStr = includeStr
    self.extList = None
    self.set_extList(extList)
    self.pos = None
    self.set_pos(pos)
    self.processRename()

  def set_pos(self, pos):
    '''

    :param pos:
    :return:
    '''
    if pos is None:
      self.pos = 0
      return
    try:
      self.pos = int(pos)
    except ValueError:
      self.pos = 0

  def set_extList(self, extList):
    '''
    extList is treated here as transfered-by-copy,
      ie, it's not passed as reference below, being copied on place

    :param extList:
    :return:
    '''
    if extList is None or len(extList) == 0 or type(extList)!=list:
      self.extList = [DEFAULT_EXTENSION]
    else:
      self.extList = list(extList)

  def processRename(self):
    self.search_renames()
    if self.confirm_renames():
      self.do_renames()

  def search_renames(self):
    self.rename_pairs = []
    for extension in self.extList:
      glob_str = '*.' + extension
      files = glob.glob(glob_str)
      for filename in files:
        name, ext = os.path.splitext(filename)
        if len(name) < self.pos:
          continue
        before_str =  filename[0 : self.pos]
        after_str = filename[self.pos : ]
        new_name = before_str + self.includeStr + after_str
        rename_pair = (filename, new_name)
        self.rename_pairs.append(rename_pair)

  def confirm_renames(self):
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      print(seq, 'Rename:')
      old_name, new_name = rename_pair
      print('FROM: >>>%s' %old_name)
      print('TO:   >>>%s' %new_name)
    ans = input('Confirm the %d renames above ? (y/N) ' %len(self.rename_pairs))
    if ans.lower() == 'y':
      return True
    print( 'No renames were done.' )
    return False
    
  def do_renames(self):
    print('-'*40)
    for i, rename_pair in enumerate(self.rename_pairs):
      old_name, new_name = rename_pair
      seq = i + 1
      print( seq, 'Rename:' )
      print( 'FROM: >>>%s' %old_name )
      print( 'TO:   >>>%s' %new_name )
      os.rename(old_name, new_name)
    print('-'*40)
    print('Finished %d renames.' %len(self.rename_pairs))

lambdaNotEmptyStr = lambda c : c != ''
def cleanEmptyStrInList(listIn):
  return list(filter(lambdaNotEmptyStr, listIn))

def getArgs():
  exts, pos = [DEFAULT_EXTENSION], 0
  includeStr = None
  for arg in sys.argv:
    if arg.startswith('-e='):
      ext_arg = arg[len('-e=') : ]
      exts = ext_arg.split(',')
      exts = cleanEmptyStrInList(exts)
    elif arg.startswith('-p='):
      pos = arg[len('-p=') : ]
    elif arg.startswith('-i='):
      includeStr = arg[len('-e=') : ]
  return exts, pos, includeStr

def process():
  '''
  '''
  extList, pos, includeStr = getArgs()
  Renamer(includeStr, extList, pos)

if __name__ == '__main__':
  process()
