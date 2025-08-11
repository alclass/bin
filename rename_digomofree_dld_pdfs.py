#!/usr/bin/env python3
"""
rename_digomofree_dld_pdfs.py
"""
import os
import glob


class SimpleDldPdfRenamer:

  def __init__(self, basedir_abspath=None):
    self.renames_confirmed = False
    self.basedir_abspath = basedir_abspath
    self.pdfs = []
    self.renamepairs = []
    self.treat_attrs()

  def treat_attrs(self):
    if self.basedir_abspath is None or not os.path.isdir(self.basedir_abspath):
      self.basedir_abspath = os.path.abspath('.')
    scrmsg = f"Current directory: {self.basedir_abspath}"
    print(scrmsg)

  def get_fileabspath_for(self, filename):
    return os.path.join(self.basedir_abspath, filename)

  def find_filenames(self):
    self.pdfs = glob.glob(self.basedir_abspath + '/*.pdf')
    self.pdfs = list(map(lambda fn: os.path.split(fn)[1], self.pdfs))

  def derive_newfilenames_n_store_renamepairs(self):
    for filename in self.pdfs:
      try:
        if filename.find("digamo-free-fr") > - 1:
          # file has already been renamed, move on
          continue
        pp = filename.split('.')
        prename = pp[0]
        npagep = pp[1]
        ext = pp[2]
        dot_npagep_n_ext = f".{npagep}.{ext}"
        new_filename = f"[digamo-free-fr_{prename}-pdf]{dot_npagep_n_ext}"
        pair = (filename, new_filename)
        self.renamepairs.append(pair)
      except (AttributeError, IndexError):
        pass

  def confirm_renames(self):
    seq = 0
    for i, pair in enumerate(self.renamepairs):
      old_filename = pair[0]
      new_filename = pair[1]
      seq = i + 1
      scrmsg = f"{seq} About to rename: FROM [{old_filename}] TO [{new_filename}]"
      print(scrmsg)
    scrmsg = f"Confirm the {seq} renames above? (Y/n) [ENTER] means Yes "
    ans = input(scrmsg)
    self.renames_confirmed = False
    if ans in ['Y', 'y', '']:
      self.renames_confirmed = True

  def do_renames(self):
    if not self.renames_confirmed or len(self.renamepairs) == 0:
      scrmsg = 'Renames not confirmed or no files to be renamed. Returning.'
      print(scrmsg)
      return
    for i, pair in enumerate(self.renamepairs):
      old_filename = pair[0]
      new_filename = pair[1]
      old_filepath = self.get_fileabspath_for(old_filename)
      new_filepath = self.get_fileabspath_for(new_filename)
      os.rename(old_filepath, new_filepath)
      seq = i + 1
      scrmsg = f"{seq} renamed: FROM [{old_filename}] TO [{new_filename}]"
      print(scrmsg)

  def process(self):
    self.find_filenames()
    self.derive_newfilenames_n_store_renamepairs()
    self.confirm_renames()
    self.do_renames()


def process():
  """

  :return:
  """
  ren = SimpleDldPdfRenamer()
  ren.process()


if __name__ == '__main__':
  process()
