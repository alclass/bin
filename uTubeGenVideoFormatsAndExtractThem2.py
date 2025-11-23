#!/usr/bin/env python3
"""
~bin/uTubeGenVideoFormatsAndExtractThem.py

import os
"""
import sys
import subprocess
from pathlib import Path
import json
import bin_local_settings as bls
CONFIG_FILE = Path.home() / ".dispatcher_config.json"
pass


def load_config():
  """Load configuration from file or use defaults"""
  default_config = {
    "base_path": str(Path.home() / "my_scripts"),
    "scripts_dir": "scripts"
  }

  if CONFIG_FILE.exists():
    try:
      with open(CONFIG_FILE, 'r') as f:
        user_config = json.load(f)
        default_config.update(user_config)
    except json.JSONDecodeError:
      print(f"Warning: Invalid config file {CONFIG_FILE}, using defaults")
  return default_config


def main():
  if len(sys.argv) < 2:
    print("Usage: dispatcher <script_name> [args...]")
    print("Available scripts in target directory:")
    list_available_scripts()
    sys.exit(1)
  config = load_config()
  target_script = sys.argv[1]
  script_args = sys.argv[2:]
  base_path = Path(config["base_path"])
  scripts_dir = base_path / config["scripts_dir"]
  venv_path = base_path / "venv"
  python_path = venv_path / "bin" / "python"
  # Auto-detect script extension
  script_paths = [
    scripts_dir / target_script,
    scripts_dir / f"{target_script}.py",
    scripts_dir / f"{target_script}.sh"  # in case you have shell scripts too
  ]
  target_script_path = None
  for path in script_paths:
    if path.exists():
      target_script_path = path
      break
  if not target_script_path:
    errmsg = f"Error: Script '{target_script}' not found in {scripts_dir}"
    print(errmsg)
    list_available_scripts(scripts_dir)
    sys.exit(1)

  if not venv_path.exists():
    print(f"Error: Virtual environment not found at {venv_path}")
    sys.exit(1)

  # Build and execute command
  cmd = [str(python_path), str(target_script_path)] + script_args

  try:
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)
  except FileNotFoundError:
    errmsg = f"Error: Python interpreter not found at {python_path}"
    print(errmsg)
    sys.exit(1)


def list_available_scripts(scripts_dir=None):
  """List available scripts in the scripts directory"""
  if not scripts_dir:
    config = load_config()
    scripts_dir = Path(config["base_path"]) / config["scripts_dir"]

  if scripts_dir.exists():
    for script_file in scripts_dir.iterdir():
      if script_file.is_file() and script_file.suffix in ['.py', '.sh']:
        print(f"  - {script_file.stem}")


if __name__ == "__main__":
  """
  process()
  """
  main()
