#!/usr/bin/env python3
"""
pyVideoCompressWithFfmpg.py

Usage:

$pyVideoCompressWithFfmpg.py --input-dir <source_dirtree_abspath>
   --output-dir <tareget_dirtree_abspath> [--resolution <height:width>]

Where:

  --input-dir is the source dirtree abspath
  --output-dir is the target dirtree abspath
  --resolution is the video-resolution as width and height
    if --resolution is not given, it defaults to 256:144

Beyond 256:144, accepted ones are:
 2) 426x240 | 3) 640x360 | 4) 854x480 | 5) 1280x720

Example Usage
==============

$pyVideoCompressWithFfmpg.py --input-dir "/media/user/disk1/Science/Physics"
   --output-dir "/media/user/disk2/Science/Physics" --resolution <height:width>


Explanation of what this script can do
======================================

This script compresses videos from a directory upwards in a folder tree to
  another directory reflected by its target root directory

  An example of what it can do:

  1) suppose two disks mounted as:
    source root directory: /media/user/disk1
    target root directory: /media/user/disk2

    2) suppose further that one wants to videocompress all files starting from:
      /media/user/disk1/Science/Physics

    2.1) suppose also folder named Physics has the following subfolders:
      /media/user/disk1/Science/Physics/Optics
      /media/user/disk1/Science/Physics/Relativity
      /media/user/disk1/Science/Physics/Quantum

  3) then this script can replicate the above directory structure
     to the target root directory, ie:
    /media/user/disk2/Science/Physics
    /media/user/disk2/Science/Physics/Optics
    /media/user/disk2/Science/Physics/Relativity
    /media/user/disk2/Science/Physics/Quantum

  4) this target directory structure will receive the compressed videos processed

  5) suppose there is the following video in source directory named 'Relativity', say:
      /media/user/disk1/Science/Physics/Relativity/Einstein-01.mp4
    this video will be compressed to the following file:
      /media/user/disk2/Science/Physics/Relativity/Einstein-01.mp4
  Notice:
    5-1 filenames are the same, the compressed one in its equivalent reflected directory
    5-2 if the resolutions of the source video given for compression is higher,
      compression takes place
      (TO-DO: at this version, it's only checking the same resolution
        as the one given in parameter),
    5-3 if a video has the same input resolution,
       processing for the video will not take place and the script goes for the next one.

The Underlying Processing Program
=================================

This script uses the ffmpeg built-in Linux
  (a tweat may be needed for another OS such as macOS or Windows - or perhaps it may work without modification!)

At the time of writing this, the compression is hardcoded to 256x144
    TO-DO: make this compression resolution be changed via a CLI parameter

Usage:
python compress_videos.py --resolution 320:180 --input_dir my_videos/
    --output_dir output_compressed/

"""
import datetime
import os
import subprocess
import os
import subprocess
import argparse
import logging
import time
# Configure logging (move the hardcoded folderpaths later to somewhere else - a kind of configfile)
log_folder = '/home/friend/bin/logs'
log_filename = f"{time.strftime('%Y-%m-%d_%H-%M-%S')} video compression errors.log"
log_file_abspath = os.path.join(log_folder, log_filename)
logging.basicConfig(filename=log_filename,
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
DEFAULT_RESOLUTION_WIDTH_HEIGHT = (256, 144)  # 256:144
DEFAULT_COMPRESSABLE_DOT_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]
ACCEPTED_RESOLUTIONS = [(256, 144), (426, 240), (640, 360), (854, 480), (1280, 720)]

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--resolution", type=str, default="256:144", help="Target resolution (e.g., 256:144)")
parser.add_argument("--input_dir", type=str, default="videos/", help="Directory to process videos from")
parser.add_argument("--output_dir", type=str, default="compressed_videos/", help="Directory to save compressed videos")
args = parser.parse_args()


def extract_width_n_height_from_cli_resolution_arg(p_args):
  """
  Extract target width and height from CLI argument
  Used named p_args for argument, because the IDE notices it as a shadow name
    (i.e., there is a variable called 'args' in the program scope below)

  The name of the CLI argument is 'resolution' (if it's changed, it should be updated here)

  :param p_args: the CLI argument object
  :return resolution_tuple: a double (2-tuple) consisting of target_width, target_height
  """
  try:
    target_width, target_height = map(int, p_args.resolution.split(":"))
    resolution_tuple = target_width, target_height
    if resolution_tuple not in ACCEPTED_RESOLUTIONS:
      scrmsg = f"Resolution format not in list {ACCEPTED_RESOLUTIONS}, plase retry."
      print(scrmsg)
      exit(1)
    return resolution_tuple
  except AttributeError:
    return DEFAULT_RESOLUTION_WIDTH_HEIGHT
  except ValueError:
    scrmsg = "Invalid resolution format. Please use WIDTH:HEIGHT (e.g., 256:144)."
    print(scrmsg)
    exit(1)
  # no returning from here, this last line is unreachable (IDE confirmed!)


