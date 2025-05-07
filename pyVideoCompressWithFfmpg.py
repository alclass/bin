#!/usr/bin/env python3
"""
pyVideoCompressWithFfmpg.py

This script compresses videos in a directory
  it can, with a small tweat, be encompassed within a dirwalk to process videos through a directory tree,
    ie, it may process a whole file system bottomup [suffice it make a caller with os.walk()]

It uses the ffmpeg built-in Linux
  (a tweat may be needed for another OS such as MacOS or Windows - or perhaps it may work without modification!)

At the time of writing this, the compression is hardcoded to 256x144
    TO-DO: make this compression resolution be changed via a CLI parameter

Usage:
python compress_videos.py --resolution 320:180 --input_dir my_videos/
    --output_dir output_compressed/

"""
import os
import subprocess
import os
import subprocess
import argparse
DEFAULT_RESOLUTION_WIDTH_HEIGHT = (256, 144)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--resolution", type=str, default="256:144", help="Target resolution (e.g., 256:144)")
parser.add_argument("--input_dir", type=str, default="videos/", help="Directory to process videos from")
parser.add_argument("--output_dir", type=str, default="compressed_videos/", help="Directory to save compressed videos")
args = parser.parse_args()


def extract_width_n_height_from_cli_resolution_arg(args):
  # Extract target width and height from CLI argument
  try:
    target_width, target_height = map(int, args.resolution.split(":"))
    resolution_tuple = target_width, target_height
    return resolution_tuple
  except AttributeError:
    return DEFAULT_RESOLUTION_WIDTH_HEIGHT
  except ValueError:
    print("Invalid resolution format. Please use WIDTH:HEIGHT (e.g., 256:144).")
    exit(1)
  # no returning from here, this last line is unreachable (IDE confirmed!)


# Function to get video resolution
def get_video_resolution(video_path):
  cmd = [
    "ffprobe", "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=width,height",
    "-of", "csv=p=0", video_path
  ]
  try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    width, height = map(int, result.stdout.strip().split(","))
    return width, height
  except Exception as e:
    print(f"Error checking resolution for {video_path}: {e}")
  return None, None


class VideoCompressor:

  dot_extensions = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]

  def __init__(self, srctree_abspath, trgtree_abspath, resolution_tuple):
    self.srctree_abspath = srctree_abspath
    self.trgtree_abspath = trgtree_abspath
    self.resolution_tuple = resolution_tuple
    self.currdir_abspath = None

  @property
  def trg_currdir_abspath(self):
    """
    OBS: correct relative ongoing/working current folder
    """
    treepiece_relpath = self.trg_currdir_abspath[len(self.srctree_abspath):]
    _trg_currdir_abspath = self.trgtree_abspath + '/' + treepiece_relpath
    return _trg_currdir_abspath

  @property
  def curr_output_file_abspath(self):
    """
    OBS: correct relative ongoing/working current folder
    """
    treepiece_relpath = self.curr_input_file_abspath[len(self.srctree_abspath):]
    _curr_output_file_abspath = self.trgtree_abspath + '/' + treepiece_relpath
    return _curr_output_file_abspath

  @property
  def resolution_with_colon(self):
    return f"{self.resolution_tuple[0]}:{self.resolution_tuple[1]}"

  def process_command(self, input_path):
    # FFmpeg command to resize and compress
    cmd = [
      "ffmpeg", "-i", curr_input_file_abspath,
      "-vf", f"scale={self.resolution_with_colon}",
      "-c:v", "libx264", "-crf", "28",
      "-preset", "fast",
      "-c:a", "aac", "-b:a", "64k",
      self.curr_output_file_abspath
    ]
    # Execute the command
    try:
      subprocess.run(cmd, check=True)
      print(f"Successfully compressed: {filename} -> {args.resolution}")
    except subprocess.CalledProcessError:
      print(f"Error compressing: {filename}")

  def process_folder(self, files):
    for filename in files:
      if filename.endswith(tuple(self.dot_extensions)):  # Add more formats if needed
        input_path = os.path.join(self.currdir_abspath, filename)
        output_path = os.path.join(args.output_dir, f"compressed_{filename}")
        # Check video resolution
        width, height = get_video_resolution(input_path)
        if width == target_width and height == target_height:
          print(f"Skipping {filename} (Already {args.resolution})")
          continue
        self.process_command()

  def process(self):
    """
    Process videos in all directories using os.walk()
    """
    for self.currdir_abspath, _, files in os.walk(args.input_dir):
      self.process_folder(files)
    print("All videos processed!")


def get_args():
  """
  # Ensure the output directory exists
  os.makedirs(args.output_dir, exist_ok=True)

  :return:
  """
  srctree_abspath = args.input_dir
  trgtree_abspath = args.output_dir
  # target_width, target_height = map(int, args.resolution.split(":"))
  resolution_tuple = extract_width_n_height_from_cli_resolution_arg(args)
  return srctree_abspath, trgtree_abspath, resolution_tuple


def process():
  srctree_abspath, trgtree_abspath, resolution_tuple = get_args()
  print(srctree_abspath, trgtree_abspath, resolution_tuple)
  if not os.path.isdir(srctree_abspath):
    scrmsg = "Source directory [{srctree_abspath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  if not os.path.isdir(trgtree_abspath):
    scrmsg = "Target directory [{trgtree_abspath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  print('Paramters')
  scrmsg = f"Source directory = [{srctree_abspath}]"
  print(scrmsg)
  scrmsg = f"Target directory = [{trgtree_abspath}]"
  print(scrmsg)
  scrmsg = f"Resolution = [{resolution_tuple}]"
  print(scrmsg)
  scrmsg = "The parameters are okay? (Y/n) [ENTER] means Yes "
  ans = input(scrmsg)
  if ans not in ['Y', 'y', '']:
    return False
  vcompressor = VideoCompressor()
  vcompressor.process()
  return True


if __name__ == '__main__':
  process()
