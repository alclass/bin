#!/usr/bin/env python3
"""
This scripts reads a text file with youtube-ids and queues the ids up for downloading.
The downloading is undertaken by the open source software dl-youtube Python's version
  and each download is issued by an OS standard system call (os.system(command)) without pipes.

This script, in folder ~/bin, acts like a broker to call its homonimous (same name) counterpart
  in the uTubeOurApps app. (It instantiates its main class, like an API call, to run its tasks.)

Because of the option mentioned above -- and also because of the warnings PyCharm show --
  and also because the library import depends on a config-variable (the app's installed path)
the importing occurs inside a try-block (see code below for these details).

Notice that the app's installed path (*) is kept in the git repo,
  so every Linux box should have the app installed in the same directory.
  (It's easy to change this rigidity by moving this config-var to local_settings.py
  which should not be kept in repo, for giving it the chance to store local config.)

  (*) The uTubeOurApps app has its installed directory path stored in:
    => installed_apps_dirs.UTUBEAPP_PATH
    as mentioned above, this path should be fix for every installation in Linux,
    though an easy modification may make it flexible,
"""
import sys
import installed_apps_dirs as installed  # local Python (bin) settings
try:
  from uTubeOurApps.shellclients.dlYouTubeWithIdsOnTxtFile import VideoidsGrabberAndDownloader
except ImportError:
  def warning_msg(f):
    print('Library VideoidsGrabberAndDownloader not found. Please revise [installed_apps_dirs.py] :', f)
  VideoidsGrabberAndDownloader = warning_msg
  sys.path.insert(0, installed.UTUBEAPP_PATH)


def process():
  youtubeids_filename = None
  try:
    youtubeids_filename = sys.argv[1]
  except IndexError:
    pass
  VideoidsGrabberAndDownloader(youtubeids_filename)  


if __name__ == '__main__':
  process()
