#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
============================= Explanation of this Script's Job =============================
This script does the following:
  It touches new files based on the following rule:
  1) it copies the filename that has a certain/given extension;
  2) then it changes its extension by a fixed one that is name "empty";
  3) this new name is then touched (ie, it is created as a new empty file).
An example:
  If extension chosen is "mp4" and a file named "abc.mp4" is present on the local folder,
  a new file named "abc.empty", if it does not exist previously, will be created empty.
  This, in fact, will be done for all files with extension "mp4" on the local folder.
  
Syntax:
  touchEncloseReplaceExtByEmpty.py -e=<ext>
    where <ext> is a chosen extension.  If not given, default is "mp4".
============================= ****************************** =============================
'''
import glob, os, sys

class Toucher(object):
  '''
  This class instantiates an object that models that process chain, 
    including asking the user's confirmation, to touch new files
    names after a list of files with a certain extension, but
    having the extension "empty".
  '''
  
  def __init__(self, extension='mp4'):
    self.extension = extension
    self.shell_commands = []
    self.process()
    
  def process(self):
    self.prepare_touch()
    if self.ask_confirmation_for_touch():
      self.touch()

  def prepare_touch(self):
    files_with_given_extension = glob.glob('*.'+ self.extension)
    for i, filename in enumerate(files_with_given_extension):
      backoffset = len(self.extension) + 1
      newname = filename[ : -backoffset ] + '.empty'
      if not os.path.isfile(newname):
        comm = 'touch "%s"' %newname
        self.shell_commands.append(comm)

  def ask_confirmation_for_touch(self):
    if len(self.shell_commands) == 0:
      print 'There are no touches for this folder.'
      return False
    for i, comm in enumerate(self.shell_commands):
      seq = i + 1
      print seq, comm
      confirm_msg = ' Confirm the %d touchs above ? (Y/n) ' %len(self.shell_commands)
    ans = raw_input(confirm_msg) 
    if ans.lower() == 'N':
      return False
    return True

  def touch(self):
    for i, comm in enumerate(self.shell_commands):
      seq = i + 1
      print seq, comm
      os.system(comm)
    print '%d files were touched.' %len(self.shell_commands)


def process():
  extension = 'mp4'
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[ len('-e=') : ]
    elif arg == '-h' or arg == '--help':
      print __doc__
      return
  Toucher(extension)

if __name__ == '__main__':
  process()
