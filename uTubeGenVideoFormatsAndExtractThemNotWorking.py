#!/usr/bin/env python3
"""
~bin/uTubeGenVideoFormatsAndExtractThem.py

"""
import subprocess
import sys
import os
import bin_local_settings as bls
# --- Configuration ---
# 1. Path to the virtual environment directory (the parent of 'bin' or 'Scripts')
#    Replace this with the actual absolute path to your virtual environment.
VENV_DIR = bls.PYMIRROAPP_PATH  # "/path/to/your/virtualenv"
# 2. Name of the target script you want to run within the venv.
#    This script should be executable (e.g., have a shebang and be mode +x).
TARGET_SCRIPT_NAME = __file__


# --- Logic ---
def main():
  """
  Constructs the command to run the target script inside the venv and executes it.
  """
  # Determine the path to the Python interpreter inside the virtual environment.
  # This path might be slightly different on Windows (e.g., VENV_DIR/Scripts/python.exe)
  # On Linux/macOS:
  if sys.platform.startswith('win'):
    # Windows example (adjust as needed)
    python_executable = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
  else:
    # Linux/macOS example
    python_executable = os.path.join(VENV_DIR, 'venv', 'bin', 'python')

  # Full path to the target script
  target_script_path = os.path.join(os.path.dirname(__file__), TARGET_SCRIPT_NAME)
  # 1. Start the command with the venv's Python interpreter
  command = [python_executable]
  # 2. Add the target script
  command.append(target_script_path)
  # 3. Append all arguments passed to the dispatcher script
  #    sys.argv[0] is the dispatcher's name, so we slice from [1:]
  command.extend(sys.argv[1:])

  try:
    # Use subprocess.run to execute the command.
    # check=True will raise an error if the script returns a non-zero exit code.
    # The output of the target script will be streamed to the current terminal.
    result = subprocess.run(command, check=True, stdout=sys.stdout, stderr=sys.stderr)
    sys.exit(result.returncode) # Exit with the target script's exit code
  except FileNotFoundError:
    print(f"Error: Virtual environment interpreter not found at {python_executable}", file=sys.stderr)
    sys.exit(1)
  except subprocess.CalledProcessError as e:
    # This catches errors if the TARGET_SCRIPT_NAME script itself fails
    print(f"Error: Target script failed with exit code {e.returncode}", file=sys.stderr)
    sys.exit(e.returncode)
  except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  """
  process()
  """
  main()
