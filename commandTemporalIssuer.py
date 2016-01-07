#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Explanation
'''
import os, sys, time

def issueInfineLoopCommand(command, nOfMinutes):
  nOfSeconds = nOfMinutes * 60; seq = 0
  while 1:
    print 'Issuing: ', command
    seq += 1
    print 'seq', seq, time.ctime(), ' (next run will occur in ', nOfMinutes, 'minutes) '
    print ' *** to stop/break/interupt, press <CONTROL> + <C> *** '
    os.system(command)
    time.sleep(nOfSeconds)

def getArgs():
  command    = sys.argv[1]
  nOfMinutes = int(sys.argv[2])
  print 'Arguments:'
  print 'command:', command
  print 'Time to delay in between runs:', nOfMinutes
  ans = raw_input('Is this okay ? y/N ')
  if ans not in ['y', 'Y']:
    sys.exit(0)
  return command, nOfMinutes
    
def process():
  command, nOfMinutes = getArgs()
  issueInfineLoopCommand(command, nOfMinutes)
    
if __name__ == '__main__':
  process()
