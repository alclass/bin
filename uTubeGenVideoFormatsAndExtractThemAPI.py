#!/usr/bin/env python3
"""
~bin/uTubeGenVideoFormatsAndExtractThemAPI.py
  This is a dispatcher script relaying executing to:
    /home/dados/Sw3/PrdPrjSw/DirTreeMirror_PrdPrjSw/cmm/yt/uTubeGenVideoFormatsAndExtractThem.py

  The different from its counterpart named:
~bin/uTubeGenVideoFormatsAndExtractThem.py

  is that it connects to the destination script via its API
  instead of relying on subprocess.run()

  (@see docstr of destination script for more info)

"""
import sys
from pathlib import Path
import bin_local_settings as bls
targetapp_rootpath = Path(bls.PYMIRROAPP_PATH)
print('insert into path', targetapp_rootpath)
# remember to cast PosixPath to str on sys.path.inserting
sys.path.insert(0, str(targetapp_rootpath))
print(sys.path)
import cmm.yt.uTubeGenVideoFormatsAndExtractThem as extract_mod


def dispatch():
  # sys.argv will go along to 'destination'
  extract_mod.process()


if __name__ == "__main__":
  """
  adhoctest1()
  """
  dispatch()
