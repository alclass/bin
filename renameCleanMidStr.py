#!/usr/bin/env python
'''
This script belongs to the 'rename' prefix Python group of scripts located in the user's bin folder (or, in fact, anywhere).
It does a particular kind of file renaming, which is the following:
 Given a filename, the script will attempt to strip a [p, s] chunk of it,
 where p is string initial position and s is the number of chars to strip off.
Example:

 '01 - blah - The Title.mp4'

If we want the new filename to be:

'01 The Title.mp4'

The chunk '- blah - ' needs to be strip off the original filename.

In this case, -p should be 4 (the initial 0-based index position) and -s should be 9 which is the length/size of '- blah - '
Of course, -ext should be 'mp4' (but the script is able to have None in this parameter and cover the whole directory listing)
'''

import os, sys
# import glob, string, shutil
# import getopt


class Args(object):
  '''
  This is a CLI arguments fetcher class.
  TO-DO : substitute this class with a more standard Python class or API

  The arguments to be fetched are:
    # args = ['-p=', '-s=', '-e']

  The explanation of each one of the arguments with found in the print_explanation_and_exit() method below

  '''
  def __init__(self):
    self.pos_ini  = None
    self.size  = None
    self.file_ext = None
    self.process_cli_args()
    self.check_if_pos_and_size_were_set()

  def print_explanation_and_exit(self):
    print '''Arguments to the script:
    ===========================================
      -p=<integer> required :: it is the string index to begin the char-cleaning
      -s=<integer> required :: it is the number of chars (the size) to clean (withdraw from filename)
      -e=<extension> optional :: it is the file's extension
    ===========================================
    '''
    sys.exit(0)

  def process_cli_args(self):
    for arg in sys.argv:
      if arg.startswith('-p='):
        self.pos_ini = int(arg[len('-p=') : ])
      elif arg.startswith('-s='):
        self.size = int( arg[len('-s=') : ] )
      elif arg.startswith('-e='):
        self.file_ext = arg[len('-e=') : ]

  def check_if_pos_and_size_were_set(self):
    if self.pos_ini == None or self.size == None:
      self.print_explanation_and_exit()

  def get_ext_with_period(self):
    return '.%s' %self.file_ext  # file_ext does NOT have the beginning period ('.')

  def __str__(self):
    outStr = '''Args object:
pos_ini  = %(pos_ini)d
size     = %(size)d
file_ext = %(file_ext)s
''' %{'pos_ini':self.pos_ini, 'size':self.size,'file_ext':self.file_ext}
    return outStr


