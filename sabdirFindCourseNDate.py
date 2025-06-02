#!/usr/bin/env python3
"""
sabdirFindCourseNDate.py
  Use os.walk() to visit SabDir courses in a directory tree and introspect each one to find its date

Usage:
  $sabdirFindCourseNDate.py <--rootdir>

Where:
  --rootdir is the absolute path of the folder from where the SabDir courses reside

Example:
  $sabdirFindCourseNDate.py "/media/user/disk1/Direito/CursosSaberDireito"

Output (at this moment's version, a list with coursenames and their dates will be printed out)

  TO-DO: improve this script adding other forms of output (file, database, spreadsheet, etc.)
"""
import copy
import datetime
import os
import argparse
import re
import sys
# sys.path.insert('.')
import localuserpylib.pydates.localpydates as lpd  # module where gen_last_n_monday_dates() resides

parser = argparse.ArgumentParser(description="Walk a dirtree to find SabDir course dates.")
parser.add_argument("--rootdir", type=str, default=None,
                    help="Directory from which to walk up directory to find SabDir course dates")
parser.add_argument("--nlist", type=int, default=50,
                    help="number of courses to list in descending alphabetical order")
args = parser.parse_args()


class SabDirCourse:

  def __init__(self, coursename, coursedate=None):
    self.coursename = coursename
    self.coursedate = coursedate

  def __str__(self):
    outstr = f"{self.coursedate} | {self.coursename}"
    return outstr


