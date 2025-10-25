#!/usr/bin/python3
"""
~/bin/extract_datedsluglikelinks.py

localuserpylib.pydates.localpydates.gen_last_n_monday_dates_from_date
"""
import os, re, sys
import lblib.pydates.localpydates as dtfs  # .gen_last_n_monday_dates_from_date

lines = '''
https://noticias.uol.com.br/newsletters?investimentos
https://economia.uol.com.br/blogs-e-colunas
https://economia.uol.com.br/videos
https://economia.uol.com.br/imposto-de-renda/duvidas
https://economia.uol.com.br/imposto-de-renda/noticias/redacao/2020/03/06/faca-o-download-do-programa-de-declaracao-do-ir-2020.htm
https://www.folha.uol.com.br/
'''
re_str = r'(\/\d{4}\/\d{2}\/\d{2}\/)'  # regex
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


def process2():
  lines = read_input_file(get_filename_arg())
  urls = filter_datedsluglikelinks(lines)
  confirm_n_download_lines(urls)


class ConvertDates:

  def __init__(self, lines):
    self.lines = lines
    self.dates = []
    self.process()

  def process(self):
    for line in self.lines:
      pdate = dtfs.trans_longtextdate_into_pydate(line)
      if pdate is None:
        continue
      self.dates.append(pdate)
      # self.dates.sort()

  def as_line_by_line_yyyymmdd_dates(self):
    outstr = ""
    for pdate in self.dates:
      line = f"{pdate}\n"
      outstr += line
    return outstr

  def __str__(self):
    outstr = self.as_line_by_line_yyyymmdd_dates()
    return outstr


def process():
  text = """12 de março  de 2024
04 de janeiro de 2024
12 de setembro de 2023
15 de agosto de 2023
15 de agosto de 2023
15 de agosto de 2023
08 de agosto de 2023
24 de julho  de 2023
12 de julho  de 2023
03 de julho  de 2023
02 de junho  de 2023  """
  lines = text.split('\n')
  conv = ConvertDates(lines)
  print(conv)



if __name__ == '__main__':
  process()