class Rename(object):
  '''
  This class does the renaming.
  The explanation of the renaming it does is found above in the module's s__doc__ string.
  '''

  def __init__(self, pos_ini, size, file_ext = None, mockFileList=[]):
    '''

    :param pos_ini: required :: it is the string index to begin the char-cleaning
    :param size: required :: it is the number of chars (the size) to clean (withdraw from filename)
    :param file_ext: optional :: it is the file's extension
    :param mockFileList: list used for testing, with messing up with the files in the current folder
    '''

    self.pos_ini = pos_ini
    self.size    = size
    self.file_ext = file_ext
    self.mockFileList = mockFileList
    self.rename_pairs = []
    # self.process()

  def process(self):
    '''

    :return: n_of_renames
    '''
    n_of_renames = 0
    if self.mockFileList != []:
      return None
    self.get_elligible_file_pairs_for_rename()
    bool_confirm = self.show_renames_and_ask_confirmation()  # if self.mockFileList is present, do_renames() will return upfront and not execute
    if bool_confirm:
      n_of_renames = self.do_renames()  # if self.mockFileList is present, do_renames() will return upfront and not execute
    print ('n_of_renames =', n_of_renames)
    return n_of_renames

  def get_elligible_file_pairs_for_rename(self):
    '''
    Both
      + process() without "mocking mode" (the mockFileList filled-in) and
      + run_test_str_with_mockFileList() issue this method

    In mock mode, the mockFileList will be used
    In "folder mode", ie, in true-run mode, the current folder file listing will be used

    :return:
    '''

    if self.mockFileList ==[]:
      files = os.listdir('.')
      files.sort()
    else:
      files = self.mockFileList[:] # make a copy


    self.rename_pairs = []  # reinitialize it to empty
    for original_filename in files:

      name, dot_ext = os.path.splitext(original_filename)
      target_dot_ext = '.' + self.file_ext

      if self.file_ext is not None and target_dot_ext <> dot_ext:
        continue # this file is not to be renamed, it has a different extension

      if self.pos_ini > len(name) - 1:
        continue  # cannot rename this file, for pos_ini is beyond its size

      if self.pos_ini + self.size <= len(name):
        pos_fim = self.pos_ini + self.size
      else:
        pos_fim = len(name) - self.pos_ini + 1

      if self.pos_ini > 0:
        newName = name[ : self.pos_ini]
        if pos_fim < len(name):
          newName += name[ pos_fim : ]
      else: # ie pos_ini == 0
        if pos_fim < len(name):
          newName += name[ pos_fim : ]
        else:
          continue # ie, the file will just be the same, so no need to rename it

      new_filename = newName
      if self.file_ext != None:
        new_filename += target_dot_ext

      self.rename_pairs.append((original_filename, new_filename))

  def show_renames_and_ask_confirmation(self):
    '''

    :return: a boolean confirmation whether to rename files or not
    '''
    if len(self.rename_pairs) == 0:
      print ('No files in folder are under the parameters for renames (pos_ini=%d, pos_fim=%d, file_ext=%s)' %(self.pos_ini, self.size, self.file_ext) )
      return False

    for i, pair in enumerate(self.rename_pairs):
      original_filename, new_filename = pair
      if not os.path.isfile(original_filename):
        continue
      n = i+1
      phrase = 'renaming'
      print ( n, phrase, original_filename )
      print ( '> to:', new_filename )

    ans = raw_input('Are you sure? (y/n) ')
    if ans in ['y', 'Y']:
      return True
    return False

  def do_renames(self):
    '''

    :return: n_of_renames
    '''

    n_of_renames = 0

    if self.mockFileList != []:
      return n_of_renames

    if len(self.rename_pairs) == 0:
      return n_of_renames

    for i, pair in enumerate(self.rename_pairs):
      original_filename, new_filename = pair
      if not os.path.isfile(original_filename):
        continue
      n = i+1
      phrase = 'renamed'
      print ( n, n_of_renames + 1, phrase, original_filename )
      print ( '> to:', new_filename )
      os.rename(original_filename, new_filename)
      n_of_renames += 1
    return n_of_renames

  def run_test_str_with_mockFileList(self):
    '''
    This is an ad hoc testing method that uses the mockFileList class' attribute

    :return: outStr :: the string text that shows original filenames and renamed (new) filenames
    '''
    if self.mockFileList == []:
      return 'mockFileList is EMPTY!'
    self.get_elligible_file_pairs_for_rename()
    outStr = "="*30
    outStr += "\n"
    outStr += "The Result with_mockFileList:"
    outStr += "\n"
    outStr += "-"*30
    outStr += "\n"
    for i, pair in enumerate(self.rename_pairs):
      original_filename, new_filename = pair
      outStr += str(i)
      outStr += " => Old Name = [%s]" %original_filename
      outStr += "\n"
      outStr += "New Name = [%s]" %new_filename
      outStr += "\n"
    return outStr

  def __str__(self):
    '''

    :return:
    '''
    outStr = '''Rename object:
pos_ini  = %(pos_ini)d
size     = %(size)d
file_ext = %(file_ext)s
''' %{'pos_ini':self.pos_ini, 'size':self.size,'file_ext':self.file_ext}
    return outStr


def test_ad_hoc():
  str_files = '''01 - The Learning Problem-mbyG85GZ0PI.mp4
02 - Is Learning Feasible-MEG35RDD7RA.mp4
03 -The Linear Model I-FIbVs5GbBlQ.mp4
04 - Error and Noise-L_0efNkdGMc.mp4
05 - Training Versus Testing-SEYAnnLazMU.mp4
06 - Theory of Generalization-6FWRijsmLtE.mp4
07 - The VC Dimension-Dc0sr0kdBVI.mp4
08 - Bias-Variance Tradeoff-zrEyxfl2-a8.mp4
09 - The Linear Model II-qSTHZvN8hzs.mp4
10 - Neural Networks-Ih5Mr93E-2c.mp4
11 - Overfitting-EQWr3GGCdzw.mp4
12 - Regularization-I-VfYXzC5ro.mp4
13 - Validation-o7zzaKd0Lkk.mp4
14 - Support Vector Machines-eHsErlPJWUU.mp4
15 - Kernel Methods-XUj5JbQihlU.mp4
16 - Radial Basis Functions-O8CfrnOPtLc.mp4
17 - Three Learning Principles-EZBUDG12Nr0.mp4
18 - Epilogue-ihLwJPHkMRY.mp4
youtube-ids.txt*
  '''
  mockFileList = str_files.split('\n')
  rename = Rename(3, 2, 'mp4', mockFileList)
  result_str = rename.run_test_str_with_mockFileList()
  print ( result_str )


def process():
  args = Args()
  # print (args)
  rename = Rename(args.pos_ini, args.size, args.file_ext)
  print ( 'Rename Object: ' + str(rename) )
  rename.process()

if __name__ == '__main__':
  process()
  # test_ad_hoc()
  # unittest.main()
