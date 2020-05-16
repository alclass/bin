#!/usr/bin/env python3

import os, sys
import lxml
from lxml.html.clean import Cleaner

BASE_DIR = '.' # '/home/friend/Downloads/Bks/Newspapers/'
inFilename = None # '2020-05-08 [Folha SP] Olavo de Carvalho xinga Regina Duarte depois de defendê-la.html'
basedir_abspath = os.path.abspath(BASE_DIR)

cleaner = Cleaner()
cleaner.javascript = True # This is True because we want to activate the javascript filter
cleaner.style = False

cleaner.kill_tags = ['script']
# cleaner.remove_tags = ['p']

def remove_script_tags_from_file(inFilePath):
  # print("WITH JAVASCRIPT & STYLES")
  # print(lxml.html.tostring(lxml.html.parse(inFilePath)))
  print("Writing output file WITHOUT JAVASCRIPT & STYLES")
  outfilename = 'z-result.html'
  print('Transformed file is named [%s]' %outfilename)
  text = lxml.html.tostring(cleaner.clean_html(lxml.html.parse(inFilePath)))
  outfilepath = os.path.join(basedir_abspath, outfilename)
  outfile = open(outfilepath, 'w')
  outfile.write(str(text))
  outfile.close()

def form_filepath(filename):
  filePath = os.path.join(basedir_abspath, filename)
  if not os.path.isfile(filePath):
    error_msg = 'File %s does not exist in folder.' %filePath
    raise OSError(error_msg)
  return filePath

def get_filename_arg():
  for arg in sys.argv[1:]:
    return arg

def process():
  inFilename = get_filename_arg()
  inFilePath = form_filepath(inFilename)
  remove_script_tags_from_file(inFilePath)

if __name__ == '__main__':
  process()
