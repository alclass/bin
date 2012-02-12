#!/usr/bin/env python
import glob, os, sys
# http://javaposse.com/index.php?post_category=podcasts

def printUsage():
    print '''Usage:
    <command> [file numbers]'''

def checkIfConvertedExists(inMp3, mp3sCaseInsensitive):
    if len(inMp3) > 4:
        extensionLess = inMp3[:-4].lower()
        lookingFor = extensionLess + '.24k.mp3'
        if lookingFor in mp3sCaseInsensitive:
            return 1
    return 0
    


#commPatt = 'lame -b 24 --mp3input -m s --resample 24 %(inMp3)s %(outMp3)s'
commPatt = 'lame -b 24 --mp3input -m s --resample 24 "%s" "%s"'    
mp3s = glob.glob('*.mp3')
mp3s = mp3s + glob.glob('*.MP3')
mp3s = mp3s + glob.glob('*.Mp3')
mp3s = mp3s + glob.glob('*.mP3')

mp3sCaseInsensitive = []
for each in mp3s:
    mp3sCaseInsensitive.append(each.lower())    

mp3s.sort()
for inMp3 in mp3s:
    if inMp3.find('.24k.') > -1:
        print inMp3, 'not being 24kbps-converted, supposed is 24kpbs already.'
        continue
    if checkIfConvertedExists(inMp3, mp3sCaseInsensitive):
        print inMp3, 'not being 24kbps-converted, it seems it has been converted already.'
        continue
    outMp3 = inMp3[:-4] + '.24k.mp3'
    commLine = commPatt %(inMp3, outMp3)
    retValue = os.system(commLine)
    print commLine, '(returned', retValue, ')'