class SabDirCourseOSWalkFinder:

  INFOFILENAME = 'z-info.txt'
  dateregexp = re.compile('^(\\d{4}-\\d{2}-\\d{2})')
  nlist_default = 50

  def __init__(self, rootdir_abspath, nlist=None):
    self.rootdir_abspath = rootdir_abspath
    self.currentdir_abspath = None
    self.courses = []
    self.course_infofile_found = 0
    self.n_course = 0
    if nlist is None:
      nlist = self.nlist_default
    self.nlist = nlist

  def find_courses_date(self, sabdircourse):
    self.course_infofile_found += 1
    infofilepath = os.path.join(self.currentdir_abspath, self.INFOFILENAME)
    text = open(infofilepath, 'r').read()
    lines = text.split('\n')
    for line in lines:
      re_o = self.dateregexp.search(line)
      if re_o:
        coursedate = re_o[1]
        pp = coursedate.split('-')
        year = int(pp[0])
        month = int(pp[1])
        day = int(pp[2])
        pdate = datetime.date(year, month, day)
        sabdircourse.coursedate = pdate
        self.courses.append(sabdircourse)
        # print(sabdircourse)

  def introspect_courses_folder_for_info(self, sabdircourse):
    filenames = os.listdir(self.currentdir_abspath)
    onefilename = list(filter(lambda s: s == self.INFOFILENAME, filenames))
    if len(onefilename) == 1:
      # file exists in folder, see into it
      infofilename = onefilename[0]
      if infofilename == self.INFOFILENAME:
        self.find_courses_date(sabdircourse)

  def walk_dir_up(self):
    """

    :return:
    """
    for self.currentdir_abspath, _, filenames in os.walk(self.rootdir_abspath):
      _, foldername = os.path.split(self.currentdir_abspath)
      pos = foldername.find(' _i ')
      if pos > -1:
        coursename = foldername[: pos]
        self.n_course += 1
        print(self.n_course, '@', coursename)
        sabdircourse = SabDirCourse(coursename)
        self.introspect_courses_folder_for_info(sabdircourse)

  def process(self):
    self.walk_dir_up()

  def gen_last_ncourses_by_descending_date(self, alternative_nlist: int = None):
    """
    Generates the last n (self.nlist) courses in descending date order
    :return:
    """
    # tuplelist = []
    # for sabdircourse in self.courses:
    #   t = (sabdircourse.coursedate, sabdircourse)
    #   tuplelist.append(t)
    # ==========
    # a copy is to avoid changing the original order of self.courses
    if alternative_nlist is None:
      nlist = self.nlist
    else:
      nlist = alternative_nlist
    courses_copied = copy.copy(self.courses)
    courses_copied.sort(key=lambda course: course.coursedate, reverse=True)
    nelems = nlist if nlist <= len(courses_copied) else len(courses_copied)
    for i in range(nelems):
      # t = tuplelist.pop()
      # sabdircourse = t[1]
      yield courses_copied[i]
    del courses_copied
    return

  def find_course_on_date(self, pdate):
    resultlist = list(filter(lambda c: c.coursedate == pdate, self.courses))
    if len(resultlist) == 1:
      return resultlist[0]
    return None

  def report_missing_mondays_in_sabdircourses(self):
    courses_copied = copy.copy(self.courses)
    courses_copied.sort(key=lambda course: course.coursedate, reverse=True)
    # now the last course in a list (courses_copied) is the oldest in date
    nelems = len(courses_copied)
    oldest_course = courses_copied[nelems-1]
    oldest_coursedate = oldest_course.coursedate
    for pdate in lpd.gen_all_mondays_inbetweenfrom(oldest_coursedate, ascending_order=False):
      sabdircourse = self.find_course_on_date(pdate)
      if sabdircourse:
        scrmsg = f"The is a course on {pdate} | {sabdircourse}"
        print(scrmsg)
      else:
        scrmsg = f"The is NOT a course on {pdate}"
        print(scrmsg)

  def find_courses_date_by_first_lecture_filedate(self):
    """

    Useful functions
      os.path.getctime(file_path):
        Gets the creation time (or last metadata change time on some systems) as seconds since the epoch.
      os.path.getatime(file_path):
        Gets the last access time as seconds since the epoch.
      os.stat(file_path):
        Returns a stat object containing various file metadata, including timestamps as attributes
          like st_mtime, st_ctime, and st_atime.
      datetime.datetime.fromtimestamp(timestamp):
        Converts the timestamp into a datetime object for more flexible formatting.

    :return:
    """
    # step 1: find the file that corresponds to lecture 1 (_Aula 1)
    filenames = os.listdir(self.currentdir_abspath)
    filename = None
    for filename in filenames:
      if filename.find('_Aula 1') > -1:
        # got it
        break
    if filename is None:
      return None
    file_abspath = os.path.join(self.currentdir_abspath, filename)
    files_ctime = os.path.getctime(file_abspath)
    mondaydate = lpd.get_nearest_monday_from(files_ctime)
    return mondaydate

  def create_zinfofile_if_not_exists(self):
    pass


def get_cli_args():
  """
  Required parameters:
    src_rootdir_abspath & trg_rootdir_abspath

  Optional parameter:
    resolution_tuple

  :return: srctree_abspath, trg_rootdir_abspath, resolution_tuple
  """
  try:
    if args.h or args.help:
      print(__doc__)
      sys.exit(0)
  except AttributeError:
    pass
  rootdir_abspath = args.rootdir
  nlist = args.nlist
  return rootdir_abspath, nlist


def adhoc_test():
  """
  Example for an adhoc test:
    --rootdir="/home/dados/VideoAudio/Soc vi/Law vi/BRA Dir vi/Sab Dir vi/completed Sab Dir ytvi"
  """
  for i, sdate in enumerate(lpd.gen_last_n_monday_dates()):
    print(i, sdate)


def process():
  rootdir_abspath, nlist = get_cli_args()
  finder = SabDirCourseOSWalkFinder(rootdir_abspath, nlist)
  finder.process()
  for i, t in enumerate(finder.gen_last_ncourses_by_descending_date()):
    seq = i + 1
    print(seq, t)
  finder.report_missing_mondays_in_sabdircourses()


if __name__ == '__main__':
  """
  adhoc_test()
  """
  process()
