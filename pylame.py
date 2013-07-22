#!/usr/bin/env python
#-*-coding:utf-8-*-
import glob, os, re, sys

def print_program_usage_and_exit():
  print '''Usage:
  <command> [file numbers]'''
  sys.exit(0)

class DEFAULTS:
  DEFAULT_MIN_FREQ_IN_KBPS = 24
  DEFAULT_FREQ_IN_KBPS     = 32
  DEFAULT_MAX_FREQ_IN_KBPS = 48

def pick_up_freq_in_arg1_or_default_or_print_usage_and_exit():
  try:
    arg1 = sys.argv[1]
    if arg1 in ['-h', '--help']:
      print_program_usage_and_exit()
    freq_in_kbps = int(arg1)
    # acceptableKbps =  [24,32,48,64,96,128]     # if freq_in_kbps not in acceptableKbps:
    if freq_in_kbps < 32:
      # fall back to the min frequency default and return
      return DEFAULTS.DEFAULT_MIN_FREQ_IN_KBPS
    elif freq_in_kbps > 32:
      # fall back to the min frequency default and return
      return DEFAULTS.DEFAULT_MAX_FREQ_IN_KBPS
  except IndexError: # in case, there's no CLI argument, ie, there's no sys.argv[1]
    pass
  except ValueError: # in case, there's a CLI argument, but it's not an int
    pass
  # If not returned above, fall back to the average frequency default and return
  return DEFAULTS.DEFAULT_FREQ_IN_KBPS

def pick_up_all_mp3s_on_localfolder():
  mp3s = glob.glob('*.mp3')
  mp3s = mp3s + glob.glob('*.MP3')
  mp3s = mp3s + glob.glob('*.Mp3')
  mp3s = mp3s + glob.glob('*.mP3')
  return mp3s

class Mp3LameFreqChanger(object):

  # think about how to solve the "--resample" issue
  LAME_COMMAND_BASE = 'lame -b %(freq_in_kbps)d --mp3input -m s --resample 48 "%(input_mp3_filename)s" "%(output_mp3_filename)s"'
  # LAME_COMMAND_BASE = 'lame -b %(freq_in_kbps)d --mp3input -m s "%(input_mp3_filename)s" "%(output_mp3_filename)s"'
  kbps_re_str = '\d+k'
  kbps_re = re.compile(kbps_re_str)
  
  
  def __init__(self, freq_in_kbps):
    self.freq_in_kbps = freq_in_kbps
    self.init_mp3_tuple_list_to_convert_on_localfolder()
    self.confirm_batch_conversion()
    self.batch_convert_one_by_one()

  def does_output_mp3_filename_pass_exclusion_criteria(self, input_name_extensionless, output_mp3_filename):
    if os.path.isfile(output_mp3_filename):
      return False
    name_ending = '.%dk' %(self.freq_in_kbps)
    if input_name_extensionless.endswith(name_ending):
      return False
    # another test on ending
    try:
      pp = input_name_extensionless.split('.')
      kbps_piece = pp[-1]
      if self.kbps_re.match(kbps_piece):
        return False
    except IndexError:
      pass
    return True


  def init_mp3_tuple_list_to_convert_on_localfolder(self):
    self.input_mp3s = pick_up_all_mp3s_on_localfolder()
    self.mp3_tuple_list_to_convert = []
    self.input_mp3s.sort() 
    for input_mp3_filename in self.input_mp3s:
      input_name_extensionless, ext = os.path.splitext(input_mp3_filename)
      output_mp3_filename = '%s.%dk%s' %(input_name_extensionless, self.freq_in_kbps, ext)
      if not self.does_output_mp3_filename_pass_exclusion_criteria(input_name_extensionless, output_mp3_filename):
        continue
      convert_tuple = (input_mp3_filename, output_mp3_filename)
      self.mp3_tuple_list_to_convert.append(convert_tuple)

  def confirm_batch_conversion(self):
    print 'Conversion:'
    print '-'*30
    for i, convert_tuple in enumerate(self.mp3_tuple_list_to_convert):
      print i+1, 'converting:', convert_tuple
    print 'Total:', len(self.mp3_tuple_list_to_convert)
    ans = raw_input(' *** Please, to avoid converting them above, press n or N and [ENTER]. Any other key means [ok] to convert. ***')
    if ans in ['n', 'N']:
      sys.exit(0)

  def batch_convert_one_by_one(self):
    for convert_tuple in self.mp3_tuple_list_to_convert:
      input_mp3_filename, output_mp3_filename = convert_tuple
      dict_for_lame_command_base = {'freq_in_kbps':self.freq_in_kbps, 'input_mp3_filename':input_mp3_filename, 'output_mp3_filename':output_mp3_filename} 
      command = self.LAME_COMMAND_BASE %dict_for_lame_command_base
      retValue = os.system(command)
      print '-'*30
      print 'os.system() returned %d' %retValue
      print '-'*30

def process():
  freq_in_kbps = pick_up_freq_in_arg1_or_default_or_print_usage_and_exit()
  Mp3LameFreqChanger(freq_in_kbps)

if __name__ == '__main__':
  process()