# Function to get video resolution
def get_actual_video_resolution_of(video_path):
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

  compressable_dot_extensions = DEFAULT_COMPRESSABLE_DOT_EXTENSIONS

  def __init__(self, srctree_abspath, trgtree_abspath, resolution_tuple):
    self.srctree_abspath = srctree_abspath
    self.trgtree_abspath = trgtree_abspath
    self.resolution_tuple = resolution_tuple
    self.treat_params()
    self.src_currdir_abspath = None
    self.n_dir_passing = 0
    self.n_file_passing = 0
    self.n_videos_processed = 0
    self.n_videos_skipped = 0
    self.n_files_existing_in_trg = 0
    self.n_files_not_existing_in_src = 0
    self.n_errors_compressing = 0
    self.n_dir_effected = 0
    self.n_file_compressed = 0
    self.n_dirs_for_compression = 0
    self.n_files_for_compression = 0
    self.begin_time = datetime.datetime.now()
    self.end_time = None

  def treat_params(self):
    if not os.path.isdir(self.srctree_abspath):
      errmsg = f"Error: source dirtree path {self.srctree_abspath} does not exist."
      raise ValueError(errmsg)
    if self.resolution_tuple not in ACCEPTED_RESOLUTIONS:
      errmsg = (f"Error: In VideoCompress init() resolution {self.resolution_tuple} is not in list"
                f" {ACCEPTED_RESOLUTIONS}")
      raise ValueError(errmsg)

  @property
  def resolution_with_colon(self):
    return f"{self.target_width}:{self.target_height}"

  @property
  def target_width(self):
    return self.resolution_tuple[0]

  @property
  def target_height(self):
    return self.resolution_tuple[1]

  @property
  def relative_working_dirpath(self):
    """
    The relative path is the path beyond srctree_abspath
      and is given by a 'subtraction' so to say, i.e.,
        relative_dirpath = src_currdir_abspath[len(srctree_abspath): ]

    relative path can then be used to form the target directory
      that receives the compressed video
    :return _relative_working_dirpath: the relative path as an object's (dynamical) property
    """
    _relative_working_dirpath = self.src_currdir_abspath[len(self.srctree_abspath):]
    # relative_working_dirpath should not begin with /
    if _relative_working_dirpath.startswith('/'):
      _relative_working_dirpath = _relative_working_dirpath.lstrip('/')
    return _relative_working_dirpath

  @property
  def trg_currdir_abspath(self) -> os.path:
    """
    if the target folder does not exist, create it

    Here are the steps to derive trg_currdir_abspath:
      1) the first interactive variable received from os.walk()
         contains the ongoing abspath
      2) subtracting the srcrootdir from it, one gets the
         relative ongoing dirpath
      3) adding the relative path to trgrootdir, one gets the
         absolute ongoing dirpath
    """
    try:
      _trg_currdir_abspath = os.path.join(self.trgtree_abspath, self.relative_working_dirpath)
    except (OSError, ValueError) as e:
      errmsg = f"In the method that derives the relative working path => {e}"
      raise OSError(errmsg)
    if os.path.isfile(_trg_currdir_abspath):
      errmsg = f"Name {_trg_currdir_abspath} exists as file, program aborting at this point."
      raise OSError(errmsg)
    os.makedirs(_trg_currdir_abspath, exist_ok=True)
    return _trg_currdir_abspath

  def get_curr_output_file_abspath(self, filename: str):
    """
    To get the curr_output_file_abspath,
      add the filename to self.trg_currdir_abspath

    Notice that, by design, the output file must be
      in the same relative path as the input file

    Example:
      a) suppose the following context with directories and files:
        src_abspath = '/media/user/disk1'
        trg_abspath = '/media/user/disk2'
        relativepath = '/sciences/physics/quantum_phys'
        filename = 'quantum_gravity.pdf'

      b) joining the "pieces" of this example, the abspath for the input file is:
        scr_file_abspath = '/media/user/disk1/sciences/physics/quantum_phys/quantum_gravity.pdf'

      b) joining the "pieces" of this example, the abspath for the output file is:
        trg_file_abspath = '/media/user/disk2/sciences/physics/quantum_phys/quantum_gravity.pdf'

      Notice that the only difference is in the root dir-abspath-part,
        relative-path and filename are the same
    """
    curr_output_file_abspath = os.path.join(self.trg_currdir_abspath, filename)
    return curr_output_file_abspath

  def get_curr_input_file_abspath(self, filename):
    """
    @see docstring above for get_curr_output_file_abspath()
    """
    return os.path.join(self.src_currdir_abspath, filename)

  def show_final_report(self):
    self.end_time = datetime.datetime.now()
    elapsed_time = self.end_time - self.begin_time
    scrmsg = f"""Report after videocompressing
    =========================================
    srctree_abspath = {self.srctree_abspath}
    trgtree_abspath = {self.trgtree_abspath}
    n_videos_processed = {self.n_videos_processed}
    n_dirs_for_processing = {self.n_dirs_for_compression}
    n_files_for_compression = {self.n_files_for_compression}
    n_errors_compressing = {self.n_errors_compressing}
    n_videos_skipped = {self.n_videos_skipped}
    begin_time = {self.begin_time}
    end_time = {self.end_time}
    elapsed_time = {elapsed_time}
    """
    print(scrmsg)

  def process_command(self, filename):
    input_file_abspath = self.get_curr_input_file_abspath(filename)
    if not os.path.isfile(input_file_abspath):
      self.n_files_not_existing_in_src += 1
      numbering = f"{self.n_files_not_existing_in_src} / {self.n_file_passing} / {self.n_files_for_compression}"
      scrmsg = f'{numbering} file {input_file_abspath} does not exist. Returing.'
      print(scrmsg)
      return 0
    output_file_abspath = self.get_curr_output_file_abspath(filename)
    if os.path.isfile(output_file_abspath):
      self.n_files_existing_in_trg += 1
      numbering = f"{self.n_files_existing_in_trg} / {self.n_file_passing} / {self.n_files_for_compression}"
      scrmsg = f'{numbering} file [{output_file_abspath}] already exists. Not processing, returing.'
      print(scrmsg)
      return 0
    # FFmpeg command to resize and compress
    cmd = [
      "ffmpeg", "-i", input_file_abspath,
      "-vf", f"scale={self.resolution_with_colon}",
      "-c:v", "libx264", "-crf", "28",
      "-preset", "fast",
      "-c:a", "aac", "-b:a", "64k",
      output_file_abspath
    ]
    # Execute the command
    try:
      scrmsg = '-'*40
      print(scrmsg)
      scrmsg = (f"{self.n_file_passing} | proc {self.n_videos_processed} | total {self.n_files_for_compression}"
                f" filename {filename}")
      print(scrmsg)
      scrmsg = f"In folder {self.src_currdir_abspath}"
      print(scrmsg)
      scrmsg = '-'*40
      print(scrmsg)
      subprocess.run(cmd, check=True)
      self.n_videos_processed += 1
      print(f"{self.n_videos_processed} / {self.n_file_passing} / {self.n_files_for_compression}"
            f" successfully compressed: {filename} -> {self.resolution_with_colon}")
      return 1
    except subprocess.CalledProcessError:
      self.n_errors_compressing += 1
      strline = "-"*35
      print(strline)
      logging.error(strline)
      errmsg = (f"Error compressing: {self.n_errors_compressing} / {self.n_file_passing}"
                f" / {self.n_files_for_compression}")
      print(errmsg)
      logging.error(errmsg)
      errmsg = f"\tError compressing file/video: [{filename}]"
      print(errmsg)
      logging.error(errmsg)
      errmsg = f"\tIn directory [{self.src_currdir_abspath}]"
      print(errmsg)
      logging.error(errmsg)
      strline = "-"*35
      print(strline)
      return 0

  def process_folder(self, files):
    for filename in files:
      self.n_file_passing += 1
      if filename.endswith(tuple(self.compressable_dot_extensions)):
        input_file_abspath = self.get_curr_input_file_abspath(filename)
        # Check video resolution
        width, height = get_actual_video_resolution_of(input_file_abspath)
        if width == self.target_width and height == self.target_height:
          self.n_videos_skipped += 1
          print(f"{self.n_videos_skipped} / {self.n_file_passing} skipping {filename}"
                f" (already {self.resolution_with_colon})")
          continue
        self.process_command(filename)

  def process_in_oswalk(self):
    self.n_file_passing = 0
    for self.src_currdir_abspath, _, files in os.walk(self.srctree_abspath):
      self.n_dir_passing += 1
      scrmsg = (f"Dir {self.n_dir_passing} of {self.n_dirs_for_compression} "
                f"processing videos in [{self.src_currdir_abspath}]")
      print(scrmsg)
      self.process_folder(files)
    print(f"{self.n_videos_processed} videos processed in {self.n_dirs} directories")

  def confirm_videoprocessing_with_the_counting(self):
    scrmsg = f""" *** Confirmation needed
    Confirm the videocompressing with the following counts:
      source root dir = {self.srctree_abspath}
      target root dir = {self.trgtree_abspath}
      target extensions = {self.compressable_dot_extensions}
      n_files_for_compression = {self.n_files_for_compression}
      n_dirs_to_process = {self.n_dirs_for_compression}
    -----------------------
    [Y/n] ? [ENTER] means Yes
    """
    ans = input(scrmsg)
    if ans in ['Y', 'y', '']:
      return True
    return False

  def count_grouped_files_under_video_extensions(self, files):
    n_files_for_compression = 0
    for filename in files:
      if filename.endswith(tuple(self.compressable_dot_extensions)):
        n_files_for_compression += 1
        scrmsg = f"{n_files_for_compression} counting, {self.n_files_for_compression} counted"
        print(scrmsg)
        scrmsg = f"{filename} in [{self.src_currdir_abspath}]"
        print(scrmsg)
    return n_files_for_compression

  def precount_dirs_n_files(self):
    print("Precounting dirs & files for videocompressing")
    print(f"looking and counting those with extensions: {self.compressable_dot_extensions}")
    self.n_dirs_for_compression = 0
    self.n_files_for_compression = 0
    for self.src_currdir_abspath, _, files in os.walk(self.srctree_abspath):
      n_files = self.count_grouped_files_under_video_extensions(files)
      if n_files > 0:
        self.n_dirs_for_compression += 1
        self.n_files_for_compression += n_files

  def process(self):
    """
    Process videos in all directories using os.walk()

    Class process chain:
      1) before start processing, count all directories & files eligible for videocompressing
        1-1 so that, on starting each videofile compression,
            a screen message will inform n_processed / n_iterated / total
        1-2 the triple mentioned above is:
            n_process is number of videos compressed
            n_iterated is number of files looped over
            total is the total number of eligible files (videos having the target file-extensions)
      2) confirm/allow starting of videocompressing with the numbers counted above
        i.e., the user wants to proceed with the numbers collected?
      3) process videocompressing
        video compression is done by the underlying ffmpeg OS tool (so it must be available)
      4) output final processing report
    """
    self.precount_dirs_n_files()
    if not self.confirm_videoprocessing_with_the_counting():
      return False
    self.process_in_oswalk()
    self.show_final_report()
    return True


