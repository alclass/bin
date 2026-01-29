#!/usr/bin/env python3
"""
~/bin/mp3SplitAndDeleteOriginals.py

  This script seems, at this moment, to be incomplete.

  Its name suggests that it will split an mp3-file in n-smaller ones
    and then delete the original.
"""
import glob, os
mp3s = glob.glob('*.mp3')
mp3s.sort()


def pick_up_mp3_of_lecture(lecture_n_str):
  mp3s_for_lecture = []
  for mp3 in mp3s:
    if mp3.startswith(lecture_n_str):
      mp3s_for_lecture.append(mp3)
  return mp3s_for_lecture


def mp3wrap(lecture_n):
  lecture_n_str = '%02d' % lecture_n
  glob_str = '%s*.mp3' % lecture_n_str
  mp3s_for_lecture = pick_up_mp3_of_lecture(lecture_n_str)
  name = mp3s_for_lecture[0]
  name = name[len('01-1 '):]
  name = '%s %s' % (lecture_n_str, name)
  comm = 'mp3wrap "%s" ' % name
  for mp3 in mp3s_for_lecture:
    comm += '"%s" ' % mp3
  print('-' * 30)
  print(comm)
  os.system(comm)


def process():
  for lecture_n in range(1, 36+1):
    mp3wrap(lecture_n)


if __name__ == '__main__':
  process()
