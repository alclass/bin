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

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--resolution", type=str, default="256:144", help="Target resolution (e.g., 256:144)")
parser.add_argument("--input_dir", type=str, default="videos/", help="Directory to process videos from")
parser.add_argument("--output_dir", type=str, default="compressed_videos/", help="Directory to save compressed videos")
args = parser.parse_args()

# Ensure the output directory exists
os.makedirs(args.output_dir, exist_ok=True)


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


def process():
  # Extract target width and height from CLI argument
  try:
    target_width, target_height = map(int, args.resolution.split(":"))
  except ValueError:
    print("Invalid resolution format. Please use WIDTH:HEIGHT (e.g., 256:144).")
    exit(1)

  # Process videos in all directories using os.walk()
  for root, _, files in os.walk(args.input_dir):
    for filename in files:
      if filename.endswith((".mp4", ".mkv", ".avi", ".mov", ".wmv")):  # Add more formats if needed
        input_path = os.path.join(root, filename)
        output_path = os.path.join(args.output_dir, f"compressed_{filename}")
        # Check video resolution
        width, height = get_video_resolution(input_path)
        if width == target_width and height == target_height:
          print(f"Skipping {filename} (Already {args.resolution})")
          continue
        # FFmpeg command to resize and compress
        cmd = [
          "ffmpeg", "-i", input_path,
          "-vf", f"scale={args.resolution}",
          "-c:v", "libx264", "-crf", "28",
          "-preset", "fast",
          "-c:a", "aac", "-b:a", "64k",
          output_path
        ]
        # Execute the command
        try:
          subprocess.run(cmd, check=True)
          print(f"Successfully compressed: {filename} -> {args.resolution}")
        except subprocess.CalledProcessError:
          print(f"Error compressing: {filename}")

  print("All videos processed!")


if __name__ == '__main__':
    process()
