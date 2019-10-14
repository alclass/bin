#!/usr/bin/env python3
filename = 'urls.txt'
text = open(filename).read()
lines = text.split('\n')
n_lines_initial = len(lines)
lambdef = lambda line : line not in ['', '\n']
lines = list(filter(lambdef, lines))
nline = 0
while nline < len(lines):
  line = lines[nline]
  # look ahead
  delta=1
  try:
    while line == lines[nline+delta]:
      del lines[nline+delta]
      #print ('del line %d' %(nline+delta))
      delta += 1
  except IndexError:
    break
  if delta > 1:
    nline = nline + delta
  else:
    nline += 1
  if nline > len(lines) - 1:
    break

for line in lines:
  print(line)
print ( 'Final   Total of lines: %d' %len(lines) )
print ( 'Initial Total of lines: %d' %n_lines_initial )
