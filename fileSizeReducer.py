#!/usr/bin/env python
import os, sys

print 'Number of Arguments:', len(sys.argv)
if len(sys.argv) <> 4:
  print 'Number of Arguments MUST BE 3 i.e. [1] source file, [2] target file, and [3] target size in Megabytes.'
  sys.exit(0)

infilename  = sys.argv[1]
outfilename = sys.argv[2]
newSizeStr  = sys.argv[3]
print 'Source file:', infilename
print 'Target file:', outfilename
print 'Target file size:', newSizeStr

if not os.path.isfile(infilename):
  print 'Source file (', infilename, ') does not exist. Program can not continue.'
  sys.exit(0)

if os.path.isfile(outfilename):
  print 'Target file (', outfilename, ') exist.'
  ans = raw_input('Delete it? (y/n) ')
  if ans in ['y','Y']:
    os.remove(outfilename)
  else:
    sys.exit(0)

try:
  newSize = float(newSizeStr)
except ValueError:
  print '3rd argument can not be converted to number. Please try again.'
  sys.exit(0)

MEGABYTE = 1024*1024
remaining = cutOffSize = int (newSize * MEGABYTE)

input = open(infilename); output = open(outfilename,'w')
print 'Transferring', cutOffSize, 'bytes to', outfilename

transferred = 0
while remaining > 0:
  if remaining >= 10 * MEGABYTE:
    transferred += 10
    print ' :: ', transferred,
    output.write(input.read(10 * MEGABYTE))
    remaining = remaining - 10 * MEGABYTE
  else:
    transferred += remaining / MEGABYTE
    print ' :: ', transferred
    output.write(input.read(remaining))
    remaining = 0

input.close()
output.close()
