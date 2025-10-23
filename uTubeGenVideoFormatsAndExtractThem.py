#!/usr/bin/env python3
"""
~bin/uTubeGenVideoFormatsAndExtractThem.py

/home/dados/Sw3/PrdPrjSw/DirTreeMirror_PrdPrjSw/cmm/yt/uTubeGenVideoFormatsAndExtractThem.py
/home/dados/Sw3/PrdPrjSw/DirTreeMirror_PrdPrjSw/cmm/yt/uTubeGenVideoFormatsAndExtractThem.py
/home/dados/Sw3/PrdPrjSw/DirTreeMirror_PrdPrjSw
/home/friend/bin/uTubeGenVideoFormatsAndExtractThem.py

cmm/yt/uTubeGenVideoFormatsAndExtractThem.py


import json
CONFIG_FILE = Path.home() / ".dispatcher_config.json"
"""
import os
import sys
import subprocess
from pathlib import Path
import bin_local_settings as bls
this_script_path = __file__
this_script_name = os.path.split(this_script_path)[1]
root_targetpath = bls.PYMIRROAPP_PATH
root_targetpath = Path(root_targetpath)
relpath_to_foward_script = 'cmm/yt'
venv_bin_relpath = 'venv/bin'
trgscript = root_targetpath / relpath_to_foward_script / this_script_name
trgscript_relpath = relpath_to_foward_script + '/' + this_script_name
venvs_pyexecutable_path = root_targetpath / venv_bin_relpath / 'python'
venvs_pyexecutable_relpath = venv_bin_relpath + '/python'
script_args = sys.argv[1:]
pass


def dispatch_to_its_env():
  if not venvs_pyexecutable_path.exists():
    print(f"Error: Virtual environment not found at {venvs_pyexecutable_path}")
    sys.exit(1)
  if not trgscript.exists():
    print(f"Error: Virtual environment not found at {trgscript}")
    sys.exit(1)
  # Build and execute command
  # sys.path.insert(0, root_targetpath)
  _ = root_targetpath
  os.chdir(root_targetpath)
  curdir = os.curdir
  ap = os.path.abspath(curdir)
  subprocess.run(['venv'])
  print(ap)
  cmd = [str(venvs_pyexecutable_relpath), str(trgscript_relpath)] + script_args
  try:
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)
  except FileNotFoundError:
    errmsg = f"Error: Python interpreter not found at {python_path}"
    print(errmsg)
    sys.exit(1)


if __name__ == "__main__":
  """
  adhoctest1()
  """
  dispatch_to_its_env()
