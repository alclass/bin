#!/usr/bin/env python3
import glob, json, os, string, subprocess, sys #, shutil, sys

DEFAULT_EXTENSION = 'mp4'

def print_explanation_and_exit():
  print('''
  Script's function:
  ==================

  This script tries to find the duration of media files in a folder 
  and puts this duration in-between the first and second word of its name.
  
  Example:
  
  Suppose current folder has the following file:
  "This video is about Physics.mp4"
  
  Supposing it has 11 minutes duration, the script will rename it to:
  "This 11' video is about Physics.mp4"
  ie, it puts a ((11')) (an eleven [one one] and a plics)
      in-between "This" and "video".
    
  Arguments to the script:
  =======================

  -e=<file-extension> (if not given, default is %s [do not use the dot '.' before extension])
  -y avoids confirmation, ie, it does the renaming without asking a confirm Yes or No
  -h or --help prints this help message
''') %DEFAULT_EXTENSION
  sys.exit(0)

def probe_n_return_json(vid_file_path):
  '''

    NOT YET WORKING TO THE PROBABLY THE BYTES/STRING PROBLEM FROM THE PIPE-FFPROBE
    Give a json from ffprobe command line
    @vid_file_path : The absolute (full) path of the video file, string.

      This function was copied from the one in StackOverflow at:
        https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python

  '''
  if not os.path.isfile(vid_file_path):
    raise Exception('Give ffprobe a full file path of the video')

  command = ["ffprobe",
    "-loglevel",  "quiet",
    "-print_format", "json",
    "-show_format",
    "-show_streams",
    vid_file_path
  ]

  pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  out, err = pipe.communicate()
  # print(out, err)
  # sys.exit(0)
  return json.loads(out)

def transform_duration_from_sec_to_min(duration_in_sec):
  return int(round(float(duration_in_sec) / 60, 0))

def get_duration_in_sec(json_as_dict):
  '''
  :param json_as_dict:
  :return:

  The approach here will be as follows:
  1) first, try to find the duration key inside json_as_dict['streams']
  2) if the above attempt fails, then try to find the duration key inside json_as_dict['format']
  3) if both above fails, then exit(1) with error "duration not found"

  Chances to improve this routine:
  1) try to find a way to introspect the whole json_as_dict,
    so that it would look up the duration key wherever it has a chance to be
  2) if the above is implementable,
    that would guarantee "duration not found"
    in case duration is really missing
  '''
  try:
    # 1st try: look up duration key from dict inside key 'streams', second element from list
    dict_that_has_duration = json_as_dict['streams'][1]
    duration_in_sec = dict_that_has_duration['duration']
    # got it, so return it right away
    # (but how will we know whether or not this exception is always thrown
    # and code might be refactored to leave only the 2nd try below?)
    return duration_in_sec
  except (IndexError, KeyError) as e:
    pass
  try:
    # 2nd try: look up duration key from dict inside key 'format'
    dict_that_has_duration = json_as_dict['format']
    duration_in_sec = dict_that_has_duration['duration']
  except (IndexError, KeyError) as e:
    print (json_as_dict)
    print ("Couldn't find duration key, program cannot continue.")
    sys.exit(1)
  return duration_in_sec

def get_duration_str(fil): #
  json = probe_n_return_json(fil)
  duration_in_sec = get_duration_in_sec(json)
  duration_in_min = transform_duration_from_sec_to_min(duration_in_sec)
  if duration_in_min <= 60:
	# Notice that output is dd' where dd is value in minutes (eg. 59' or 7')
    duration_str = str(duration_in_min) + "'"
  else:
	# Notice that output is 1hdd where dd is value in minutes (eg. 1h59 or 1h07)
    duration_in_hours = duration_in_min // 60
    remainder = duration_in_min - (duration_in_hours*60)
    duration_str = str(duration_in_hours) + 'h' + str(remainder).zfill(2)
  return duration_str

# args = ['-e='] # -e is file extension
class Args:
  '''

  '''
  def __init__(self):
    self.ext = None
    self.confirm_before_rename = True
    self.process_cli_args()
    self.check_if_at_least_ext_was_set()

  def process_cli_args(self):
    for arg in sys.argv:
      if arg in ['-h', '--help']:
        print_explanation_and_exit()
      if arg.startswith('-y'):
        self.confirm_before_rename = False
      if arg.startswith('-e='):
          self.ext = arg[len('-e=') : ]

  def check_if_at_least_ext_was_set(self):
    if self.ext == None:
      self.ext = DEFAULT_EXTENSION

  def get_ext_with_period(self):
    return '.%s' %self.ext

  def get_extension(self):
    if self.ext is None:
      return DEFAULT_EXTENSION
    return self.ext

class Rename:

  def __init__(self, args):
    '''

    :param confirm_before_rename:
    '''
    self.extension             = args.get_extension()
    self.confirm_before_rename = args.confirm_before_rename
    # self.abspath = os.path.dirname(os.path.abspath(__file__))
    self.abspath = os.getcwd()
    self.rename_pairs = []
    self.processRenames()

  def processRenames(self):
    '''

    :param self:
    :return:
    '''
    self.findRenames()
    self.showRenames()
    doRename = False
    if self.confirm_before_rename:
      doRename = self.confirmRenames()
    else:
      doRename = True
    if doRename:
      self.renamePairs()

  def findRenames(self):
    '''

    :return:
    '''
    files = glob.glob('*.' + self.extension)
    files.sort()
    for filename in files:
      name, ext = os.path.splitext(filename)
      if ext is None or ext == '':
        continue
      words = filename.split(' ')
      if len(words) < 2:
        continue
      fileabspath = os.path.join(self.abspath, filename)
      duration_str = get_duration_str(fileabspath)  # probe_n_return_json
      # if (duration_str) exists in source filename, do not buffer it to rename_pairs tuple list
      if duration_str == words[1]:
        continue
      newName = words[0] + ' ' + duration_str + " " + ' '.join(words[1:])
      rename_tuple = ( filename, newName )
      self.rename_pairs.append(rename_tuple)

  def showRenames(self):
    '''

    :return:
    '''
    for i, rename_pair in enumerate(self.rename_pairs):
      filename, newName = rename_pair
      print(i+1, ' ======== Rename Pair ========')
      print('FROM: >>>' + filename)
      print('TO:   >>>' + newName)
    if len(self.rename_pairs) == 0:
      print(
''' *** No files are renameable. ***
    ==>>> Either:
    1) no files with renaming extension (%s) in folder;
    2) namesizes are too short or
    3) files already have the duration mark.      
''' %self.extension )


  def confirmRenames(self):
    '''

    :return:
    '''
    n_renames = len(self.rename_pairs)
    if n_renames > 0:
      msg_for_input = 'Are you sure to  rename these (%d) files? (Y/n) ' %n_renames
      ans = input(msg_for_input)
      if ans in ['n','N']:
        return False
    return True

  def renamePairs(self):
    '''

    :return:
    '''
    nOfRenames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      filename, newName = rename_pair
      os.rename(filename, newName)
      nOfRenames += 1
    print('Total files renamed: %d' %nOfRenames)

def process():
  args = Args()
  Rename(args)

if __name__ == '__main__':
  process()
  # unittest.main()
