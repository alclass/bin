#!/usr/bin/env python3
"""

"""


def cut_after_idx(idx, p_queue):
  """
  """
  scrmsg = f"cut_after_idx idx={idx} on {p_queue}"
  print(scrmsg)
  while idx < len(p_queue) - 1:
    _ = p_queue.pop()
  scrmsg = f"result {p_queue}"
  print(scrmsg)


def adhoctest1():
  queue = list(range(10))
  cut_after_idx(5, queue)
  queue = ['2']
  cut_after_idx(5, queue)


if __name__ == '__main__':
  """
  adhoc_test2()
  process()
  """
  adhoctest1()

