#!/usr/bin/env python3
"""
    This scripts implements the Karatsuba's Multiplication Algorithm.
    (At this time, it only works for 21 x 13 = 273 (it needs more research).)
"""
import glob, sys


def show_cli_help():
  print(__doc__)


def do_karatsubas_algo(sn1, sn2):
  n1 = int(sn1)
  n2 = int(sn2)
  ld1 = int(sn1[0])
  rd1 = int(sn1[-1])
  ld2 = int(sn2[0])
  rd2 = int(sn2[-1])
  midsum = ld1 + rd1 + ld2 + rd2
  karat_result = str(ld1) + str(midsum) + str(rd2)
  dir_mult_result = n1 * n2
  print("Result via Karatsuba's Algorithm = ", karat_result)
  print("Result via direct multiplication = ", dir_mult_result)


def get_strnumbers_args():
  '''

  '''
  try:
    sn1 = sys.argv[1]
    sn2 = sys.argv[2]
    _ = int(sn1)
    _ = int(sn2)
  except (IndexError, ValueError) as e:
    print(show_cli_help())
    sys.exit(1) 
  return sn1, sn2


def process():
  '''

  '''
  sn1, sn2 = get_strnumbers_args()
  do_karatsubas_algo(sn1, sn2)


if __name__ == '__main__':
  process()
