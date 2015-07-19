#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
'''
import  codecs, os, sys
class InputParameterError(Exception):
  pass


def process_filter_in_even_lines(filename):
  lines = codecs.open(filename,'r', 'utf-8')
  output_text = ''
  for i, line in enumerate(lines):
    line_n = i+1
    if line_n % 2 == 0:
      output_text += line
  return output_text

def process_print_out_even_lines(filename):
  output_text = process_filter_in_even_lines(filename)
  print output_text

def process():
  try:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
      raise InputParameterError, 'A valid input parameter is the filename of an existing file on folder.'
  except IndexError:
    raise InputParameterError, 'A valid input parameter is the filename of an existing file on folder.'
  except InputParameterError, msg:
    print msg
    exit(-1)
  process_print_out_even_lines(filename)

if __name__ == '__main__':
  process()
