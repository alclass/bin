#!/usr/bin/env python
'''
dlMiMusicaCristianaNet
Created: 2017-03-05 Luiz Lewis

The argument for this script is the name of a text file that contains the JavaScript array variable that is eval'ed in a dict_list here
'''
import os, sys #, time

 
# The example belows shows what is the argument that should be passed in to the executing class WgetComm
# dict_list = [{"title":"Mi Refugio","mp3":"http://mus1.mimusicacristiana.net/mp3/369e3e9c-a98a-4dd4-a2db-2f94c8e62c68.mp3"},
#              {"title":"En Tus Manos","mp3":"http://mus1.mimusicacristiana.net/mp3/b7c4c592-5b5d-4b32-a155-58ea2877969d.mp3"}, ] # etc

def print_arg_explanation_and_exit():
	print '''
	
	This script downloads mp3 songs from mimusicacristiana.net
	
	This script is not automatic for that, ie, the user has to visit the album's webpage in mimusicacristiana.net and copy the JavaScript array as explained below.
	
	This script needs only one command line argument.
	
	This argument is the name of a text file that contains the JavaScript array variable that is eval'ed in a dict_list here.
	Inside this data file, the user should put a JavaScript array list.
	This JavaScript array list is like the following:
	
    dict_list = [{"title":"Mi Refugio","mp3":"http://mus1.mimusicacristiana.net/mp3/369e3e9c-a98a-4dd4-a2db-2f94c8e62c68.mp3"},
                 {"title":"En Tus Manos","mp3":"http://mus1.mimusicacristiana.net/mp3/b7c4c592-5b5d-4b32-a155-58ea2877969d.mp3"}, ] # etc
                 
    How do I get this variable?
    
    Open the source code for an album's artist webpage in http://www.mimusicacristiana.net
    
    Example:
    
    http://www.mimusicacristiana.net/christine-dclario/eterno
    
    Inside the page source, do control+F (search) using '.mp3' and see if the cursor has arrived to something like the chunk below:
    
    --------------------------    
    var list = [{"title":"Intro #EternoLive (Live)","mp3":"http://mus1.mimusicacristiana.net/mp3/e2088a12-b8c9-4f93-8590-83ea7b85cb69.mp3"},{"title":"Yahweh [...]
    --------------------------    
    
    Finding that, just copy and paste it into the data file that is to be used as this script's argument.
    ***
	'''
	sys.exit(0)


class WgetComm():
	
	def __init__(self, dict_list):

		self.dict_list = dict_list
		self.local_folder_name = None # to be found
		self.setLocalFolderName()
		# ==>>> go process!
		self.follow_process()
		
	def setLocalFolderName(self):
		'''
		self.local_folder_name is the name of the current executing folder, ie, the '.''s name
		This attribute is a string (str) and only used for printing, ie, for improving output info to the user
		Even if its retrieval fails (see the try/except block in this method), the guarding abspath str will do okay as an output info
		'''
		localdir_abspath = os.path.abspath('.')
		local_folder_name = str(localdir_abspath) # to be changed in if the try/except block below doesn't raise
		try:
			_, local_folder_name = os.path.split(localdir_abspath)
		except OSError:
			pass
		self.local_folder_name = local_folder_name

	def follow_process(self):
		self.mount_wget_commands()
		if self.confirm_downloads():
			self.exec_comms()

	def mount_wget_commands(self):
		for i, mp3_info_dict in enumerate(self.dict_list):
			n = i + 1
			title = mp3_info_dict['title']
			url   = mp3_info_dict['mp3']
			comm   = 'wget -c %(url)s -O "%(n)s %(title)s.mp3"' %{'n':str(n).zfill(2), 'url':url, 'title':title}
			mp3_info_dict['comm'] = comm
		
	def print_comms(self):
		for i, mp3_info_dict in enumerate(self.dict_list):
		# for i, comm in enumerate(self.wget_commands):
			comm = mp3_info_dict['comm']
			print i+1, comm

	def confirm_downloads(self):
		print '='*40
		print 'Is the list of wget downloads below correct and consistent?'
		print '-'*40
		self.print_comms()
		total = len(self.dict_list)
		print '-'*40
		print 'Total:', total, 'for folder [[', self.local_folder_name, ']]'
		print '='*40
		ans = raw_input(' ==>>> Enter [y/N] and [ENTER] to continue ==>>> ')
		if ans not in ['y','Y']:
			return False
		return True

	def exec_comms(self):
		total = len(self.dict_list)
		for i, mp3_info_dict in enumerate(self.dict_list):
		# for i, comm in enumerate(self.wget_commands):
			info_dict = self.dict_list[i]
			print '-'*40
			print i+1, 'of',total, '=>>> Downloading [', info_dict['title'], '] in [', self.local_folder_name, ']'
			comm = mp3_info_dict['comm']
			os.system(comm)

def pickup_dict_list_arg():
	try:
		data_filename = sys.argv[1]
		jsarray = open(data_filename).read()
		jsarray = jsarray.rstrip(' ;\t\r\n') # in case the user left an ending semicolon, it will strip off, otherwise the eval() will raise an exception
		dict_list = eval(jsarray)
	except IndexError:
		print '''Please, enter the data filename. For help, type -h as argument.
		Exiting.
		'''
		sys.exit(1)
	except IOError:
		print '''IOError, please check if data file exists. For help, type -h as argument.
		Exiting.
		'''
		sys.exit(1)
	except NameError, SyntaxError:
		print '''The JavaScript in data file is not python-eval'ing. Please, check it.'
		Exiting.
		'''
		sys.exit(1)
	return dict_list

def process():
	if '-h' in sys.argv:
		print_arg_explanation_and_exit()
		pass
	dict_list = pickup_dict_list_arg()
	wComm = WgetComm(dict_list)

if __name__ == '__main__':
	process()
