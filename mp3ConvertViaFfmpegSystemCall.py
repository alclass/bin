#!/usr/bin/env python3
"""
~/bin/mp3ConvertViaFfmpegSystemCall.py

Examples:

python3 mp3_converter.py -b 64k -r 22050 -i video.mp4
python3 mp3_converter.py -b 128k -r 44100 -i ./media_folder -o ./converted_mp3

"""
import argparse
import os
import subprocess
import sys

# Valid bitrate/sample rate combinations (basic sanity check)
VALID_COMBINATIONS = {
    "32k": [22050],
    "64k": [22050, 44100],
    "128k": [44100],
    "192k": [44100],
    "256k": [44100],
    "320k": [44100]
}


def check_combination(bitrate, samplerate):
  if bitrate not in VALID_COMBINATIONS or samplerate not in VALID_COMBINATIONS[bitrate]:
    sys.exit(f"Error: Bitrate {bitrate} and sample rate {samplerate} Hz is not a valid combination.")


def convert_to_mp3(input_file, output_dir, bitrate, samplerate):
  filename = os.path.splitext(os.path.basename(input_file))[0] + ".mp3"
  output_file = os.path.join(output_dir, filename)

  cmd = [
      "ffmpeg",
      "-i", input_file,
      "-vn",  # no video
      "-ar", str(samplerate),
      "-ab", bitrate,
      "-f", "mp3",
      output_file
  ]

  print(f"Converting {input_file} -> {output_file}")
  subprocess.run(cmd, check=True)


def main():
  parser = argparse.ArgumentParser(description="Extract and convert audio to MP3 from media files.")
  parser.add_argument("-b", "--bitrate", required=True, help="MP3 bitrate (e.g., 32k, 64k, 128k)")
  parser.add_argument("-r", "--samplerate", type=int, required=True, help="MP3 sample rate (e.g., 22050, 44100)")
  parser.add_argument("-i", "--input", required=True, help="Input file or folder")
  parser.add_argument("-o", "--output", default="output_mp3", help="Output folder")

  args = parser.parse_args()

  # Validate bitrate/sample rate
  check_combination(args.bitrate, args.samplerate)

  # Ensure output folder exists
  os.makedirs(args.output, exist_ok=True)

  # Process input
  if os.path.isdir(args.input):
    files = [os.path.join(args.input, f) for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input, f))]
  else:
    files = [args.input]

  for f in files:
    try:
      convert_to_mp3(f, args.output, args.bitrate, args.samplerate)
    except subprocess.CalledProcessError:
      print(f"Failed to convert {f}")


if __name__ == "__main__":
  main()
