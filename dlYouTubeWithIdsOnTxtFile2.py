#!/usr/bin/env python3
"""
On 2023-09-20 renamed app root foldername as shown in the constant attribution below:
  PYMIRROAPP_PATH = '/home/dados/Sw3/ProdProjSw/DirTreeMirrorPys_PrdPrj'

dlYouTubeWithIdsOnTxtFile2.py
(notice that dlYouTubeWithIdsOnTxtFile3.py does the same but using a different approach)

This script is a sort of caller-dispatcher
  ie it links to an application installed elsewhere (the 'elsewhere-app')
  and calls its process() function passing sys.argv from here

* In an organizational note, the PyCharm IDE complains about the "remote" variables,
  for the IDE does not found them "abroad";
    it seems not to be looking into the __all__ list_. After-note: we've withdrawn __all__.

The original (elsewhere-app) script does the following:
  1) reads a list of ytids (from default filename 'youtube-ids.txt' (its name is configured)
     (in the original a different one could be given as a cli-parameter);
  2) looks up for each ytid for whether it's included or not in a sqlite table (in a db configured);
  3) those ytids not stored in the sqlite-db will become set (queued up) for downloading;

In a nutshell:
  The main purpose is not to redownload a formally downloaded video.
  ie, avoid redownloading an already-downloaded youtube video.

Notice also that the 'elsewhere-app' does the storing of downloaded videos with based on its ytid's.

-------------------
The code below was not essential to this script
  (because it dynamically imports the elsewhere app)
except ImportError:
  # ModuleNotFoundError
  print('Error: module', __all__, 'not found: see directory path for finding the app.')
  sys.exit(1)

Notice on the config variable PYMIRROAPP_PATH

The following config variable [PYMIRROAPP_PATH] has been 'conventioned'
  here though its appname itself has been changed from time to time.

So attention must be taken on the corresponding path set in bin_local_settings.py
The value set there is not in git repo, ie app may be installed anywhere in the os-dirtree
and the user must place its basefolderpath there.
"""
import sys
from bin_local_settings import PYMIRROAPP_PATH
appsrootpath = PYMIRROAPP_PATH
sys.path.insert(1, appsrootpath)
# 2025-09-17: package named commands was renamed to cmm
from cmm import dlYouTubeWithIdsOnTxtFile2 as d2


def dispatch():
    return d2.process(sys.argv)


def adhoctest1():
  pass


def process():
  # adhoctest1()
  return dispatch()


if __name__ == '__main__':
  process()
