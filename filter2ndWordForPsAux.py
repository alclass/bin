#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This small script aims to filter out the 2nd words from each line in a text file.
The original need came from "ps aux | grep <word>"
  when we were interested in the process-number-id (the 2nd word for each listed process)
Under this idea, this script is to be used in a pipeline command as shown in the usage below.

Usage:
1) $filter2ndWordForPsAux.py [--adhoctest] | [--help]
2) $filter2ndWordForPsAux.py < command_that_outputs_text [-n] [-k]
3) $command_that_outputs_text | filter2ndWordForPsAux.py

Where:
--adhoctest  :: is a parameter to run a sample "ps aux" text as an adhoc test
                after running the adhoc test it exits
--help  :: parameter that shows this text and exists
-n      :: only gets 2nd words that are numbers (int)
-k      :: outputs a "kill -9 process-list" line (it does not execute it)

Example:
  $ps aux | grep vlc | filter2ndWordForPsAux.py
"""
import sys


def from_list_to_strlist(outlines):
  outlines = map(lambda w: str(w), outlines)
  return list(outlines)


def from_list_to_lineartext(outlist):
  outstr = " ".join(from_list_to_strlist(outlist))
  return outstr


def from_list_to_text(outlines):
  outstr = "\n".join(from_list_to_strlist(outlines))
  return outstr


def extract_2nd_word_from_line(line, as_number=False):
  pp = line.split(" ")
  pp = filter(lambda w: w != "", pp)  # filters out the empty elements ["", "", ""...]
  pp = list(pp)
  if len(pp) > 1:
    try:
      if as_number:
        w = int(pp[1])  # in case that the second word needs to be a number (an int)
      else:
        w = pp[1]
      return w
    except ValueError:
      pass
  return None


def extract_2nd_words_from_stdin_or_param(p_textlines=None, as_number=False):
  second_words = []
  textlines = p_textlines or sys.stdin.readlines()
  for line in textlines:
    line = line.lstrip(' \t').rstrip(' \t\r')
    if line == '':
      continue
    secword = extract_2nd_word_from_line(line, as_number)
    if secword:
      second_words.append(secword)
  return second_words


def gen_output(outlist, output_kill9=False):
  if not output_kill9:
    output = from_list_to_text(outlist)
    print(output)
  else:
    strprocesses = from_list_to_lineartext(outlist)
    line = 'kill -9 ' + strprocesses
    print(line)


def get_adhoctest_lines():
  adhoctest_text = """
root      131747  0.7  0.0      0     0 ?        I    19:13   0:05 [kworker/1:1-events]
user1    132069  0.0  0.8 1183944844 70560 ?    Sl   19:23   0:00
root      131992  0.3  0.0      0     0 ?        D    19:20   0:00 [kworker/u8:5+events_unbound]
 /opt/google/chrome/chrome --type=renderer --enable-crashpad --crashpad-handler-pid=109663 --enable-crash-r
root      132104  0.0  0.0      0     0 ?        I    19:23   0:00 [kworker/0:1-events]
user1    132151  0.0  0.0  11804  3504 pts/3    R+   19:25   0:00 ps aux
root      132105  1.2  0.0      0     0 ?        I    19:23   0:01 [kworker/1:2-events]
  """
  lines = adhoctest_text.split('\n')
  return lines


def is_arg_for_numbers_present():
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-n'):
      return True
  return False


def is_arg_for_kill9_line_present():
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('-k'):
      return True
  return False


def get_args_for_adhoctest_if_present():
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit(0)
    elif arg.startswith('--adhoctest'):
      return get_adhoctest_lines()
  return None


def process():
  lines = get_args_for_adhoctest_if_present()
  as_number = is_arg_for_numbers_present()
  outlist = extract_2nd_words_from_stdin_or_param(lines, as_number)
  output_kill9 = is_arg_for_kill9_line_present()
  gen_output(outlist, output_kill9)


if __name__ == '__main__':
  process()
