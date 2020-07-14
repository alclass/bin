#!/usr/bin/python3
import os, re, sys

lines = '''
https://noticias.uol.com.br/newsletters?investimentos
https://economia.uol.com.br/blogs-e-colunas
https://economia.uol.com.br/videos
https://economia.uol.com.br/imposto-de-renda/duvidas
https://economia.uol.com.br/imposto-de-renda/noticias/redacao/2020/03/06/faca-o-download-do-programa-de-declaracao-do-ir-2020.htm
https://www.folha.uol.com.br/
'''
re_str = '(\/\d{4}\/\d{2}\/\d{2}\/)' #
re_compiled = re.compile(re_str)
def filter_datedsluglikelinks(lines):
  urls = []
  for line in lines:
    matchobj = re_compiled.search(line)
    if matchobj:
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      urls.append(line)
  urls = set (urls)
  return urls

DEFAULT_FILENAME = 'z-links.url'
def get_filename_arg():
  if len(sys.argv) > 1:
    return sys.argv[1]
  return DEFAULT_FILENAME

def confirm_n_download_lines(urls):
  for i, url in enumerate(urls):
    print (i+1, url)
  ans = input('Confirm dowload %d urls? (Y/n) ' %len(urls))
  if not ans in ['', 'Y', 'y']:
    return
  for i, url in enumerate(urls):
    comm = 'wget "%s"' %url
    print (i+1, 'Downloading', url)
    os.system(comm)

def read_input_file(filename):
  if not os.path.isfile(filename):
    error_msg = 'Filename %s does not exist. Please, enter a valid filename after scriptname.' %filename
    raise ValueError(error_msg)
  text = open(filename, encoding='utf8').read()
  lines = text.split('\n')
  return lines

def process():
  lines = read_input_file(get_filename_arg())
  urls = filter_datedsluglikelinks(lines)
  confirm_n_download_lines(urls)

if __name__ == '__main__':
  process()
