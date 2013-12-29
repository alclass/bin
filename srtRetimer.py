#!/usr/bin/env python


def pickUpSeconds(secsStr):
    if secsStr.find(',') > -1:
        secsStr = secsStr.replace(',','.')
    seconds = float(secsStr)
    return seconds

def splitTimeFields(timeStr):
    timeFields = timeStr.split(':')
    hour    = int(timeFields[0])
    minute  = int(timeFields[1])
    second  = pickUpSeconds(timeFields[2])
    return hour, minute, second

def joinTagTimeFields(hour, minute, second):
    timeTagStr = str(hour).zfill(2) + ':'
    timeTagStr += str(minute).zfill(2) + ':'
    strSec = str(second).replace('.',',')
    if strSec.find(',') > -1:
        tmp = strSec.split(',')
        intSec  = tmp[0]
        miliSec = tmp[-1]
        strSec = intSec.zfill(2) + ',' + miliSec.zfill(3)
    else:
        # a problem may have occurred
        raise 'a problem may have occurred with strSecs' + time
        # strSec = strSec.zfill(2) + ',' + '000' # this 
    timeTagStr += strSec
    return timeTagStr

def sumToTimeTag(timeToShift, timeShift):
    hour, minute, second = splitTimeFields(timeToShift)
    addHour, addMinute, addSecond = splitTimeFields(timeShift)
    newHour = hour + addHour
    newMinute = minute + addMinute
    newSecond = second + addSecond
    if int(newSecond) > 59:
        newMinute += 1
        newSecond -= 60
    if newMinute > 59:
        newHour   += 1
        newMinute -= 60
    # hour greater than 23 is not considered here for
    # for there is no field "day" here and time span is supposed
    # to never get close to a full day duration
    return joinTagTimeFields(newHour, newMinute, newSecond)

timeStrPattern = '01:07:10,948 --> 01:07:14,326'
arrowIndex = timeStrPattern.find('-->')
def extractTimeStrings(line):
    beginTime = ''
    endTime   = ''
    try:
        beginTime = line[0: arrowIndex - 1]
        endTime   = line[arrowIndex + 4 : -1]
        #print '*', beginTime, '***', endTime
    except:
        pass
    errorMsg = 'has not all its fields or is corrupt.'
    if len(beginTime) < len('xx:xx:xx.xxx'):
        raise 'beginTime ' + errorMsg  + ' => ' + beginTime
    if len(endTime)  < len('xx:xx:xx.xxx'):
        raise 'endTime ' + errorMsg  + ' => ' + endTime
    return beginTime, endTime

def checkTimeString(line):
    if line[arrowIndex : arrowIndex + 3] == '-->':
        return 1
    return 0

def main():
    timeShift = timeShiftValue
    inFile = open(inFilename, 'r'); print # this print for a beginning blank line
    # loop thru' inFile
    while 1:
        line = inFile.readline()
        if line == '' or line == None: # this means EOF
            break
        try:
            n = int(line)
            n += lastSeqNo
            print n
            continue
        except:
            pass
        # check regex
        isTimeTag = checkTimeString(line)
        if isTimeTag:
            beginTime, endTime = extractTimeStrings(line)
            newBeginTime =  sumToTimeTag(beginTime, timeShift)
            newEndTime   =  sumToTimeTag(endTime, timeShift)
            print newBeginTime + ' --> ' + newEndTime
        else:
            print line[:-1]
    inFile.close()

if __name__ == '__main__':
    pass
    print 1
    #main()
