#!/usr/bin/env python3
"""
/home/friend/bin/unzipEachToFolder.py
    Unzips all zipfiles in the current (executing) directory
"""
import glob
import os


def unzip():
  total_unzipped = 0
  zips = glob.glob('*.zip')
  for i, zipfilename in enumerate(zips):
    name, ext = os.path.split(zipfilename)
    foldername = name
    if os.path.isdir(foldername):
      # the unzipped contents go to a samename directory
      # if it already exists, don't unzip and move on
      continue
    comm_str = f'unzip "{zipfilename}" -d "{foldername}"'
    seq = i + 1
    scrmsg = f"{seq} unzipping [{zipfilename}] curr_n={total_unzipped}"
    print(scrmsg)
    ret_value = os.system(comm_str)
    if ret_value == 0:
      total_unzipped += 1
  scrmsg = f"Total unzipped:' {total_unzipped}, '| Total no. of zip files:', {len(zips)}"
  print(scrmsg)


def process():
  unzip()


if __name__ == '__main__':
  process()
