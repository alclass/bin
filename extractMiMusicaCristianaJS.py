#!/usr/bin/env python3
import sys
'''
This script extracts a Java Script array from the standard input:
  input:  an html is passed in
  output: the JS-array (eval'ed later by Python)
  
The extracted array is then used by the download script (dlMiMusicaCristianaNet.py)
'''

phrase_start = 'var list = [{"'
phrase_end   = '"}];'


NEWLINE = '\n'

def exit_if_phrase_not_found(pos, phrase_start_or_end):
	if pos < 0:
		sys.stderr.write('-'*40 + NEWLINE + 'Could not find the [["' + phrase_start_or_end + '"]] Javascript mark-up string.\n *** Aborting program.' + NEWLINE + '-'*40  + NEWLINE)
		sys.exit(1)

text = sys.stdin.read()
pos = text.find(phrase_start)
exit_if_phrase_not_found(pos, phrase_start)
output = text[ pos + len('var list = ') : ]
pos = output.find(phrase_end)
exit_if_phrase_not_found(pos, phrase_end)
output = output[ : pos + len(phrase_end) ]
sys.stdout.write(output + NEWLINE)
