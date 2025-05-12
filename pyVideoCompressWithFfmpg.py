#!/usr/bin/env python3
"""
pyVideoCompressWithFfmpg.py

Usage:
=========

$pyVideoCompressWithFfmpg.py --input-dir <source_dirtree_abspath>
   --output-dir <tareget_dirtree_abspath> [--resolution <height:width>]

Where:

  --input-dir is the source dirtree abspath
  --output-dir is the target dirtree abspath
  --resolution is the video-resolution as width and height
    if --resolution is not given, it defaults to 256:144

Accepted resolution pairs:
===========================

  Beyond
    1) 256:144, accepted ones are:
    2) 426:240 | 3) 640:360 | 4) 854:480 | 5) 1280:720
    (it's a hardcoded list in here, TODO move this list to a configfile)

Example Usage
==============

$pyVideoCompressWithFfmpg.py --input-dir "/media/user/disk1/Science/Physics"
   --output-dir "/media/user/disk2/Science/Physics" --resolution 426:240


Explanation of what this script does mainly
======================================

This script compresses videos from a directory upwards in a folder tree to
  another directory reflected by its target root directory

  An example:

  1) suppose two disks mounted as:
    source root directory: /media/user/disk1
    target root directory: /media/user/disk2
    *  it doesn't exclusively need to be mounted dirtrees,
       it could be any subdirectory in the OS's filesystem

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

  4) this target directory structure will receive the compressed/processed videos

  5) to see that, suppose there is the following (source) video in source directory named 'Relativity', say:
      /media/user/disk1/Science/Physics/Relativity/Einstein-01.mp4
    this video will be compressed to the following (target) file:
      /media/user/disk2/Science/Physics/Relativity/Einstein-01.mp4
  Notice:
    5-1 filenames (in source & target) are the same,
      ie, the original and the compressed one in its equivalent reflected directory
    5-2 if the resolutions of the source video given for compression is higher,
      compression takes place
      (TODO at this version, it's only checking the resolution
        and not exactly comparing lower or higher doubles [width:height],
        so a scheme to find it out could be implemented later on),
    5-3 if a video has the same input resolution,
       processing for the video will not take place and a simple copy over will be tried.

The OS-Underlying Processing Program
====================================

This script uses the ffmpeg Linux built-in tool
  (a tweat may be needed for another OS such as macOS or Windows - or perhaps
   it may just work out of the box without any modification!)

At the time of writing this, the compression double hardcode-defaults to 256x144
    TODO move this default compression resolution to a configfile
"""
import argparse
import datetime
import logging
import os
import shutil
import subprocess
import sys
import time
from pandas import timedelta_range

DEFAULT_RESOLUTION_WIDTH_HEIGHT = (256, 144)  # 256:144
DEFAULT_COMPRESSABLE_DOT_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]
ACCEPTED_RESOLUTIONS = [(256, 144), (426, 240), (640, 360), (854, 480), (1280, 720)]
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compress videos to a specified resolution.")
parser.add_argument("--input_dir", type=str, default="videos/",
                    help="Directory to process videos from")
parser.add_argument("--output_dir", type=str, default="compressed_videos/",
                    help="Directory to save compressed videos")
parser.add_argument("--resolution", type=str, default="256:144",
                    help="Target resolution (e.g., 256:144)")
args = parser.parse_args()


def get_triple_elapsed_avg_n_now_inbetween_compressions(begin_time, n_passing, timemark):
  """
  Returns a triple with:
    elapsed: the duration of last compression
    average: average duration for all previous compressions
    now: the actual time marking "compress frontiers"
  :return: elapsed, average, now
  """
  now = datetime.datetime.now()
  elapsed = now - timemark
  # assigning now to compress_marktime for "next time coming here"
  if n_passing < 1:
    return 0.0, 0.0, now  # before the first compression, elapsed and average are zero
  if n_passing < 2:
    return elapsed, elapsed, now  # for the first compression, average equals elapsed
  n_compressions = n_passing - 1
  elapsed_uptilnow = now - begin_time
  average = elapsed_uptilnow / n_compressions
  return elapsed, average, now


