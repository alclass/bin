#!/usr/bin/env python3
"""
~/bin/obxListItemsThruFolders.py
  Walks up a given base folder, looks up all files with "resumo"
  in their names, reads them and extract the "id\ttitle" pattern

"""
import os
import re
# import sys
# re pattern  # (?P<name>...)
restr = r"^(?P<sku>\d{8})\t(?P<title>.*)$"
recmp = re.compile(restr)


class TextThruFoldersGrabber:

  def __init__(self, base_folder):
    self.base_folder = base_folder
    self.curdir_abspath = None
    self.skus = []
    self.skus_n_titles_dict = {}
    self.files_to_read = []
    self.n_files_to_read = 0
    self.n_items = 0
    self.titles = []

  def output_skus_n_items(self):
    items = self.skus_n_titles_dict.items()
    items = sorted(items, key=lambda x: x[1])
    self.n_items = 0
    for tupl in items:
      sku = tupl[0]
      title = tupl[1]
      self.n_items += 1
      scrmsg = f"{sku}\t{title}"
      # print(self.n_items, sku, title)
      print(scrmsg)
    scrmsg = f"Total {len(items)} / {self.n_items}"
    print(scrmsg)

  def read_files(self):
    for filepath in self.files_to_read:
      lines = open(filepath, 'r').readlines()
      for line in lines:
        match_o = recmp.match(line)
        if match_o:
          sku = match_o.group('sku')
          if sku in self.skus_n_titles_dict:
            continue
          title = match_o.group('title')
          title = title.lstrip(' \t').rstrip(' \t\r')
          self.skus_n_titles_dict[sku] = title

  def process_folder(self, filenames):
    for filename in filenames:
      if filename.find('resumo') > -1:
        self.n_files_to_read += 1
        filepath = os.path.join(self.curdir_abspath, filename)
        # print(self.n_files_to_read, 'Added', filename)
        self.files_to_read.append(filepath)

  def walkup_fr_basefolder(self):
    for i, (self.curdir_abspath, _, filenames) in enumerate(os.walk(self.base_folder)):
      # seq = i + 1
      # print(seq, 'traversing:', self.curdir_abspath)
      self.process_folder(filenames)

  def process(self):
      self.walkup_fr_basefolder()
      self.read_files()
      self.output_skus_n_items()


def process():
  dirpath = ("/home/dados/OurDocs/Biz OD/Compras OD/Mats Cnst CmprOD/Lojas Mats Cnst CmprOD/Obramax MatCns CmprOD"
             "/ano a ano Obramax CmprOD")
  grabber = TextThruFoldersGrabber(base_folder=dirpath)
  grabber.process()


if __name__ == '__main__':
  process()
