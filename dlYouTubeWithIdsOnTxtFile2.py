#!/usr/bin/env python3
"""
dlYouTubeWithIdsOnTxtFile2.py

This scripts:
1) reads a list of ytids
2) looks up each one if it's also inside a sqlite repo
3) the ones that are not inside the database are queued up for download

Another process must be previously run in order to store all present ytid's into its sqlite repo.
The purpose is to avoid redownloading an already-downloaded youtube video.
"""
import sys
from bin_local_settings import PYMIRROAPP_PATH
sys.path.insert(0, PYMIRROAPP_PATH)
from commands import dlYouTubeWithIdsOnTxtFile2


def adhoctest1():
  pass


def process():
  # adhoctest1()
  dlYouTubeWithIdsOnTxtFile2.process(sys.argv)


if __name__ == '__main__':
  process()
