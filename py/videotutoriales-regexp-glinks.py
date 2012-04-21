#!/usr/bin/env python
# --*-- encoding: utf8 --*--
import glob, os, re, sys

def filter(urlPart):
  return urlPart.replace('&amp;','&')

filename = defaultFilename = 'videotutoriales-googlemaps.php.htm.txt'
if len(sys.argv) > 1:
  filename = sys.argv[1]

baseUrl='http://www.illasaron.com/html/'
text = open(filename).read()

pattStr = 'value="Descargar Ahora".+onClick="window.location = \'(modules.php[?].+)\'\">'
patt = re.compile(pattStr)
iter = patt.finditer(text)
for matchObj in iter:
  complUrl = matchObj.group(1)
  complUrl = filter(complUrl)
  url = baseUrl + complUrl
  print 'opera -newpage "'+url+'"'