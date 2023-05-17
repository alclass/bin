#!/usr/bin/env python3
"""
This script adds a string to the end of a name in a filename.

Usage:
	$renameSufix.py -i="include-string" -e=[<extension>] -p=[<directory-path>]
Where:
	-i is "the string to add to name's end"
	-e [optional] is the extension to which renames apply (default to pdf)
	-p [optional] is the path to directory where renaming occurs (default to current folder)

Example:
	Suppose a (current) folder has the following files:
		text1.txt | video.mp4 | "a text.txt"
	Running:
		$renameSufix.py -e=txt -i=" a sufix added"
	after confirmation, the new filenames will be:
		"text1 a sufix added.txt" | video.mp4 | "a text a suffix added.txt"
"""
import os
import sys
DEFAULT_DOTEXTENSION = '.pdf'


def include_dot_in_extension_if_needed(ext):
	if ext is None:
		return None
	if not ext.startswith('.'):
		ext = '.' + ext
	return ext


class Renamer:

	def __init__(self, includestr=None, dotextension=None, dir_abspath=None):
		self.rename_pairs = []
		self.confirmed = False
		# params
		self.includestr = None
		self.dotextension = None
		self.dir_abspath = None
		self.treat_params(includestr, dotextension, dir_abspath)

	def treat_params(self, includestr=None, dotextension=None, dir_abspath=None):
		# param includestr
		if includestr is None:
			error_msg = 'includestr is None, please enter it with the -i=<string> parameter'
			raise ValueError(error_msg)
		else:
			self.includestr = str(includestr)
		# param dotextension
		if dotextension is None:
			self.dotextension = DEFAULT_DOTEXTENSION
		else:
			self.dotextension = include_dot_in_extension_if_needed(dotextension)
		# param dir_abspath
		if dir_abspath is None or os.path.isdir(dir_abspath):
			self.dir_abspath = os.path.abspath('.')
		else:
			self.dir_abspath = dir_abspath

	def prep_rename(self):
		self.rename_pairs = []
		filenames = os.listdir(self.dir_abspath)
		filenames = list(filter(lambda f: f.endswith(self.dotextension), filenames))
		filenames.sort()
		for i, fn in enumerate(filenames):
			newname, _ = os.path.splitext(fn)
			newname += self.includestr
			new_filename = newname + self.dotextension
			rename_pair = (fn, new_filename)
			seq = i + 1
			print(seq, 'renaming')
			print('FROM: ' + fn)
			print('TO:   ' + new_filename)
			self.rename_pairs.append(rename_pair)

	def confirm_rename(self):
		self.confirmed = False
		total_torename = len(self.rename_pairs)
		screen_msg = 'Confirm the %d renames above (Y*/n) [ENTER] means yes ' \
			% total_torename
		ans = input(screen_msg)
		if ans in ['Y', 'y', '']:
			self.confirmed = True

	def do_rename(self):
		n_renamed = 0
		if self.confirmed:
			for i, rename_pair in enumerate(self.rename_pairs):
				fn, new_filename = rename_pair
				seq = i + 1
				print(seq, 'renaming')
				print('FROM: ' + fn)
				print('TO:   ' + new_filename)
				os.rename(fn, new_filename)
				n_renamed += 1
		screenline = 'Total files = ' + str(len(self.rename_pairs))
		if n_renamed == 0:
			print(screenline + ' :: No files renamed')
		else:
			print(screenline + ' :: Total files renamed =', n_renamed)

	def process_rename(self):
		self.prep_rename()
		self.confirm_rename()
		self.do_rename()


def get_args():
	dictargs = {'dotextension': None, 'includestr': None}
	for arg in sys.argv:
		if arg.startswith('-e='):
			dotextension = arg[len('-e='):]
			dotextension = include_dot_in_extension_if_needed(dotextension)
			dictargs['dotextension'] = dotextension
		elif arg.startswith('-i='):
			includestr = arg[len('-i='):]
			dictargs['includestr'] = includestr
	return dictargs


def process():
	dictargs = get_args()
	renamer = Renamer(**dictargs)
	renamer.process_rename()


if __name__ == '__main__':
	process()