class Log:
  """
  Defines the logging attributes (main) for errorfile logging
  """
  users_home_dir = os.path.expanduser("~")
  log_folder = f"{users_home_dir}/bin/logs"
  log_filename = f"{time.strftime('%Y-%m-%d_%H-%M-%S')} video compression errors.log"
  log_filepath = os.path.join(log_folder, log_filename)

  @classmethod
  def start_logging(cls):
    """
    Configure logging (TODO move the hardcoded folderpaths later to somewhere else - a kind of configfile)
      at any rate, the current path picks up the user's home directory and adds to it "bin/logs"
    """
    logging.basicConfig(
      filename=cls.log_filepath,
      level=logging.ERROR,
      format='%(asctime)s - %(levelname)s - %(message)s'
    )


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

  def __init__(self, src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple):
    self.src_rootdir_abspath = src_rootdir_abspath  # source root directory (or scrdirtree) abspath
    self.trg_rootdir_abspath = trg_rootdir_abspath  # target root directories (or trgdirtree) abspath
    self.resolution_tuple = resolution_tuple
    self.treat_params()
    self.src_currdir_abspath = None  # its trg equivalent is a class property (i.e., dynamically found)
    self.total_files = 0
    self.n_file_passing = 0  # counts each file coming up via os.walk()
    self.n_video_passing = 0  # counts each file that has the eligible video extensions (mp4, mkv, etc.)
    self.n_dir_passing = 0  # counts each directory coming up via os.walk()
    self.n_videos_processed = 0  # counts video processed
    self.n_videos_skipped = 0  # counts videofiles skipped (either because they were not found or exist in target)
    self.n_videos_copied_over = 0  # counts videos that have already the same target resolution (the copied over)
    self.n_failed_videos_copied_over = 0  # counts failed copies-over
    self.n_files_existing_in_trg = 0  # counts videofiles that exist in target
    self.n_files_not_existing_in_src = 0  # counts videofiles that don't exist in the source (were moved out?)
    self.n_errors_compressing = 0  # counts when exception subprocess. is raised
    self.n_files_for_compression = 0  # counts ffmpeg commands gone to completion
    self.n_dirs_for_compression = 0  # counts total directories that have videos for compression
    self.compress_marktime = datetime.datetime.now()  # marks time at a videocompression, helps in duration averaging
    self.begin_time = datetime.datetime.now()  # it marks script's begintime
    self.end_time = None  # will mark script's endtime at the report calling time

  def treat_params(self):
    if not os.path.isdir(self.src_rootdir_abspath):
      errmsg = f"Error: source dirtree path {self.src_rootdir_abspath} does not exist."
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
    _relative_working_dirpath = self.src_currdir_abspath[len(self.src_rootdir_abspath):]
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
      _trg_currdir_abspath = os.path.join(self.trg_rootdir_abspath, self.relative_working_dirpath)
    except (OSError, ValueError) as e:
      errmsg = f"In the method that derives the relative working path => {e}"
      raise OSError(errmsg)
    if os.path.isfile(_trg_currdir_abspath):
      errmsg = f"Name {_trg_currdir_abspath} exists as file, program aborting at this point."
      raise OSError(errmsg)
    os.makedirs(_trg_currdir_abspath, exist_ok=True)
    return _trg_currdir_abspath

  def get_curr_output_file_abspath(self, filename: str) -> os.path:
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

  def get_curr_input_file_abspath(self, filename) -> os.path:
    """
    @see docstring above for get_curr_output_file_abspath()
    """
    return os.path.join(self.src_currdir_abspath, filename)

  def show_final_report(self):
    self.end_time = datetime.datetime.now()
    elapsed_time = self.end_time - self.begin_time
    scrmsg = f"""Report after videocompressing
    =========================================
    src_rootdir_abspath = {self.src_rootdir_abspath}
    trg_rootdir_abspath = {self.trg_rootdir_abspath}
    error_log_file      = {Log.log_filepath}
    -----------------------------------------
    total dirs visited = {self.n_dir_passing}
    total dirs for processing = {self.n_dirs_for_compression}
    total videos processed = {self.n_videos_processed}
    total files visited = {self.n_file_passing}
    total videos visited = {self.n_video_passing}
    total files = {self.total_files}
    total videos for compression = {self.n_files_for_compression}
    total videos copied over = {self.n_videos_copied_over}
    total failed copied over = {self.n_failed_videos_copied_over}
    total videos skipped = {self.n_videos_skipped}
    total files not existing in src = {self.n_files_not_existing_in_src}
    total files existing in trg = {self.n_files_existing_in_trg}
    total compression errors = {self.n_errors_compressing}
    -----------------------------------------
    begin_time = {self.begin_time}
    end_time = {self.end_time}
    elapsed_time = {elapsed_time}
    """
    print(scrmsg)

  def get_quad_elapsed_avg_now_n_remaining_inbetween_compressions(self):
    """
    Returns a quadruple with:
      elapsed: the duration of last compression
      average: average duration for all previous compressions
      now: the actual time marking "compress frontiers"
      remaining_time: a prediction on how much time to go to complete processing
    :return: elapsed, average, now, remaining
    """
    elapsed, average, now = get_triple_elapsed_avg_n_now_inbetween_compressions(
      self.begin_time,
      self.n_file_passing,
      self.compress_marktime
    )
    self.compress_marktime = now
    # forecasting remaining time
    remaining_videos = self.n_files_for_compression - self.n_videos_processed
    remaining_time = remaining_videos * average
    return elapsed, average, now, remaining_time

  def process_command(self, filename):
    input_file_abspath = self.get_curr_input_file_abspath(filename)
    if not os.path.isfile(input_file_abspath):
      self.n_files_not_existing_in_src += 1
      numbering = (f"src-doesn't-exist={self.n_files_not_existing_in_src} | video={self.n_video_passing}"
                   f" | total={self.n_files_for_compression}")
      scrmsg = f"{numbering} file {input_file_abspath} does not exist. Returing."
      print(scrmsg)
      return False
    output_file_abspath = self.get_curr_output_file_abspath(filename)
    if os.path.isfile(output_file_abspath):
      self.n_files_existing_in_trg += 1
      numbering = (f"trg-exists={self.n_files_existing_in_trg} | video={self.n_video_passing}"
                   f" | total={self.n_files_for_compression}")
      scrmsg = f"{numbering} file [{output_file_abspath}] already exists. Not processing, returing."
      print(scrmsg)
      return False
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
      scrmsg = (f"video={self.n_video_passing} | proc {self.n_videos_processed}"
                f" | total {self.n_files_for_compression}"
                f" filename {filename}")
      print(scrmsg)
      scrmsg = f"\tin folder {self.src_currdir_abspath}"
      print(scrmsg)
      elapsed, average, now, remaining_time = self.get_quad_elapsed_avg_now_n_remaining_inbetween_compressions()
      scrmsg = (f" \t{now} => times: last compression duration: {elapsed} secs"
                f" | average duration until now: {average} secs"
                f" | remaining_time: {remaining_time}")
      print(scrmsg)
      scrmsg = '-'*40
      print(scrmsg)
      subprocess.run(cmd, check=True)
      self.n_videos_processed += 1
      print(f"{self.n_videos_processed} / {self.n_file_passing} / {self.n_files_for_compression}"
            f" successfully compressed: {filename} -> {self.resolution_with_colon}")
      return True
    except subprocess.CalledProcessError:
      # logging and printing the error context
      self.n_errors_compressing += 1
      strline = "-"*35
      print(strline)
      logging.error(strline)
      errmsg = (f"Error compressing: errors: {self.n_errors_compressing} / visited: {self.n_file_passing}"
                f" / total: {self.n_files_for_compression}")
      print(errmsg)
      logging.error(errmsg)
      errmsg = f"\terror compressing file/video: [{filename}]"
      print(errmsg)
      logging.error(errmsg)
      errmsg = f"\tin directory [{self.src_currdir_abspath}]"
      print(errmsg)
      logging.error(errmsg)
      strline = "-"*35
      print(strline)
      return False

  def copy_over_file_to_trg(self, filename):
    input_file_abspath = self.get_curr_input_file_abspath(filename)
    output_file_abspath = self.get_curr_output_file_abspath(filename)
    if not os.path.isfile(input_file_abspath):
      self.n_videos_skipped += 1
      numbering = (f"not-copied={self.n_videos_skipped} | reached={self.n_file_passing}"
                   f" | total={self.n_files_for_compression}")
      print(f"{numbering} | video file does not exist (or was moved out) in source.")
      return False
    if os.path.isfile(output_file_abspath):
      self.n_videos_skipped += 1
      numbering = (f"not-copied={self.n_videos_skipped} | reached={self.n_file_passing}"
                   f" | total={self.n_files_for_compression}")
      print(f"{numbering} | video filename already exists in target.")
      return False
    try:
      shutil.copy2(input_file_abspath, output_file_abspath)
    except (OSError, IOError) as e:
      # logging and printing the error context
      self.n_failed_videos_copied_over += 1
      strline = "-"*35
      print(strline)
      logging.error(strline)
      numbering = (f"failed_copy={self.n_failed_videos_copied_over} | reached={self.n_file_passing}"
                   f" | total={self.n_files_for_compression}")
      errmsg = f"{numbering} | videopath = {input_file_abspath}) \n\tError = {e}"
      logging.error(errmsg)
      print(errmsg)
      return False
    self.n_videos_copied_over += 1
    numbering = (f"copied={self.n_videos_copied_over} | reached={self.n_file_passing}"
                 f" | total={self.n_files_for_compression}")
    scrmsg = f"{numbering} (videos has already {self.resolution_with_colon})"
    print(scrmsg)
    return True

  def process_files_in_folder(self, files):
    for filename in files:
      self.n_file_passing += 1
      if filename.endswith(tuple(self.compressable_dot_extensions)):
        self.n_video_passing += 1
        input_file_abspath = self.get_curr_input_file_abspath(filename)
        # Check video resolution
        width, height = get_actual_video_resolution_of(input_file_abspath)
        if width == self.target_width and height == self.target_height:
          # resolution is already the aimed one, copy videofile over to destination dirtree
          _ = self.copy_over_file_to_trg(filename)  # returns a boolean
          continue
        _ = self.process_command(filename)  # returns a boolean

  def process_in_oswalk(self):
    self.n_file_passing = 0
    for self.src_currdir_abspath, _, files in os.walk(self.src_rootdir_abspath):
      self.n_dir_passing += 1
      n_files_in_dir = len(files)
      scrmsg = (f"Visited dirs {self.n_dir_passing} | total dirs {self.n_dirs_for_compression} "
                f"| processing {n_files_in_dir} videos in [{self.src_currdir_abspath}]")
      print(scrmsg)
      self.process_files_in_folder(files)

  def confirm_videoprocessing_with_the_counting(self):
    scrmsg = f""" =========================
    *** Confirmation needed
    Confirm the videocompressing with the following counts:
      source root dir = {self.src_rootdir_abspath}
      target root dir = {self.trg_rootdir_abspath}
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
      self.total_files += 1
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
    for self.src_currdir_abspath, _, files in os.walk(self.src_rootdir_abspath):
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
  Required parameters:
    src_rootdir_abspath & trg_rootdir_abspath

  Optional parameter:
    resolution_tuple

  :return: srctree_abspath, trg_rootdir_abspath, resolution_tuple
  """
  try:
    if args.h or args.help:
      print(__doc__)
      sys.exit(0)
  except AttributeError:
    pass
  src_rootdir_abspath = args.input_dir
  trg_rootdir_abspath = args.output_dir
  resolution_tuple = extract_width_n_height_from_cli_resolution_arg(args)
  return src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple


