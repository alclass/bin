#!/usr/bin/env python3
"""
This script renames pdf-files inserting the total page number according to a standard/protocal way.

Example:
  Suppose a filename is named:
    'Book of Greek Philosophy.pdf'
  Suppose further this pdf_file has 100 pages. The renaming will change it to:
    'Book of Greek Philosophy.100p.pdf'

Usage:
  pdfsPageCounter.py [<abs_directory>]

Optional Parameter:
  abs_directory: the directory under which the renames will occur. If None, current directory will be used.
"""
import glob
import os
import PyPDF2
from PyPDF2 import PdfFileReader


def check_n_get_number_from_strnumber_plus_p(strnumber_plus_p):
  if strnumber_plus_p is None or len(strnumber_plus_p) == 0:
    return False
  if not strnumber_plus_p.endswith('p'):
    return False
  strnumber = strnumber_plus_p.rstrip('p')
  try:
    number = int(strnumber)
  except ValueError:
    return False  # 0 is equivalent to False
  return number


class PageTotalPdfRenamer:

  def __init__(self, basefolder_absdir='.'):
    if basefolder_absdir is None or\
       len(basefolder_absdir) == 0 or\
       basefolder_absdir == '.' or\
       not os.path.isdir(basefolder_absdir):
      basefolder_absdir = os.path.abspath('.')
    self.basefolder_absdir = basefolder_absdir
    self.seq = 0
    self.total_pdfs_in_folder = 0
    self.pdfs = []  # this attribute is to be deleted after use
    self.pdf_n_pagetotal_tuplelist = []
    self.rename_tuplelist = []
    self.total_renames = 0
    self.bool_confirmed = False

  def collect_pdfs_in_folder(self):
    pdfs = glob.glob('*.pdf')
    # for keeping a record of amounts, the pdf file list itself will be kept up until the end of script
    self.total_pdfs_in_folder = 0 + len(pdfs)
    # filter out those with page-total
    for pdf_filename in pdfs:
      pp = pdf_filename.split('.')
      try:
        from_strnumber_plus_p = pp[-2]
      except IndexError:
        continue
      number = check_n_get_number_from_strnumber_plus_p(from_strnumber_plus_p)
      if not number:  # notice there should not be a pdf with 0 pages (as 0 is equivalent to False)
        self.pdfs.append(pdf_filename)

  def collect_totalpage_for_pdfs(self):
    # for keeping just a record of amounts, the list itself will be deleted
    total_pdfs = len(self.pdfs)
    for i, pdf_filename in enumerate(self.pdfs):
      seq = i + 1
      print(seq, '=>', pdf_filename)
      filepath = os.path.join(self.basefolder_absdir, pdf_filename)
      with open(filepath, 'rb') as fd:
        try:
          pdf_obj = PdfFileReader(fd)
          n_of_pages = pdf_obj.getNumPages()
        except (PyPDF2.errors.PdfReadError, ValueError):
          continue
        pdf_n_pagetotal_tuple = (pdf_filename, n_of_pages)
        print(seq, '/', total_pdfs, 'finding total pages as', n_of_pages, 'for', pdf_filename)
        print('-'*30)
        self.pdf_n_pagetotal_tuplelist.append(pdf_n_pagetotal_tuple)
    del self.pdfs

  def print_totalpage_for_pdfs(self):
    total_pdfs = len(self.pdfs)
    for i, pdf_n_pagetotal_tuple in enumerate(self.pdf_n_pagetotal_tuplelist):
      seq = i + 1
      pagetotal = pdf_n_pagetotal_tuple[1]
      pdfname = pdf_n_pagetotal_tuple[1]
      print(seq, '/', total_pdfs, 'page total', pagetotal, pdfname)

  def mount_renametuples(self):
    for _, pdf_n_pagetotal_tuple in enumerate(self.pdf_n_pagetotal_tuplelist):
      src_filename = pdf_n_pagetotal_tuple[0]
      pagetotal = pdf_n_pagetotal_tuple[1]
      src_filepath = os.path.join(self.basefolder_absdir, src_filename)
      extless_name, _ = os.path.splitext(src_filename)
      if len(extless_name) < 3:
        continue
      if extless_name.endswith('.p'):
        extless_name = extless_name[:-2]
      trg_filename = extless_name + '.' + str(pagetotal) + 'p.pdf'
      trg_filepath = os.path.join(self.basefolder_absdir, trg_filename)
      rename_tuple = (src_filepath, trg_filepath)
      self.rename_tuplelist.append(rename_tuple)

  def show_pairs(self):
    total_renamepdfs = len(self.rename_tuplelist)
    for i, rename_tuple in enumerate(self.rename_tuplelist):
      seq = i + 1
      print('-'*30)
      src_filepath, trg_filepath = rename_tuple
      print(seq, '/', total_renamepdfs, 'To Confirm-Rename:')
      print('\t [', src_filepath, ']')
      print('\t [', trg_filepath, ']')

  def confirm_renames(self):
    self.bool_confirmed = False
    total_renamepdfs = len(self.rename_tuplelist)
    if total_renamepdfs == 0:
      print('-'*30)
      print('There are %d pdf files in running folder.' % self.total_pdfs_in_folder)
      print('No pdf files to rename adding total page number.')
      print('-'*30)
      return
    self.show_pairs()
    screen_msg = 'Confirm the %d renames above ? (*Y/n) ' % len(self.rename_tuplelist)
    ans = input(screen_msg)
    if ans in ['Y', 'y', '']:
      self.bool_confirmed = True

  def rename_pairs(self):
    total_renamepdfs = len(self.rename_tuplelist)
    for i, rename_tuple in enumerate(self.rename_tuplelist):
      seq = i + 1
      src_filepath, trg_filepath = rename_tuple
      if not os.path.isfile(src_filepath):
        continue
      if os.path.isfile(trg_filepath):
        continue
      print(seq, '/', total_renamepdfs, 'Renaming:')
      print(seq, src_filepath)
      print(seq, trg_filepath)
      os.rename(src_filepath, trg_filepath)
      self.total_renames += 1
    print('Total renamed =', self.total_renames)

  def process(self):
    self.collect_pdfs_in_folder()
    self.collect_totalpage_for_pdfs()
    self.mount_renametuples()
    self.confirm_renames()
    if self.bool_confirmed:
      self.rename_pairs()


if __name__ == '__main__':
  renamer = PageTotalPdfRenamer()
  renamer.process()
