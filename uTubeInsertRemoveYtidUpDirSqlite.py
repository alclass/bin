#!/usr/bin/env python3
"""
~/bin/uTubeInsertRemoveYtidUpDirSqlite.py
  A dispatcher to the same named script in the DirTree codebase.

(Notice that similar named dlYouTubeWithIdsOnTxtFile3.py does the same, but uses a different approach.)

This script is a sort of caller-dispatcher:
  a) i.e., it links to an application installed elsewhere (the elsewhere-app)
  b) and calls its process() (via if __name__) function passing sys.argv from here
  c) in the future (a TODO), this app may be included within PYTHONPATH
     from where the app may be called directly, obsoleting this dispatcher

* As an organizational note, the PyCharm IDE complains about the "remote" variables,
  for the IDE does not found them "abroad" (it seems not to be looking into the __all__ list_).

The original (elsewhere-app) script does the following:
1) reads a list of ytids (from default filename 'youtube-ids.txt' (its name is configured);
2) for each ytid, if not in db, insert it into a sqlite table (in a db-configured sqlitefile);
3) those ytids not stored in the sqlite-db will form the to-download set;

In a nut-shell:
  The main purpose is to avoid to download a previously (and kept) downloaded video.

Notice also that the elsewhere-app does the storing of downloaded videos with its ytids.

-------------------
The code below was not essential to this script
  (because it dynamically imports the elsewhere-app)
except ImportError:
  # ModuleNotFoundError
  print('Error: module', __all__, 'not found: see directory path for finding the app.')
  sys.exit(1)


Notice about the config variable PYMIRROAPP_PATH:

  The following config variable [PYMIRROAPP_PATH] has been 'conventioned' here,
    though its appname itself has been changed from time to time.

So attention must be taken on the corresponding path set in bin_local_settings.py
The value set there is not in git repo, ie app may be installed anywhere in the os-dirtree
and the user must place its basefolderpath there.

  Another solution is to install the app to a PYTHONPATH path (a TODO).
"""
import sys
from bin_local_settings import PYMIRROAPP_PATH
appsrootpath = PYMIRROAPP_PATH
sys.path.insert(1, appsrootpath)
from commands import uTubeInsertRemoveYtidUpDirSqlite as insertMissingInDb


def dispatch():
    return insertMissingInDb.process(sys.argv)


def adhoctest1():
  pass


def process():
  # adhoctest1()
  return dispatch()


if __name__ == '__main__':
  process()
