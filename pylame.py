#!/usr/bin/env python
import glob, os, string, sys
# http://javaposse.com/index.php?post_category=podcasts

def printUsage():
    print '''Usage:
    <command> [file numbers]'''

kbps = int(sys.argv[1])
acceptableKbps =  [24,32,48,64,96,128]
if kbps not in acceptableKbps:
    print kbps, 'not in', acceptableKbps
    sys.exit(1)

if kbps < 32:
    freq=24
elif kbps == 32:
    freq=32
else:
    freq=44

def stripExtension(inMp3):
    pp = inMp3.split('.')
    if len(pp) < 2:
        return inMp3
    # suppose pp[-1] is extension
    nameWithoutExtension = string.join(pp[:-1],'.')
    return nameWithoutExtension

def checkIfConvertedExists(inMp3, mp3sCaseInsensitive):
    extensionLess = stripExtension(inMp3)
    lookingFor = extensionLess + '.' + str(kbps) + 'k.mp3'
    lookingFor = lookingFor.lower()
    if lookingFor in mp3sCaseInsensitive:
        return 1
    return 0
    
commPatt = 'lame -b '+str(kbps)+' --mp3input -m s --resample '+str(freq)+' "%s" "%s"'
mp3s = glob.glob('*.mp3')
mp3s = mp3s + glob.glob('*.MP3')
mp3s = mp3s + glob.glob('*.Mp3')
mp3s = mp3s + glob.glob('*.mP3')

mp3sCaseInsensitive = []
for each in mp3s:
    mp3sCaseInsensitive.append(each.lower())    

mp3s.sort()
for inMp3 in mp3s:
    kbpsStr = '.'+str(kbps)+'k.'
    if inMp3.find(kbpsStr) > -1:
        print inMp3, 'not being '+str(kbps)+'kbps-converted, supposed is '+str(kbps)+'kpbs already.'
        continue
    if checkIfConvertedExists(inMp3, mp3sCaseInsensitive):
        print inMp3, 'not being '+str(kbps)+'kbps-converted, it seems it has been converted already.'
        continue
    outMp3 = inMp3[:-4] + '.'+str(kbps)+'k.mp3'
    # last check
    if os.path.isfile(outMp3):
        print inMp3, 'not being '+str(kbps)+'kbps-converted, it seems it has been converted already (last check).'
        continue
    commLine = commPatt %(inMp3, outMp3)
    retValue = os.system(commLine)
    print commLine, '(returned', retValue, ')'
