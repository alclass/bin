#!/usr/bin/env python
import glob, os, sys

commPatt = 'lame "%s" "%s"'
wavs = glob.glob('*.wav')
wavs = wavs + glob.glob('*.WAV')
wavs = wavs + glob.glob('*.Wav')

wavsCaseInsensitive = []
for each in wavs:
    wavsCaseInsensitive.append(each.lower())    

wavs.sort()
for wav in wavs:
    mp3 = wav[:-4] + '.mp3'
    if os.path.isfile(mp3):
      continue
    commLine = commPatt %(wav,mp3)
    retValue = os.system(commLine)
    print commLine, '(returned', retValue, ')'
