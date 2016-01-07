#!/usr/bin/env python
import glob, os, sys

extensionList = ['7z','gzip','gz','zip','jar','txt','pdf','doc','swf']

def typeInFilename():
  print 'Type In Filename:'
  filename = raw_input('>>>')
  return filename

files = glob.glob('sf.net-*.txt'); ans='n'; filename=''
if len(files)> 0:
  filename = files[0]
  print 'Proceed with', filename,'? (If "n", a filename choosing will be prompted.)'
  ans=raw_input('(y/n) ')

if not os.path.isfile(filename):
  ans='n'
   
while ans in ['n','N']:
  filename = typeInFilename()
  if not os.path.isfile(filename):
    print 'Filename', filename, 'does not exist. Exiting now.'
    sys.exit(0)

# this is a CONVENTION
projectName = filename[len('sf.net-'):-4]
print 'projectName is', projectName

LF = '\n'; outText = ''
lines=open(filename).readlines(); urlBase = ''

'''
# OLD CODE
if len(lines) > 0:
  firstLine = lines[0]
  if firstLine[0]=='#':
    pp = firstLine.split()
    if len(pp) > 1:
      urlBase = pp[1].strip()

if len(urlBase) < len('x.dl.sourceforge.net/x'):
  print 'Program could not find base url.'
  sys.exit(0)

if not urlBase[-1]=='/':
  urlBase += '/'
'''

urlBase = 'http://ufpr.dl.sourceforge.net/'+projectName+'/'
  
for line in lines:
  if len(line) < 3:
    continue
  if line[0] == '#':
    print 'line[0] =', line[0], 'continuing'
    continue
  pp = line.split()
  #print pp
  if len(pp) > 0:
    urlComplement = pp[0].strip()
    if urlComplement.find('.') < 0:
      continue
    extension = urlComplement.split('.')[-1]
    if extension not in extensionList:
      continue
    if not urlBase.startswith('http://'):
      urlBase = 'http://' + urlBase
    url = urlBase + urlComplement
    outText += url + LF
    print url

ans = raw_input('Output urls to urls-to-dl.txt (former content will be lost) ? (y/n) ')
if ans in ['y','Y']:
  outFile = open('urls-to-dl.txt', 'w')
  outFile.write(outText)
  outFile.close()
