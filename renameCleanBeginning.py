#!/usr/bin/env python3
import os
import sys


def print_explanation_and_exit():
  print('Arguments to the script:')
  print('-e=<file-extension> (optional)')
  print('-p=<integer-string-index-position> (required)')
  sys.exit(0)


# args = ['-p=', '-e=']
class Args:
  def __init__(self):
    self.ext = None
    self.pos = None
    self.autoren_no_cli_confirm = False
    self.process_cli_args()
    self.check_if_at_least_pos_was_set()

  def process_cli_args(self):
    for arg in sys.argv:
      if arg.startswith('-e='):
        self.ext = arg[len('-e='):]
      elif arg.startswith('-p='):
        self.pos = int(arg[len('-p='):])
      elif arg.startswith('-y'):
        self.autoren_no_cli_confirm = True

  def check_if_at_least_pos_was_set(self):
    if self.pos is None:
      print_explanation_and_exit()

  def get_ext_with_period(self):
    return '.%s' % self.ext
   

def rename(args):
  pos_from = args.pos
  files = os.listdir('.')
  files.sort()
  for i in range(0, 2):
    c = 0
    for fil in files:
      name, ext = os.path.splitext(fil)
      # print 'name, ext', name, ext
      tam_name_without_ext = len(name)
      if ext is not None:
        if ext != args.get_ext_with_period():
          continue
      if pos_from >= tam_name_without_ext:
        continue
      elif pos_from >= len(fil):
        continue
      new_name = fil[pos_from:]
      c += 1
      print(c, 'renaming', fil)
      print('> to:>>>'+new_name)
      if i == 1:
        os.rename(fil, new_name)
    if c == 0:
      print('No files are sized above position', pos_from)
      break
    if i == 0 and c > 0:
      if not args.autoren_no_cli_confirm:
        ans = input('Are you sure? (y/n) ')  # raw_input
        if ans != 'y':
          break


def process():
  args = Args()
  rename(args)


if __name__ == '__main__':
  process()
  # unittest.main()
