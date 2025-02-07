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
     (e.g.: "the file.mp4" is touched as "the file. empty" and inside a line as "the file.mp4")
  5) optionally, delete original files used for touch
An example:
  If extension chosen is "mp4" and a file named "abc.mp4" is present on the local folder,
  a new file named "abc.empty", if it does not exist previously, will be created empty.
  This, in fact, will be done for all files with extension "mp4" on the local folder.
  
Syntax:
  touchEncloseReplaceExtByEmpty.py [-e=<ext>] [-wi] [-d]
    where:
      -e=<ext> is the extension to be reached: if not given, default is "mp4".
      -wi [or --write-inside] is a marker for writing
                              the former filename into the .empty touched new file
      -d [or --delete] is a marker for deleting original files for empty-touching after touch
          (though an extra confirmation will be asked in the prompt line,
          use this with care for there is not undoing it after deletion)

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
  name = filename[: -len(dot_ext_from)]
  newfilanem = name + dot_ext_to
  return newfilanem


class Toucher(object):
  """
  This class instantiates an object that models that process chain,
    including asking the user's confirmation, to touch new files
    names after a list of files with a certain extension, but
    having the extension "empty".
  """

  def __init__(
      self,
      extension=DEFAULT_DOT_EXTENSION,
      bool_write_fname_as_txt_inside=False,
      bool_delete_origfiles=False,
  ):
    self.extension = extension
    self.bool_write_fname_as_txt_inside = bool_write_fname_as_txt_inside
    self.bool_delete_origfiles = bool_delete_origfiles
    self.bool_user_confirmed_touch = False
    self._extfiles_before_touch = None  # to store all filenames having the chosen (or default) extension
    self.queued_files_for_touch = []  # those inside above that can be touched (ie its .empty does not yet exist)
    self.origfiles_that_were_touch = []  # will contain after-process touched filenames
    self.process()

  @property
  def dot_extension(self):
    return '.' + self.extension

  @property
  def dot_empty(self):
    return DOT_EMPTY_EXT

  @property
  def extfiles_before_touch(self):
    if self._extfiles_before_touch is not None:
      return self._extfiles_before_touch
    self._extfiles_before_touch = glob.glob('*' + self.dot_extension)
    return self._extfiles_before_touch

  def delete_origfiles_in_asked(self):
    if not self.bool_delete_origfiles or len(self.origfiles_that_were_touch) == 0:
      print('No files to delete.')
      return
    scrmsg = "-"*30
    print(scrmsg)
    scrmsg = "\tFiles to delete:"
    print(scrmsg)
    scrmsg = "-"*30
    print(scrmsg)
    for i, touched_fn in enumerate(self.origfiles_that_were_touch):
      scrmsg = "\t%d => %s" % (i+1, touched_fn)
      print(scrmsg)
    scrmsg = 'Confirm deleting the %d files above ? (Y/n) ' % len(self.origfiles_that_were_touch)
    ans = input(scrmsg)
    if ans.lower() not in ['y', '']:
      print('No deletion happened.')
      return
    total_deleted = 0
    for i, fname in enumerate(self.origfiles_that_were_touch):
      print(i+1, "Deleting: " + fname)
      os.remove(fname)
      total_deleted += 1
    scrmsg = "-"*30
    print(scrmsg)
    scrmsg = "Total files deleted: %d" % total_deleted
    print(scrmsg)
    scrmsg = "-"*30
    print(scrmsg)

  def write_fname_as_txt_inside(self):
    """
    Writes a line inside in each touched empty file. This line is the original filename.
      Example:
        1) suppose "file-this.mp4" is touched to "file-this.empty"
        2) the "write-inside" will enter line "file-this.mp4" into file "file-this.empty"
      The rationale behind this is to have some non-zero hash value for the file.
      (Noticing that all zero-sized files would have the same hashed value in a particular hash-method.)

    :return:
    """
    if not self.bool_write_fname_as_txt_inside or len(self.origfiles_that_were_touch) == 0:
      scrmsg = " => Not writing original filenames into the empty files"
      print(scrmsg)
      return
    for origfilename in self.origfiles_that_were_touch:
      emptyfilename = swap_extension_in_filename(origfilename, self.dot_extension, self.dot_empty)
      scrmsg = " => Opening file " + emptyfilename
      print(scrmsg)
      fd = open(emptyfilename, 'w', encoding='utf-8')
      scrmsg = ' => Writing into it line: "%s"' % origfilename
      print(scrmsg)
      fd.write(origfilename)
      fd.close()

  def touch(self):
    if not self.bool_user_confirmed_touch or len(self.queued_files_for_touch) == 0:
      scrmsg = " => Not touching files; n° of touchable = %d" % len(self.queued_files_for_touch)
      print(scrmsg)
      return
    for i, queue_filename in enumerate(self.queued_files_for_touch):
      empty_filename = swap_extension_in_filename(queue_filename, self.dot_extension, self.dot_empty)
      comm = make_shell_touch_command(empty_filename)
      print(i+1, comm)
      os.system(comm)
      self.origfiles_that_were_touch.append(queue_filename)
    scrmsg = "-"*30
    print(scrmsg)
    print('Nº of files touched above: %d' % len(self.queued_files_for_touch))
    scrmsg = "-"*30
    print(scrmsg)

  def ask_confirmation_for_touch(self):
    if len(self.queued_files_for_touch) == 0:
      # print('There are no touches for this folder.')
      return
    for i, queued_filename in enumerate(self.queued_files_for_touch):
      seq = i + 1
      empty_filename = swap_extension_in_filename(queued_filename, self.dot_extension, self.dot_empty)
      comm = make_shell_touch_command(empty_filename)
      print(seq, comm)
    confirm_msg = ' Confirm the %d touchs above ? (Y/n) ' % len(self.queued_files_for_touch)
    ans = input(confirm_msg)
    if ans.lower() in ['y', '']:
      self.bool_user_confirmed_touch = True
    else:
      self.bool_user_confirmed_touch = False
    return

  def queue_up_files_for_touch(self):
    print("Queuing up files for empty-touch process.")
    for i, filename in enumerate(self.extfiles_before_touch):
      print(i+1, " => Verifying", filename)
      backoffset = len(self.extension) + 1
      prename = filename[:-backoffset]
      newname = prename + self.dot_empty
      print(i+1, " => Forming", newname)
      if not os.path.isfile(newname):
        self.queued_files_for_touch.append(filename)
    scrmsg = '%d files queued up for touch' % len(self.queued_files_for_touch)
    print(scrmsg)

  def process(self):
    self.queue_up_files_for_touch()
    self.ask_confirmation_for_touch()
    self.touch()
    self.write_fname_as_txt_inside()
    self.delete_origfiles_in_asked()


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
  extension, bool_write_inside, bool_delete_origfiles = get_args()
  scrmsg = ('Executing with parameters: extension=%s; write-inside=%s, delete=%s' %
            (extension, bool_write_inside, bool_delete_origfiles))
  print(scrmsg)
  Toucher(extension, bool_write_inside, bool_delete_origfiles)


if __name__ == '__main__':
  process()
