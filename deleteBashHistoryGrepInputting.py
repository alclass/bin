#!/usr/bin/env python3
"""
~/bin/deleteBashHistoryGrepInputting.py

OBS: THIS script is not yet working because 'history'
     doesn't run via os.system(), so a solution is still needed

The idea here is the following:

1) suppose one wishes to delete from bash'es history all line like:
   "shutdown now"
   (this is somewhat dangerous when using the UP-key to retrieve CL history)

2) it can be done with the following 'pipe':
   $ history | grep "shutdown now" | deleteBashHistoryGrepInputting.py

"""
import os
import sys
import time


class BashHistoryDeleter:

  def __init__(self, lines):
    self.lines = lines
    self.numbers = []

  def delete_line_by_number(self, linenumber: int):
    comm = f"history -d {linenumber}"
    print(comm)
    os.system(comm)

  def delete_lines(self):
    """
    It's necessary to have numbers list decrescently ordered
    Because if deletes start at the smallest number,
      the subsequent ones will change
    """
    self.numbers.sort()
    self.numbers.reverse()
    print('to delete bashline numbers', self.numbers)

    for linenumber in self.numbers:
      self.delete_line_by_number(linenumber)

  def extract_lines(self):
    for line in self.lines:
      print('line', line)
      try:
        pp = line.split(" ")
        pp = list(filter(lambda line: line != "", pp))
        strnumber = pp[0]
        strnumber = strnumber.strip(' \t')
        number = int(strnumber)
        self.numbers.append(number)
        print('to delete bashline number', number)
      except ValueError:
        continue

  def process(self):
    print('processing')
    self.extract_lines()
    self.delete_lines()


def process():
  lines = sys.stdin
  deleter = BashHistoryDeleter(lines)
  deleter.process()


if __name__ == '__main__':
  process()
