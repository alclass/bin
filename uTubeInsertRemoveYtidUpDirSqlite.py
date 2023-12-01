#!/usr/bin/env python3
"""
uTubeInsertRemoveYtidUpDirSqlite.py

(notice that dlYouTubeWithIdsOnTxtFile3.py does the same but using a different approach)

This scripts is a sort of caller-dispatcher
  ie it links to an application installed elsewhere (the elsewhere-app)
  and calls its process() function passing sys.argv from here

* In an organization note, the PyCharm IDE complains about the "remote" variables,
  for the IDE does not found them "abroad" (it seems not to be looking into the __all__ list_.

The original (elsewhere-app) script does the following:
1) reads a list of ytids (from default filename 'youtube-ids.txt' (its name is configured)
2) looks up for each ytid its inclusion in a sqlite table (in a db configured)
3) those ytids not stored in the sqlite-db will become the set for downloading

In a nut shell:
  The main purpose is not to download a formally downloaded video.
  The purpose is to avoid redownloading an already-downloaded youtube video.

Notice also that the elsewhere-app does the storing of downloaded videos with its ytids.

-------------------
The code below was not essential to this script
  (because it dynamically imports the elsewhere app)
except ImportError:
  # ModuleNotFoundError
  print('Error: module', __all__, 'not found: see directory path for finding the app.')
  sys.exit(1)

"""
import sys
from bin_local_settings import PYMIRROAPP_PATH  # this is the name of the variable in import module
# as of 2023 it's been convention-named 'DirTreeMirror_PrdPrjSw' but could be anyname anywhere in path
approot = PYMIRROAPP_PATH
sys.path.insert(0, approot)  # this inserts the app's absolute path to "PYTHONPATH"
# __all__ = [approot, 'dlYouTubeWithIdsOnTxtFile2']
# print(sys.path)
# from DirTreeMirror_PrdPrjSw.commands import uTubeInsertRemoveYtidUpDirSqlite as ins_missing_in_db
# the "calling" commands are located (convention) in package named 'commands'
from eval(approot + '.commands') import uTubeInsertRemoveYtidUpDirSqlite as ins_missing_in_db


def dispatch():
    return ins_missing_in_db.process(sys.argv)


def adhoctest1():
  pass


def process():
  # adhoctest1()
  return dispatch()


if __name__ == '__main__':
  process()
