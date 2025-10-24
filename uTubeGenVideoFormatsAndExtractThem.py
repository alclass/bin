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

class Director:
  this_scr_filepath = __file__
  this_scr_filename = os.path.split(this_scr_filepath)[1]
  targetapp_rootpath = Path(bls.PYMIRROAPP_PATH)
  # relpath_to_foward_script = 'cmm/yt'
  # venv_bin_relpath = 'venv/bin'
  # trgscript = root_targetpath / relpath_to_foward_script / this_script_name
  # trgscript_relpath = relpath_to_foward_script + '/' + this_script_name
  # venvs_pyexecutable_path = root_targetpath / venv_bin_relpath / 'python'
  # venvs_pyexecutable_relpath = 'venv/bin/python'
  venv_sourcing_comm = 'source venv/bin/python'
  
  script_args = sys.argv[1:]


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
  print('chdir to', root_targetpath)
  os.chdir(root_targetpath)
  curdir = os.curdir
  ap = os.path.abspath(curdir)
  sourcecomm = 'source venv/bin/activate'
  # subprocess.run([])
  os.system(sourcecomm)
  print('curdir', ap)
  # cmd = [str(venvs_pyexecutable_relpath), str(trgscript_relpath)] + script_args
  cmd = [str(trgscript_relpath)] + script_args
  print('cmd', cmd)
  os.system(str(trgscript_relpath))


def later():
  try:
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)
  except FileNotFoundError:
    errmsg = f"Error: Python interpreter not found at {root_targetpath}"
    print(errmsg)
    sys.exit(1)

def way3():
  import subprocess

  # Define the multiline script
  bash_script = f"""
  #!/bin/bash
  echo "Starting multiline script..."
  chdir "{}"
  
  ls -l
  echo "Script finished."
  """

  try:
    # Execute the script.
    # `shell=True` is used to execute the command through the shell.
    # `capture_output=True` captures stdout and stderr.
    # `text=True` decodes stdout and stderr as text.
    result = subprocess.run(
      bash_script,
      shell=True,
      capture_output=True,
      text=True,
      check=True  # Raise an exception for non-zero exit codes
    )

    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

  except subprocess.CalledProcessError as e:
    print(f"Error executing script: {e}")
    print(f"STDOUT: {e.stdout}")
    print(f"STDERR: {e.stderr}")


if __name__ == "__main__":
  """
  adhoctest1()
  """
  dispatch_to_its_env()
