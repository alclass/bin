#!/usr/bin/env python3
import glob, os, string, sys #, shutil, sys

def print_explanation_and_exit():
  print ('Arguments to the script:')
  print ('-e=<file-extension> (optional)')
  print ('-p=<integer-string-index-position> (required)')
  sys.exit(0)

# args = ['-p=', '-e=']
class Args:
  def __init__(self):
    self.ext = None
    self.pos = None
    self.process_cli_args()
    self.check_if_at_least_pos_was_set()

  def process_cli_args(self):
    for arg in sys.argv:
      if arg.startswith('-e='):
        self.ext = arg[len('-e=') : ]
      elif arg.startswith('-p='):
        self.pos = int( arg[len('-p=') : ] )

  def check_if_at_least_pos_was_set(self):
    if self.pos == None:
      print_explanation_and_exit()

  def get_ext_with_period(self):
    return '.%s' %self.ext
   
def rename(args):        
  posFrom = args.pos
  files=os.listdir('.')
  files.sort()
  for i in range(0,2):
    c=0
    for fil in files:
      name, ext = os.path.splitext(fil)
      # print 'name, ext', name, ext
      tamNameWithoutExt = len(name)
      if ext != None:
        if ext != args.get_ext_with_period():
          continue
      if posFrom >= tamNameWithoutExt:
        continue
      elif posFrom >= len(fil):
        continue
      newName = fil[posFrom:]
      c += 1
      print (c, 'renaming', fil)
      print ('> to:>>>'+newName)
      if i==1:
        os.rename(fil, newName)
    if c==0:
      print ('No files are sized above position', posFrom)
      break
    if i==0 and c > 0:
      ans = input('Are you sure? (y/n) ') # raw_input
      if ans != 'y':
        break

def process():
  args = Args()
  rename(args)

if __name__ == '__main__':
  process()
  # unittest.main()
