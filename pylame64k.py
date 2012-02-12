#!/usr/bin/env python
import glob, os, sys
# http://javaposse.com/index.php?post_category=podcasts

def printUsage():
    print '''Usage:
    <command> [file numbers]'''

commPatt = 'lame -b 64 --mp3input -m s --resample 44 "%s" "%s"'
mp3s = glob.glob('*.mp3')
mp3s.sort()
for inMp3 in mp3s:
    if inMp3.find('.64k.') > -1:
        continue
    outMp3 = inMp3[:-4] + '.64k.mp3'
    commLine = commPatt %(inMp3, outMp3)
    retValue = os.system(commLine)
    print commLine, '(returned', retValue, ')'
