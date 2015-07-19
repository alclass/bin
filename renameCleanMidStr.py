#!/usr/bin/env python
import glob, os, string, sys #, shutil, sys
import getopt

'''
Options
'''
#import renameCleanBeginning as rcb

def print_explanation_and_exit():
  print 'Arguments to the script:'
  print '-e=<file-extension> (optional)'
  print '-p=<integer-string-index-position> (required)'
  print '-s=<integer-string-size-from-index> (required)'
  sys.exit(0)

# args = ['-p=', '-e=', '-s']
class Args:
  def __init__(self):
    self.ext  = None
    self.pos  = None
    self.size = None
    self.process_cli_args()
    self.check_if_pos_and_size_were_set()

  def process_cli_args(self):
    for arg in sys.argv:
      if arg.startswith('-e='):
        self.ext = arg[len('-e=') : ]
      elif arg.startswith('-p='):
        self.pos = int( arg[len('-p=') : ] )
      elif arg.startswith('-s='):
        self.size = int( arg[len('-s=') : ] )

  def check_if_pos_and_size_were_set(self):a
    if self.pos == None or self.size == None:
      print_explanation_and_exit()

  def get_ext_with_period(self):
    return '.%s' %self.ext
   
def rename(args):
  files=os.listdir('.')
  files.sort()
  for i in range(0,2):
    c=0
    for fil in files:
      name, ext = os.path.splitext(fil)
      if args.get_ext_with_period() <> ext:
        continue
      if args.pos + args.size > len(name):
        continue
      newName = name[ : args.pos] + name [ args.pos + args.size :] + ext
      c += 1
      print c, 'renaming', fil
      print '> to:', newName
      if i==1:
        os.rename(fil, newName)
    if c==0:
      print 'No files are sized above position', args.pos
      break
    if i==0 and c > 0:
      ans = raw_input('Are you sure? (y/n) ')
      if ans != 'y':
        break

def process():
  args = Args()
  rename(args)

if __name__ == '__main__':
  process()
  # unittest.main()
