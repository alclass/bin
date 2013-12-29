#!/usr/bin/env python
import os, random, sys
'''
This is a simple token translator for organizing not so important
pass-words into some non-production SAP clients/mandantes.
'''

if len(sys.argv) > 1:
  outerPass = sys.argv[1]
else:
  outerPass = raw_input('Please, enter client code with its number [upper & lowercases are treated differently]:')

# init the alphabet, upper and lowercase letters and also string numbers
uppercaseLetters = map(chr, range(65, 65+26))
lowercaseLetters = map(chr, range(65+26+6, 65+26+6+26))
stringNumbers = map(str, range(0,10))

alphaArray = uppercaseLetters + lowercaseLetters + stringNumbers
print 'alphaArray', alphaArray

pw = ''; c = 0; polynomial = 0
for char in outerPass:
  c += 1; nOfChar = ord(char)
  polynomial += nOfChar ** c
  r = polynomial % len(alphaArray)
  newChar = alphaArray[r]
  pw += newChar
  print nOfChar, '**', c, '=', polynomial, 'index after modulus', r, newChar
outLine = outerPass+pw
print outLine
outFilename = 'ptranslator.txt'
outFile = open(outFilename, 'a')
outFile.write(outLine+'\n')

# next token is just to create garbage to the screen
garbage = ''
for i in range(len(outerPass)):
  r = random.randint(0, len(alphaArray)-1)
  newChar = alphaArray[r]
  garbage += newChar
outLine = outerPass+garbage
print outLine
outFile.write(outLine+'\n')
outFile.close()
if os.path.isfile(outFilename):
  os.system('gedit ' + outFilename)
