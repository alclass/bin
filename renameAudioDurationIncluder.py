#!/usr/bin/env python2
import glob, json, os, string, subprocess, sys #, shutil, sys

def print_explanation_and_exit():
  print('Arguments to the script:')
  print('-e=<file-extension> (required)')
  sys.exit(0)

def probe_n_return_json(vid_file_path):
  '''

    NOT YET WORKING TO THE PROBABLY THE BYTES/STRING PROBLEM FROM THE PIPE-FFPROBE
    Give a json from ffprobe command line
    @vid_file_path : The absolute (full) path of the video file, string.

      This function was copied from the one in StackOverflow at:
        https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
  '''
  if os.path.isfile(vid_file_path):
    vid_file_path = str(vid_file_path)
  if type(vid_file_path) != str:
    raise Exception('Give ffprobe a full file path of the video')
    return

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
  return json.loads(str(out))

def transform_duration_from_sec_to_min(duration_in_sec):
  return int(round(float(duration_in_sec) / 60, 0))

def get_duration_str(fil): # 
  json = probe_n_return_json(fil)
  the_streams_key_dict = json['streams'][1]
  duration_in_sec = the_streams_key_dict['duration']
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
  def __init__(self):
    self.ext = None
    self.process_cli_args()
    self.check_if_at_least_ext_was_set()

  def process_cli_args(self):
    for arg in sys.argv:
      if arg.startswith('-e='):
        self.ext = arg[len('-e=') : ]

  def check_if_at_least_ext_was_set(self):
    if self.ext == None:
      print_explanation_and_exit()

  def get_ext_with_period(self):
    return '.%s' %self.ext

def rename(args):        
  files=os.listdir('.')
  files.sort()
  for i in range(0,2):
    c=0
    for fil in files:
      name, ext = os.path.splitext(fil)
      # print 'name, ext', name, ext
      tamNameWithoutExt = len(name)
      if ext != None:
        if ext != args.get_ext_with_period():
          continue
      words = fil.split(' ')
      if len(words) < 2:
        continue
      duration_str = get_duration_str(fil) # probe_n_return_json
      newName = words[0] + ' ' + duration_str + " " + ' '.join(words[1:])
		
      c += 1
      print( c, ' ======== Rename Pair ========' )
      print( 'FROM: >>>' + fil )
      print( 'TO:   >>>' + newName )
      if i==1:
        os.rename(fil, newName)
    if c==0:
      print( 'No files are sized above position', posFrom )
      break
    if i==0 and c > 0:
      ans = raw_input('Are you sure? (y/n) ')
      if ans != 'y':
        break

def process():
  args = Args()
  rename(args)

if __name__ == '__main__':
  process()
  # unittest.main()
