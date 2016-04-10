#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Example:
10 is Italian
40 is Mathew
http://audio.wordproject.com/bibles/app/audio/10_40.zip
7 is French
41 is Mark
http://audio.wordproject.com/bibles/app/audio/7_41.zip

http://audio3.wordproject.com/bibles/app/audio/34_40.zip

Exceptions:
For Greek and Latin, examples:
  http://www.wordproaudio.com/audio_lists/gk/40_mat.zip etc
  http://www.wordproaudio.com/audio_lists/vg/40_mat.zip etc


'''
import glob, os, shutil, sys, time

url_base = 'http://audio3.wordproject.com/bibles/app/audio/%(language_number)s_%(bible_book_number)d.zip'

lang_dict = {
  1:'English',
  2:'Portuguese',
  4:'Mandarin',
  6:'Spanish',
  7:'French',
  8:'Russian',
  9:'German',
  10:'Italian',
  16:'Arabic',
  34:'Romanian',
  39:'Latin (Vulgate)',
  40:'Greek',
}
# ===================
exception_lang2digit_dict = {}
exception_lang2digit_dict[39] = 'vg' # Latin
exception_lang2digit_dict[40] = 'gk' # Greek
# ===================
EXCEPTION_LIST = exception_lang2digit_dict.keys()

url_base_for_exception = 'http://www.wordproaudio.com/audio_lists/%(lang2digit)s/'
filenames_under_exception = '''40_mat.zip
41_mark.zip
42_luke.zip
43_john.zip
44_acts.zip
45_roms.zip
46_1cor.zip
47_2cor.zip
48_galat.zip
49_ephes.zip
50_philip.zip
51_coloss.zip
52_1tess.zip
53_2tess.zip
54_1tim.zip
55_2tim.zip
56_titus.zip
57_philim.zip
58_heb.zip
59_james.zip
60_1pete.zip
61_2pete.zip
62_1john.zip
63_2john.zip
64_3john.zip
65_jude.zip
66_revel.zip'''


def download_url(url):
  '''

  :param url:
  :return:
  '''
  print url
  comm = "wget -c '%s'" %url
  os.system(comm)

def download_exception(number):
  '''

  :param number:
  :return:
  '''
  filenames = filenames_under_exception.split('\n')
  lang2digit = exception_lang2digit_dict[number]
  url_base  = url_base_for_exception %{'lang2digit':lang2digit}
  print url_base
  try:
    for filename in filenames:
      url = url_base + filename
      download_url(url)
  except KeyboardInterrupt:
    sys.exit(1)


def dispatch_download(numbers):
  '''

  :param numbers:
  :return:
  '''
  #numbers = lang_dict.keys()
  numbers.sort()
  try:
    for n in numbers:
      local_dirname_as_number = str(n)
      print 'Creating local dir', local_dirname_as_number
      if not os.path.isdir(local_dirname_as_number):
        os.makedirs(local_dirname_as_number)
      os.chdir(local_dirname_as_number)
      if n in EXCEPTION_LIST:
        print n, 'is exception. Treating it.'
        download_exception(n)
      else:
        for b in range(1, 67):
          n_str = str(n) #.zfill(2)
          url = url_base %{'language_number':n_str, 'bible_book_number':b}
          download_url(url)
      os.chdir('..')
  except KeyboardInterrupt:
    sys.exit(1)

def validate_numbers(numbers):
  '''

  :param numbers:
  :return:
  '''
  print 'Registed numbers are:'
  for n in lang_dict:
    print n, lang_dict[n]
  print '=*40'
  valid_numbers = []
  for n in numbers:
    if n in lang_dict.keys():
      print n, 'is', lang_dict[n]
      valid_numbers.append(n)
    else:
      print n, 'is not a valid wordproject.com language number.'
  return valid_numbers

def get_n_args():
  '''

  :return:
  '''
  numbers = []
  for arg in sys.argv:
    try:
      n = int(arg)
      numbers.append(n)
    except ValueError:
      pass
  return numbers

def main():
  '''

  :return:
  '''
  numbers = get_n_args()
  numbers = validate_numbers(numbers)
  print 'Valid number(s)', numbers
  if len(numbers) == 0:
    print 'No valid numbers. Exiting.'
  dispatch_download(numbers)

if __name__ == '__main__':
  main()