def get_cli_args():
  """
  # Ensure the output directory exists
  :return: srctree_abspath, trgtree_abspath, resolution_tuple
  """
  srctree_abspath = args.input_dir
  trgtree_abspath = args.output_dir
  resolution_tuple = extract_width_n_height_from_cli_resolution_arg(args)
  return srctree_abspath, trgtree_abspath, resolution_tuple


def confirm_cli_args_with_user():
  srctree_abspath, trgtree_abspath, resolution_tuple = get_cli_args()
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
  print('='*20)
  scrmsg = f"Source directory = [{srctree_abspath}]"
  print(scrmsg)
  scrmsg = f"Target directory = [{trgtree_abspath}]"
  print(scrmsg)
  scrmsg = f"Resolution = [{resolution_tuple}]"
  print(scrmsg)
  print('='*20)
  scrmsg = "The parameters are okay? (Y/n) [ENTER] means Yes "
  ans = input(scrmsg)
  print('='*20)
  confirmed = False
  if ans in ['Y', 'y', '']:
    confirmed = True
  return confirmed, srctree_abspath, trgtree_abspath, resolution_tuple


def adhoc_test1():
  srctree_abspath = args.input_dir
  trgtree_abspath = args.output_dir
  print('srctree_abspath', srctree_abspath)
  print('trgtree_abspath', trgtree_abspath)
  for ongoing, dirs, files in os.walk(srctree_abspath):
    print('ongoing', ongoing)
    relpath = ongoing[len(srctree_abspath):]
    print('relpath', relpath)
    print('dirs', dirs)
    print('files', files[:2])


def process():
  confirmed, srctree_abspath, trgtree_abspath, resolution_tuple = confirm_cli_args_with_user()
  if confirmed:
    vcompressor = VideoCompressor(srctree_abspath, trgtree_abspath, resolution_tuple)
    vcompressor.process()
    return True
  logging.shutdown()
  return False


if __name__ == '__main__':
  """
  adhoc_test1()
  """
  process()
