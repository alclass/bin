#!/usr/bin/env python3
"""
Usage: <this_script> -i=<number_of_first_mp4> -d=<number_of_mp4s>

The script's functionality:

It renames srt and mp4 files that Udacity makes available via a zipped archive.
In general, srt's have a beginning number starting with 1
  whereas the mp4's may start with a greater-than number (see example below).

Example:
  In the following example, srt's start with 1 and mp4's start with 68

command$ <this_script> -i=68 -d=24
1 oldname [01 - Intro.srt] => newname [68 Intro.srt]
2 oldname [68 - Intro .mp4] => newname [68 Intro.mp4]
3 oldname [02 - Iteration.srt] => newname [69 Iteration.srt]
4 oldname [69 - Iteration!.mp4] => newname [69 Iteration.mp4]
   (etc up to)
45 oldname [23 - Paul on Persistence.srt] => newname [90 Paul on Persistence.srt]
46 oldname [90 - Paul on Persistence.mp4] => newname [90 Paul on Persistence.mp4]
47 oldname [24 - Outro.srt] => newname [91 Outro.srt]
48 oldname [91 - Outro.mp4] => newname [91 Outro.mp4]

  Confirm above renames? (*Y/n)
Answering a Y or y or a blank (just an [Enter]) means 'yes', ie a confirmation for renaming.
"""
import glob
import math
import os
import sys


def strzeroesfilled(n, amount):
  ndigits = int(math.log(amount, 10) + 1)
  return str(n).zfill(ndigits)


def leftstrip_number_n_dash(extless_name):
  pp = extless_name.split(' ')
  try:
    int(pp[0])
    if pp[1] == '-':
      recomposed_name = ' '.join(pp[2:])
      return recomposed_name
  except (IndexError, ValueError) as e:
    pass
  return None


def cleanup_chars_from_str(name, charlist):
  for c in charlist:
    if name.find(c) > -1:
      name = name.replace(c, '')
  return name


def cleanup_questionmark_n_exclamationpoint(name):
  chars_to_remove = ['?', '!']
  return cleanup_chars_from_str(name, chars_to_remove)


def find_numberprefixedfile_in_files(ini_number, files):
  amount = len(files)
  for f in files:
    if f.startswith(strzeroesfilled(ini_number, amount)):
      return f
  return None


class Renamer:

  def __init__(self, ini_number, delta):
    self.ini_number = ini_number
    self.delta = delta
    print('ini_number', ini_number, 'delta', delta)
    self.rename_pairs = []

  def process_rename(self):
    self.prep_rename()
    self.show_renames()
    if self.confirm_renames():
      self.do_renames()

  def prep_rename(self):
    mp4files = glob.glob('*.mp4')
    mp4files = sorted(mp4files)
    print(mp4files)
    srtfiles = glob.glob('*.srt')
    filesamount = len(mp4files)
    seq = 0
    ini_number = self.ini_number
    upto = self.ini_number + self.delta
    for mp4number in range(ini_number, upto):
      seq += 1
      mp4file = find_numberprefixedfile_in_files(mp4number, mp4files)
      print('with', mp4number, 'found', mp4file)
      if mp4file is None:
        continue
      extless_name, _ = os.path.splitext(mp4file)
      srt_oldname = find_numberprefixedfile_in_files(seq, srtfiles)
      if srt_oldname is None:
        continue
      mp4_oldname = find_numberprefixedfile_in_files(mp4number, mp4files)
      if mp4_oldname is None:
        continue
      numberless_name = leftstrip_number_n_dash(extless_name)
      numberless_name = cleanup_questionmark_n_exclamationpoint(numberless_name)
      numberless_name = numberless_name.strip(' \t\r\n')
      srt_newname = strzeroesfilled(mp4number, filesamount) + ' ' + numberless_name + '.srt'
      mp4_newname = strzeroesfilled(mp4number, filesamount) + ' ' + numberless_name + '.mp4'
      pair = (srt_oldname, srt_newname)
      self.rename_pairs.append(pair)
      pair = (mp4_oldname, mp4_newname)
      self.rename_pairs.append(pair)

  def show_renames(self):
    for i, pair in enumerate(self.rename_pairs):
      oldname, newname = pair
      print(i+1, 'oldname [' + oldname + '] => newname [' + newname + ']')

  def confirm_renames(self):
    ans = input('Confirm above renames? (*Y/n) ')
    if ans in ['y', 'Y', '']:
      return True
    return False

  def do_renames(self):
    n_renames = 0
    for i, pair in enumerate(self.rename_pairs):
      oldname, newname = pair
      if not os.path.isfile(oldname):
        print ('Not renaming due to source-file (oldname)', oldname, 'not existing.')
        continue
      if os.path.isfile(newname):
        print ('Not renaming due to target-file (newname)', newname, 'existing priorly.')
        continue
      print(i+1, 'oldname [' + oldname + '] => newname [' + newname + ']')
      os.rename(oldname, newname)
      n_renames += 1
    print('Number of renames', n_renames)


def get_args():
  ini_number = 1
  delta = 10
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-i'):
      ini_number = int(arg[len('-i='): ])
    elif arg.startswith('-d'):
      delta = int(arg[len('-d='): ])
  return ini_number, delta


def adhoc_test1():
  n = 7
  amount = 99
  s = strzeroesfilled(n, amount)
  print('n =', n, ', amount = ', amount, ', strzeroesfilled = ', s)
  n = 2
  amount = 111
  s = strzeroesfilled(n, amount)
  print('n =', n, ', amount = ', amount, ', strzeroesfilled = ', s)
  n = 8
  amount = 9
  s = strzeroesfilled(n, amount)
  print('n =', n, ', amount = ', amount, ', strzeroesfilled = ', s)

def main():
  # adhoc_test1()
  # return
  ini_number, delta = get_args()
  renamer = Renamer(ini_number, delta)
  renamer.process_rename()


if __name__ == '__main__':
  main()
