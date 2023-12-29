#!/usr/bin/env python3
"""
unzipEachToFolder.py
  unzips each zipfile in the current folder.

Upgraded script from Python2 to Python3 on 2023-12-25
  (with the oportunity of maching only having Python3...)
"""
import glob
import os


def unzip_all_files_in_dir():
  zips = glob.glob('*.zip')
  n_of_unzipped = 0
  for ezip in zips:
    folder = ezip[:-4]
    if os.path.isdir(folder):
      continue
    scrmsg = f"{n_of_unzipped+1} unzipping file [{ezip}]"
    print(scrmsg)
    comm = f'unzip "{ezip}" -d "{folder}"'
    retval = os.system(comm)
    if retval == 0:
      n_of_unzipped += 1
  scrmsg = f"Total unzipped: {n_of_unzipped} ||| Total n. of zip files: {len(zips)}"
  print(scrmsg)


def process():
  unzip_all_files_in_dir()


if __name__ == "__main__":
  process()
