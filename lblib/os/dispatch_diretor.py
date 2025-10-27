#!/usr/bin/env python3
"""
~/bin/lblib/os/dispatch_diretor.py

  The dispatcher class that models relaying-executing to a destination script elsewhere.
  The two first clients are:
    1 - ~bin/uTubeGenVideoFormatsAndExtractThem.py
    2 - ~/bin/dlYouTubeWhenThereAreDubbed.py

"""
from pathlib import Path
import subprocess
import sys
import bin_local_settings as bls


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

  def __init__(self, fromfile, midpath_to_trg_scr, targetapp_rootpath, current_dir):
    self.this_scr_filepath = Path(fromfile)
    self.midpath_to_trg_scr = midpath_to_trg_scr
    self.targetapp_rootpath = Path(targetapp_rootpath)
    self.workingdir_abspath = Path(current_dir)
    self.script_args: list = sys.argv[1:]  # element-0 is the script's name itself
    if '--dirpath' not in self.script_args:
      self.add_currentpath_to_scriptargs()

  def add_currentpath_to_scriptargs(self):
    if '--dirpath' not in self.script_args:
      # some scripts must find out from which dir execution happens
      self.script_args.append('--dirpath')
      current_dirpath = Path(self.workingdir_abspath)
      self.script_args.append(str(current_dirpath))

  @property
  def this_scr_filename(self):
    return self.this_scr_filepath.name

  @property
  def destination_script_abspath(self):
    filepath = self.targetapp_rootpath / self.midpath_to_trg_scr / self.this_scr_filename
    if not filepath.exists():
      errmsg = f"Error: destination script does not exist as {filepath}"
      raise OSError(errmsg)
      # another option to raising an exception
      # print(f"Error: destination_script_abspath not found in {cls.destination_script_abspath}")
      # sys.exit(1)
    return filepath

  def dispatch_to_destination_script(self):
    dest_scr_fp = str(self.destination_script_abspath)
    cmd = [dest_scr_fp] + self.script_args
    # print(f'Args {cls.script_args}')
    print(f'cmd {cmd}')
    # print('  :: dispatch to command =>', cmd)
    try:
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