def confirm_cli_args_with_user():
  src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple = get_cli_args()
  print(src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple)
  if not os.path.isdir(src_rootdir_abspath):
    scrmsg = "Source directory [{src_rootdir_abspath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  if not os.path.isdir(trg_rootdir_abspath):
    scrmsg = "Target directory [{trg_rootdir_abspath}] does not exist. Please, retry."
    print(scrmsg)
    return False
  print('Paramters')
  print('='*20)
  scrmsg = f"Source directory = [{src_rootdir_abspath}]"
  print(scrmsg)
  scrmsg = f"Target directory = [{trg_rootdir_abspath}]"
  print(scrmsg)
  scrmsg = f"Resolution = [{resolution_tuple}]"
  print(scrmsg)
  scrmsg = f"Error-log file = [{Log.log_filepath}]"
  print(scrmsg)
  print('='*20)
  scrmsg = "The parameters are okay? (Y/n) [ENTER] means Yes "
  ans = input(scrmsg)
  print('='*20)
  confirmed = False
  if ans in ['Y', 'y', '']:
    confirmed = True
  return confirmed, src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple


def adhoc_test2():
  now = datetime.datetime.now()
  begin_time = datetime.datetime.now() - datetime.timedelta(hours=1)
  n_passing = 4
  timemark = now
  elapsed, avg, now = get_triple_elapsed_avg_n_now_inbetween_compressions(begin_time, n_passing, timemark)
  scrmsg = f"elapsed={elapsed}, avg={avg}, now={now}, n_passing={n_passing}, begin={begin_time}"
  print(scrmsg)


def adhoc_test1():
  src_rootdir_abspath = args.input_dir
  trg_rootdir_abspath = args.output_dir
  print('src_rootdir_abspath', src_rootdir_abspath)
  print('trg_rootdir_abspath', trg_rootdir_abspath)
  for ongoing, dirs, files in os.walk(src_rootdir_abspath):
    print('ongoing', ongoing)
    relpath = ongoing[len(src_rootdir_abspath):]
    print('relpath', relpath)
    print('dirs', dirs)
    print('files', files[:2])


def process():
  Log.start_logging()
  confirmed, src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple = confirm_cli_args_with_user()
  if confirmed:
    vcompressor = VideoCompressor(src_rootdir_abspath, trg_rootdir_abspath, resolution_tuple)
    vcompressor.process()
    return True
  logging.shutdown()
  return False


if __name__ == '__main__':
  """
  adhoc_test1()
  adhoc_test2()
  """
  process()
