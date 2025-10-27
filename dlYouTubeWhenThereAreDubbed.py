#!/usr/bin/env python3
"""
~/bin/dlYouTubeWhenThereAreDubbed.py

  This is a dispatcher script relaying execution to the same named script in another app
    somewhere else (in another folder, @see variable targetapp_rootpath below).

This destination script is under a virtual-env, but it itself does not have
  dependencies on its local site-packages. Because of that, relaying just need to execute it
  and send it its CLI-parameters (*).

  (*) There is a trick in the destination script for it being capable of
      getting its local imports (@see it there).
"""
from pathlib import Path
import bin_local_settings as bls
import lblib.os.dispatch_diretor as dd


def dispatch():
  fromfile = __file__
  midpath_to_trg_scr = 'cmm/yt'
  targetapp_rootpath = bls.PYMIRROAPP_PATH
  # dispatcher instantiates Director
  dispatcher = dd.Director(
    fromfile=fromfile,
    midpath_to_trg_scr=midpath_to_trg_scr,
    targetapp_rootpath=targetapp_rootpath,
    # --dirpath picks up the current working directory because this changes after dispatching
    current_dir=Path('.').absolute()
  )
  dispatcher.dispatch_to_destination_script()


if __name__ == "__main__":
  """
  adhoctest1()
  """
  dispatch()
