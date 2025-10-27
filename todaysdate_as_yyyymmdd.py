#!/usr/bin/env python3
"""
~/bin/todaysdate_as_yyyymmdd.py

  This script does the following:

    1 executes todaysdate_as_yyyymmdd.sh
    2 receives its output (a date in format yyyy-mm-dd)
    3 prints it to stout
    4 copies it to the system's clipboard
"""
import pyperclip
import subprocess


def gen_todaysdate_n_add_it_to_linuxs_clipboard():
  """

  """
  cmm_str = 'todaysdate_as_yyyymmdd.sh'
  cmm = [cmm_str]
  print('running subprocess', cmm)
  result = subprocess.run(
    args=cmm,
    check=True,
    capture_output=True,
    text=True
  )
  pdate = result.stdout
  # clean up trailing NEWLINE (\n)
  pdate = pdate.strip('\n')
  # copies it to the system's clipboard (like a Ctrl+C)
  pyperclip.copy(pdate)
  scrmsg = f'{pdate} | also copied to the clipboard'
  print(scrmsg)


def process():
  gen_todaysdate_n_add_it_to_linuxs_clipboard()


if __name__ == "__main__":
  """
  adhoctest1()
  """
  process()

