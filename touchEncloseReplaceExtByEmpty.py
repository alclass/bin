#!/usr/bin/env python3
"""
============================= Explanation of this Script's Job =============================
This script does the following:
  It touches new files based on the following rule:
  1) it copies the filename that has a certain/given extension;
  2) then it changes its extension by a fixed one that is name "empty";
  3) this new name is then touched (ie, it is created as a new empty file).
  4) optionally, instead of an empty file,
     the ".empty" file may contain a text line with the original filename
     (e.g.: "the file.mp4" is touched as "the file.empty" and inside a line as "the file.mp4")
  5) optionally, delete original files used for touch
An example:
  If extension chosen is "mp4" and a file named "abc.mp4" is present on the local folder,
  a new file named "abc.empty", if it does not exist previously, will be created empty.
  This, in fact, will be done for all files with extension "mp4" on the local folder.
  
Syntax:
  touchEncloseReplaceExtByEmpty.py [-e=<ext>] [-wi] [-d[
    where:
      -e=<ext> is the extension to be reached: if not given, default is "mp4".
      -wi [or --write-inside] is a marker for writing
                              the former filename into the .empty touched new file
      -d [or --delete] is a marker for deleting original files for empty-touching
                      (use this with care for there is not undoing it after deletion)

This scripted was updated:
  1) to Python 3
  2) to add the -wi functionality (-wi is for "writing inside")
on  2025-02-06 (its date creation is unknown, it may have been written in 2013)
============================= ****************************** =============================
"""
import glob
import os
import sys
DOT_EMPTY_EXT = '.empty'  # to make it configurable in the future (TO-DO)
DEFAULT_DOT_EXTENSION = '.mp4'


def make_shell_touch_command(filename):
  comm = 'touch "%s"' % filename
  return comm


def swap_extension_in_filename(filename, dot_ext_from, dot_ext_to):
  name = filename[ : -len(dot_ext_from)]
  newfilanem = name + dot_ext_to
  return newfilanem


class Toucher(object):
  """
  This class instantiates an object that models that process chain,
    including asking the user's confirmation, to touch new files
    names after a list of files with a certain extension, but
    having the extension "empty".
  """

  def __init__(self,
      extension=DEFAULT_DOT_EXTENSION,
      bool_write_fname_as_txt_inside=False,
      bool_delete_origfiles=False,
  ):
    self.extension = extension
    self.bool_write_fname_as_txt_inside = bool_write_fname_as_txt_inside
    self.bool_delete_origfiles = bool_delete_origfiles
    self._extfiles_before_touch = None
    self.queued_files_for_touch = []
    self.extfiles_touched = []
    self.process()

  @property
  def dot_extension(self):
    return '.' + self.extension

  @property
  def dot_empty(self):
    return DOT_EMPTY_EXT

  @property
  def prenames_touched(self):
    outlist = []
    for fn in self.extfiles_touched:
      prename = fn[:-len(fn)]
      outlist.append(prename)
    return outlist

  @property
  def empty_named_filenames(self):
    outlist = []
    for fn in self.extfiles_touched:
      prename = fn[:-len(fn)]
      emptyfilename = prename + self.dot_empty
      outlist.append(emptyfilename)
    return outlist

  @property
  def extfiles_before_touch(self):
    if self._extfiles_before_touch is not None:
      return self._extfiles_before_touch
    self._extfiles_before_touch = glob.glob('*' + self.dot_extension)
    return self._extfiles_before_touch

  def process(self):
    self.queue_up_files_for_touch()
    self.ask_confirmation_for_touch()
    if len(self.queued_files_for_touch) > 0:
      self.touch()
      if self.bool_write_fname_as_txt_inside:
        self.write_fname_as_txt_inside()
      self.delete_origfiles_in_asked()

  def delete_origfiles_in_asked(self):
    if len(self.extfiles_touched) == 0:
      print('No files to delete.')
      return
    scrmsg = 'Confirm deleting the %d files above ? (Y/n) ' % len(self.extfiles_touched)
    ans = input(scrmsg)
    if ans.lower() not in ['y', '']:
      print('No deletion happened.')
      return
    for i, fname in enumerate(self.extfiles_touched):
      print(i+1, "Deleting: " + fname)
      os.remove(fname)

  def write_fname_as_txt_inside(self):
    """

    :return:
    """
    for touched_filename in self.extfiles_touched:
      # fname = name  #  + '.' + self.extension
      emptyfilename = swap_extension_in_filename(touched_filename, self.dot_extension, self.dot_empty)
      scrmsg = "opening file " + emptyfilename
      print(scrmsg)
      fd = open(emptyfilename, 'w', encoding='utf-8')
      scrmsg = "writing into it: " + touched_filename
      print(scrmsg)
      fd.write(touched_filename)
      fd.close()

  def queue_up_files_for_touch(self):
    print("Queuing up files for empty-touch process.")
    for i, filename in enumerate(self.extfiles_before_touch):
      print(i+1, "Verifying", filename)
      backoffset = len(self.extension) + 1
      prename = filename[:-backoffset]
      newname = prename + self.dot_empty
      print(i+1, "Forming", newname)
      if not os.path.isfile(newname):
        self.queued_files_for_touch.append(filename)
    scrmsg = '%d files queued up.' % len(self.queued_files_for_touch)
    print(scrmsg)

  def ask_confirmation_for_touch(self):
    if len(self.queued_files_for_touch) == 0:
      print('There are no touches for this folder.')
      return False
    for i, queued_filename in enumerate(self.queued_files_for_touch):
      seq = i + 1
      empty_filename = swap_extension_in_filename(queued_filename, self.dot_extension, self.dot_empty)
      comm = make_shell_touch_command(empty_filename)
      print(seq, comm)
    confirm_msg = ' Confirm the %d touchs above ? (Y/n) ' % len(self.queued_files_for_touch)
    ans = input(confirm_msg)
    self.bool_do_touch = True
    if ans.lower() not in ['y', '']:
      self.bool_do_touch = False
    return

  def touch(self):
    if not self.bool_do_touch:
      print("Not touching files.")
      return
    for i, queue_filename in enumerate(self.queued_files_for_touch):
      empty_filename = swap_extension_in_filename(queue_filename, self.dot_extension, self.dot_empty)
      comm = make_shell_touch_command(empty_filename)
      seq = i + 1
      print(seq, comm)
      os.system(comm)
      self.extfiles_touched.append(queue_filename)
    print('Nº of files touched: %d' % len(self.extfiles_touched))


def get_args():
  extension = 'mp4'
  bool_write_inside = False
  bool_delete_origfiles = False
  for arg in sys.argv:
    if arg.startswith('-e='):
      extension = arg[len('-e='):]
    elif arg == '-wi' or arg == '--write-inside':
      bool_write_inside = True
    elif arg == '-d' or arg == '--delete':
      bool_delete_origfiles = True
    elif arg == '-h' or arg == '--help':
      print(__doc__)
      sys.exit(0)
  return extension, bool_write_inside, bool_delete_origfiles


def process():
  # print("This script needs a finishing as of yet. Aborting.")
  # sys.exit(0)
  extension, bool_write_inside, bool_delete_origfiles = get_args()
  scrmsg = ('Executing with parameters: extension=%s; write-inside=%s, delete=%s' %
            (extension, bool_write_inside, bool_delete_origfiles))
  print(scrmsg)
  Toucher(extension, bool_write_inside, bool_delete_origfiles)


if __name__ == '__main__':
  process()
