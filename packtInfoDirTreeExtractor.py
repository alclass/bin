#!/usr/bin/env python3
"""
packtInfoDirTreeExtractor.py
  Explanation
  "/home/dados/Books/epub Books"
"""
import os
import re
import sys
from pathlib import Path
from collections import namedtuple
bookinfo_nt = namedtuple(
  'InfoExtractor',
  ['title', 'year', 'author', 'isbn']
)


class BookInfo:
  """

  Former regex attempt for title did not consider special character such the dash (e.g. Socket-IO)
    re_s_title_n_year = r ^ ?P<title>[\b\\w+\b\\s*]+)(?P<year>\b\\d{4}\b){1}.+?$
  The one below is more generic/encompassing
  """
  re_s_title_n_year = r"^(?P<title>.+?)(?P<year>\b\d{4}\b){1}.+?$"
  re_c_title_n_year = re.compile(re_s_title_n_year)
  re_s_author_n_isbn = r"^.+?(\b\d{4}\b)\s*(?P<author>[\b\w+\b\s+]+.*?); Packt (?P<isbn>\d{13}).*?.epub$"
  re_c_author_n_isbn = re.compile(re_s_author_n_isbn)

  def __init__(self, bookline):
    self.bookline = bookline
    self.title = None
    self.year = None
    self.author = None
    self.isbn = None
    self.astr = ''
    self.matched = False
    self.bookinfo_nt = None
    self.process()

  def trans_namedtuple(self):
    if self.matched:
      self.bookinfo_nt = bookinfo_nt(
        title = self.title,
        year = self.year,
        author = self.author,
        isbn = self.isbn,
      )

  def extract(self):
    # 1 extract pair title and year
    match_o = self.re_c_title_n_year.match(self.bookline)
    self.astr = self.re_c_title_n_year.findall(self.bookline)
    if match_o:
      self.matched = True
      self.title = match_o['title'].strip()
      self.year = match_o['year']
      self.author = None
      self.isbn = None
    # 2 extract pair author(s) and isbn
    match_o = self.re_c_author_n_isbn.match(self.bookline)
    self.astr += self.re_c_author_n_isbn.findall(self.bookline)
    if match_o:
      self.matched = True
      self.author = match_o['author'].strip()
      self.isbn = match_o['isbn']

  def process(self):
    self.extract()
    self.trans_namedtuple()

  def __str__(self):
    outstr = f"""{self.bookline}
      title = [{self.title}] 
      year = {self.year}
      author = [{self.author}] 
      isbn = {self.isbn}
      matched = {self.matched} | astr = {self.astr}
      {self.bookinfo_nt}
    """
    return outstr


class InfoExtractor:

  def __init__(self, basefolder_ap=None):
    self.basefolder_ap = basefolder_ap or Path(os.path.abspath(os.path.curdir))
    self.bookcounter = 0
    # self.bi_non_isbn = 0

  def extract_info_from_filename(self, filename):
    """
      if bi.isbn is None:
        self.bi_non_isbn += 1

    :param filename:
    :return:
    """
    bi = BookInfo(filename)
    if bi.matched:
      self.bookcounter += 1
      bc = self.bookcounter
      print(bc, 'bookinfo_nt', bi.bookinfo_nt)

  def extract_info_from_folder(self, files):
    files = filter(lambda f: f.endswith(('.epub', '.mobi')), files)
    files = filter(lambda f: f.find('Packt') > -1, files)
    for each_file in files:
      self.extract_info_from_filename(each_file)

  def walkup_dirtree(self):
    for self.current_folder_ap, _, files in os.walk(self.basefolder_ap):
      self.extract_info_from_folder(files)

  def process(self):
    self.walkup_dirtree()


def adhoc_test1():
  t = "AI Blueprints 2018 Joshua Eckroth +1; Packt 9781788992879.epub"
  bi = BookInfo(t)
  print('bi', bi)


def get_args():
  rootfolder_ap = None
  if len(sys.argv) > 1:
    rootfolder_ap = sys.argv[1]
  return rootfolder_ap


def process():
  rootfolder_ap = get_args()
  extractor = InfoExtractor(rootfolder_ap)
  extractor.process()


if __name__ == '__main__':
  """
  adhoc_test1()
  """
  process()
