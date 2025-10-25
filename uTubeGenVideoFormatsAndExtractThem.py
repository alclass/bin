#!/usr/bin/env python3
"""
~bin/uTubeGenVideoFormatsAndExtractThem.py
  This is a dispatcher script relaying executing to:
    /home/dados/Sw3/PrdPrjSw/DirTreeMirror_PrdPrjSw/cmm/yt/uTubeGenVideoFormatsAndExtractThem.py

This destination script was written under a virtual-env, but it itself does not have
  dependencies on its local site-packages. Because of that, relaying just need to execute it
  and send it its CLI-parameters.

However, this destination script does need the local imports in its app. Because of this,
  it adds (manually) the root-app-dir into sys.path (@see it there).

Just as a reminder for the future, the json idea below will be carried on
  for the rename-scripts (*) strategy in the future.
    import json
    CONFIG_FILE = Path.home() / ".dispatcher_config.json"

 (*) the rename-scripts are about 20 in number and they might be executed, instead of one for each one,
   by a command subcommand strategy. For example:
   1 - the renameCleanBegining.py <params> might become:
     => rendsp cleanBeginning <params>
   2 - the renameReplace12.py <params> might become:
     => rendsp replace12 <params>

"""
import sys
import subprocess
from pathlib import Path
import bin_local_settings as bls
import lblib.os.dispatch_diretor as dd


class Director:
  """
  These two following lines are only necessary if the app has a local site-packages dependency
    (which is not the case for this script, its dependency is inward in the app itself)
    (this 'inward' dependency is solved by a sys.insert in the destination script)
  ----------------------------------------------
  relpath_to_venv_bin_python = 'venv/bin/python'
  python_comm_abspath = targetapp_rootpath / relpath_to_venv_bin_python

  Another point of attention is that 'source' does not work with system-callers
    (whether it's os.system() or subprocess.run())
  # venv_sourcing_comm = 'source venv/bin/python'

  """
  this_scr_filepath = Path(__file__)
  # the destination script has the same name
  this_scr_filename = this_scr_filepath.name  # os.path.split(this_scr_filepath)[1]
  targetapp_rootpath = Path(bls.PYMIRROAPP_PATH)
  midpath_to_trg_scr = 'cmm/yt'
  destination_script_abspath = targetapp_rootpath / midpath_to_trg_scr / this_scr_filename
  script_args: list = sys.argv[1:]  # element-0 is the script's name itself

  @classmethod
  def dispatch_to_destination_script(cls):
    if not cls.destination_script_abspath.is_file():
      print(f"Error: destination_script_abspath not found in {cls.destination_script_abspath}")
      sys.exit(1)
    try:
      dest_scr_fp = str(cls.destination_script_abspath)
      cmd = [dest_scr_fp] + cls.script_args
      # print(f'Args {cls.script_args}')
      # print(f'cmd {cmd}')
      # print('  :: dispatch to command =>', cmd)
      result = subprocess.run(
        cmd,  # =cmd,
        check=True,
        # shell=True, # if shell is set to True, CLI-parameters are not passed on
        capture_output=True,
        text=True,
      )
      # Execute the script.
      # `shell=True` is used to execute the command through the shell.
      # `capture_output=True` captures stdout and stderr.
      # `text=True` decodes stdout and stderr as text.
      print("STDOUT:")
      print(result.stdout)
      print("STDERR:")
      print(result.stderr or "\tNo errors in STDERR.")

    except subprocess.CalledProcessError as e:
      print(f"Error executing script: {e}")
      print(f"STDOUT: {e.stdout}")
      print(f"STDERR: {e.stderr}")
      sys.exit(e.returncode)


def process():
  Director.dispatch_to_destination_script()


def dispatch():
  fromfile = __file__
  midpath_to_trg_scr = 'cmm/yt'
  targetapp_rootpath = bls.PYMIRROAPP_PATH
  # dispatcher instantiates Director
  dispatcher = dd.Director(
    fromfile=fromfile,
    midpath_to_trg_scr=midpath_to_trg_scr,
    targetapp_rootpath=targetapp_rootpath
  )
  dispatcher.dispatch_to_destination_script()


if __name__ == "__main__":
  """
  adhoctest1()
  """
  dispatch()
