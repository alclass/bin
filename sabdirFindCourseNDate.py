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

  TO-DO: improve this script adding other forms of output (file, database, spreadsheet etc.)
"""
import datetime
import os
import argparse
import re

parser = argparse.ArgumentParser(description="Walk a dirtree to find SabDir course dates.")
parser.add_argument("--rootdir", type=str, default=None,
                    help="Directory from which to walk up directory to find SabDir course dates")
parser.add_argument("--nlist", type=int, default=50,
                    help="number of courses to list in descending alphabetical order")
args = parser.parse_args()


def gen_last_n_monday_dates(n=50):
  today = datetime.date.today()
  # take today as monday until proven contrary
  monday_date = today
  weekday = today.isoweekday()
  if weekday > 1:
    minus_days = weekday - 1
    monday_date = today - datetime.timedelta(days=minus_days)
  # yields the last n monday dates
  for i in range(n):
    yield monday_date
    monday_date = monday_date - datetime.timedelta(days=7)
  return


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

  def gen_last_ncourses_by_descending_date(self, n=50):
    tuplelist = []
    for sabdircourse in self.courses:
      t = (sabdircourse.coursedate, sabdircourse.coursename)
      tuplelist.append(t)
    tuplelist.sort(key=lambda k: k[0])
    for i in range(n):
      t = tuplelist.pop()
      sabdircourse = SabDirCourse(coursename=t[1], coursedate=t[0])
      yield sabdircourse
    return


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
  for i, sdate in enumerate(gen_last_50_monday_dates()):
    print(i, sdate)


def process():
  rootdir_abspath, nlist = get_cli_args()
  finder = SabDirCourseOSWalkFinder(rootdir_abspath, nlist)
  finder.process()
  for i, t in enumerate(finder.gen_last_ncourses_by_descending_date()):
    seq = i + 1
    print(seq, t)


if __name__ == '__main__':
  """
  adhoc_test()
  """
  process()
