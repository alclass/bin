#!/usr/bin/env python
# put . in sys.path so we can find ...
import string, sys, os
#sys.path.insert(0, '/home/friend/bin/') # os.curdir
tmpStr='Allocate memory before a back import happens.'
import  srtRetimer

filename = sys.argv[1]
hour = int(sys.argv[2])
minu = int(sys.argv[3])
seco = int(sys.argv[4])
lastSeqNo = 0
if len(sys.argv) > 5:
    lastSeqNo = int(sys.argv[4])

# e.g. '00:01:46,500'
timeShift =  string.zfill(str(hour),2) + ':'
timeShift += string.zfill(str(minu),2) + ':'
timeShift += string.zfill(str(seco),2) + ',000'

lines=open(filename, 'r').readlines()
for line in lines:
    isTimeTag = srtRetimer.checkTimeString(line)
    if isTimeTag:
        beginTime, endTime = srtRetimer.extractTimeStrings(line)
        newBeginTime       =  srtRetimer.sumToTimeTag(beginTime, timeShift)
        newEndTime         =  srtRetimer.sumToTimeTag(endTime, timeShift)
        # print beginTime + ' --> ' + endTime
        print newBeginTime + ' --> ' + newEndTime
    else:
        print line[:-1]
