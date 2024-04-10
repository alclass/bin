#!/usr/bin/env python3
"""
This script renames pdf-files inserting the total page number according to a standard/protocal way.
(It uses library PyPDF2.)

Usage:
  pdfsPageCounter.py [-p="<abs_directory>"]  [-y|-Y]

Optional Parameters:
  1) abs_directory: the directory under which the renames will occur. If None, current directory will be used.
  2) -y|-Y means autorename (ie without the user's confirmation (yes/no) in CLI-prompt)

A simple example:
1) Issuing command:
  $ pdfsPageCounter.py
2) Now, suppose there is a filename (in the current running folder) named:
  'Book of Greek Philosophy.pdf'
3) Suppose further this pdf_file has 100 pages. The renaming will change it to:
  'Book of Greek Philosophy.100p.pdf'
4) Notice that a confirmation (yes/no) in the CLI-prompt, in this case (ie, without the -y option), will show up.

Previously, this script ran only under the current folder. In August 2023,
  it was updated to accept any directory in the available folder-tree and then
  can also be used as an API to other calling programs.
"""
import os
import sys
from PyPDF2 import PdfReader  # got deprecated after PyPDF2 v3 use instead PdfReader
from PyPDF2.errors import PdfReadError


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

  def __init__(self, p_basefolder_absdir=None, p_autoren_no_cli_confirm=False):
    self.seq = 0
    self.total_pdfs_in_folder = 0
    self.pdffilenames = []  # this attribute is to be deleted after use
    self.filename_n_pagetotal_tuplelist = []
    self.renamepairs = []
    self.total_renames = 0
    self.autoren_no_cli_confirm = p_autoren_no_cli_confirm
    self.basefolder_absdir = p_basefolder_absdir
    self.treat_basefolder_absdir()

  def treat_basefolder_absdir(self):
    try:
      if os.path.isdir(self.basefolder_absdir):
        # it's okay, return
        return
      else:
        # folder does not exist and exception has not been raised, set it to local 'running' folder and return
        self.basefolder_absdir = os.path.abspath('.')
        return
    except (TypeError, ValueError):
      # exception has been raised, set it to local 'running' folder (return happens in following)
      self.basefolder_absdir = os.path.abspath('.')

  def finish_collect_pdfs_excluding_those_already_with_pagesufix(self, pdffiles):
    """
    There is a strong supposition in the code below, ie filename.nnp.pdf the nnp should not collide with a coincide case
    But would there be a coincide in such case, for the semantics of nnp (eg 257p) is 257 pdf-pages
    :param pdffiles:
    :return:
    """
    self.pdffilenames = []
    for i, pdffile in enumerate(pdffiles):
      pdffilename = os.path.split(pdffile)[1]
      pp = pdffilename.split('.')
      try:
        from_strnumber_plus_p = pp[-2]  # there is a strong supposition in here (@see docstring above)
      except IndexError:
        continue
      number = check_n_get_number_from_strnumber_plus_p(from_strnumber_plus_p)
      if not number:  # notice there should not be a pdf with 0 pages (as 0 is equivalent to False)
        self.pdffilenames.append(pdffilename)

  def select_pdffiles_in_folder(self):
    """
    The method picks up all pdf files in the target (basedir) folder
    Just a historical note: before script was updated to consider full os-paths, it used:
      pdfs = glob.glob('*.pdf')  # because previously the running context was always the current executing directory
    :return:
    """
    filenames = os.listdir(self.basefolder_absdir)
    filenames = list(filter(lambda fn: fn.endswith('.pdf'), filenames))
    pdffiles = [os.path.join(self.basefolder_absdir, fn) for fn in filenames]
    pdffiles = list(filter(lambda f: os.path.isfile(f), pdffiles))
    sorted(pdffiles)
    # filter out those that have already a page-total sufix and then don't need it
    return self.finish_collect_pdfs_excluding_those_already_with_pagesufix(pdffiles)

  def collect_totalpage_in_each_pdf_for_all_pdfs(self):
    # for keeping just a record of amounts, the list itself will be deleted
    afterprocess_filenames = []
    for i, pdffilename in enumerate(self.pdffilenames):
      seq = i + 1
      pdffile = os.path.join(self.basefolder_absdir, pdffilename)
      print(seq, '=>', pdffilename)
      with open(pdffile, 'rb') as fd:
        try:
          pdf_obj = PdfReader(fd)  # PdfFileReader got deprecated
          n_of_pages = len(pdf_obj.pages)  # pdf_obj.getNumPages() got deprecated
        except (PdfReadError, ValueError):  # PyPDF2.errors.PdfReadError
          continue
        afterprocess_filenames.append(pdffilename)
        filename_n_pagetotal_tuple = (pdffilename, n_of_pages)
        print(seq, '/', self.total_pdfs_in_folder, 'finding total pages as', n_of_pages, 'for', pdffilename)
        print('-'*30)
        self.filename_n_pagetotal_tuplelist.append(filename_n_pagetotal_tuple)
    self.pdffilenames = afterprocess_filenames

  def print_totalpage_for_pdfs(self):
    total_pdfs_for_rename = len(self.filename_n_pagetotal_tuplelist)
    for i, filename_n_pagetotal_tuple in enumerate(self.filename_n_pagetotal_tuplelist):
      seq = i + 1
      pdffilename = filename_n_pagetotal_tuple[0]
      pagetotal = filename_n_pagetotal_tuple[1]
      print(seq, '/', total_pdfs_for_rename, 'page total', pagetotal, pdffilename)

  def generate_renamepairs(self):
    self.renamepairs = []
    for pdffile_n_pagetotal_tuple in self.filename_n_pagetotal_tuplelist:
      oldfilename = pdffile_n_pagetotal_tuple[0]
      pagetotal = pdffile_n_pagetotal_tuple[1]
      extless_name, _ = os.path.splitext(oldfilename)
      if len(extless_name) < 3:
        continue
      if extless_name.endswith('.p'):
        extless_name = extless_name[:-2]
      oldfile = os.path.join(self.basefolder_absdir, oldfilename)
      newfilename = extless_name + '.' + str(pagetotal) + 'p.pdf'
      newfile = os.path.join(self.basefolder_absdir, newfilename)
      rename_tuple = (oldfile, newfile)
      self.renamepairs.append(rename_tuple)

  def show_pairs(self):
    total_renamepdfs = len(self.renamepairs)
    for i, rename_tuple in enumerate(self.renamepairs):
      seq = i + 1
      print('-'*30)
      oldfile, newfile = rename_tuple
      oldfilename = os.path.split(oldfile)[1]
      newfilename = os.path.split(newfile)[1]
      print(seq, '/', total_renamepdfs, 'To Confirm-Rename:')
      print('\t [', oldfilename, ']')
      print('\t [', newfilename, ']')

  def confirm_renames(self):
    total_renamepdfs = len(self.renamepairs)
    if total_renamepdfs == 0:
      print('-'*30)
      print('There are %d pdf files in running folder.' % self.total_pdfs_in_folder)
      print('No pdf files to rename adding total page number.')
      print('-'*30)
      return
    self.show_pairs()
    if self.autoren_no_cli_confirm:
      return True
    screen_msg = 'Confirm the %d renames above ? (*Y/n) ' % len(self.renamepairs)
    ans = input(screen_msg)
    if ans in ['Y', 'y', '']:
      return True
    return False

  def rename_pairs(self):
    for i, rename_tuple in enumerate(self.renamepairs):
      seq = i + 1
      oldfile, newfile = rename_tuple
      if not os.path.isfile(oldfile):
        continue
      if os.path.isfile(newfile):
        continue
      print(seq, '/', len(self.renamepairs), 'Renaming:')
      oldfilename = os.path.split(oldfile)[1]
      newfilename = os.path.split(newfile)[1]
      print(seq, oldfilename)
      print(seq, newfilename)
      os.rename(oldfile, newfile)
      self.total_renames += 1
    print('Total renamed =', self.total_renames)

  def process(self):
    self.select_pdffiles_in_folder()
    self.collect_totalpage_in_each_pdf_for_all_pdfs()
    self.generate_renamepairs()
    if self.confirm_renames():
      self.rename_pairs()


def get_args():
  p_autoren_no_cli_confirm = False
  p_basefolder_absdir = None
  for arg in sys.argv:
    if arg.startswith('-p='):
      p_basefolder_absdir = arg[len('-p='):]
    elif arg in ['-y', '-Y']:
      p_autoren_no_cli_confirm = True
  return p_basefolder_absdir, p_autoren_no_cli_confirm


if __name__ == '__main__':
  basefolder_absdir, autoren_no_cli_confirm = get_args()
  renamer = PageTotalPdfRenamer(basefolder_absdir, autoren_no_cli_confirm)
  renamer.process()
