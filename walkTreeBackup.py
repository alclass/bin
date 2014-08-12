#!/usr/bin/env python
# --*-- encoding: utf8 --*--
import md5, os, shutil, sys, time #, shutil, sys

LF = '\n' # Line Feed constant
REPORT_DIF_SIZE = 'REPORT_DIF_SIZE'
REPORT_DIF_LAST_MODIFICATION_DATE = 'REPORT_DIF_LAST_MODIFICATION_DATE'
REPORT_DIF_MD5 = 'REPORT_DIF_MD5'

localTimeTuple = time.localtime()
localDateTime = str(localTimeTuple[0]) + '-' + str(localTimeTuple[1]).zfill(2) + '-' + str(localTimeTuple[2]).zfill(2) + ' :: '
localDateTime += str(localTimeTuple[3]).zfill(2) + ':' + str(localTimeTuple[4]).zfill(2)  + ':' + str(localTimeTuple[5]).zfill(2)

reportFileName = '_reportFile.txt'
reportFile = open(reportFileName, 'a')
reportFile.write('# this is the report file generated after walk-tree-backup.py ' + localDateTime + LF)


def reportFileDifference(fileOrigin, fileTarget, onWhat):
  text = '''
    fileOrigin = %s
    fileTarget = %s
    DIFFERENCE = %s
''' %(fileOrigin, fileTarget, onWhat)
  reportFile.write(text)


startDirOrigin = defaultStartDir = os.path.abspath('/please/set/start/dir/origin/') 
if len(sys.argv) > 1:
  startDirOrigin = os.path.abspath(sys.argv[1])

# eg /largerpartition/Tp/var-cache-yum
startDirTarget = os.path.abspath('.')
print 'Origin:', startDirOrigin
print 'Target:', startDirTarget

ans = raw_input('Verifique se estão certas as pastas (origem/destino) acima: (s/n)(y/n) ')
if ans not in ['s','S','y','Y']:
  sys.exit(0)

print 'Checking folders existence:'
EXIT=0
print ' [TESTING EXISTENCE] originStartDir', startDirOrigin,
if not os.path.isdir(startDirOrigin):
  print 'does not exist.'
  EXIT=1
else:
  print 'exists. OK!'

print ' [TESTING EXISTENCE] targetStartDir', startDirTarget,
if not os.path.isdir(startDirTarget):
  print 'does not exist.'
  EXIT=1
else:
  print 'exists. OK!'

if EXIT==1:
  print ' [ERROR] A problem occurred: one or the two folder do not exist!'
  print ' Please, revise each folder (origin and target) and re-run script!'
  sys.exit(0)

def takePathAboveOriginStartDir(currentWalkDirFrom, startDirOrigin, startDirTarget):
  relativePath = currentWalkDirFrom[len(startDirOrigin):]
  if len(relativePath) < 1:
    return startDirTarget
  if relativePath[0] == '/':
    relativePath = relativePath[1:]
  return os.path.join(startDirTarget, relativePath) # relativePath

dirsCopiedCount=0; filesCopiedCount=0
for currentWalkDir, folders, files in os.walk(startDirOrigin):
  print ' [CURRENT DIR]', currentWalkDir
  currentWalkDirFrom = os.path.join(startDirOrigin, currentWalkDir)
  currentWalkDirTo = takePathAboveOriginStartDir(currentWalkDirFrom, startDirOrigin, startDirTarget)
  print ' [currentWalkDirTo]', currentWalkDirTo
  folders.sort()
  for folder in folders:
    print ' [CHECK DIR]', folder
    dirTarget = os.path.join(currentWalkDirTo, folder)
    #print ' [target DIR]', dirTarget
    if not os.path.isdir(dirTarget):
      print ' [MAKING DIR]', dirTarget
      dirsCopiedCount += 1
      os.mkdir(dirTarget)
  files.sort()
  for fil in files:
    print ' [CHECK FILE]', fil
    fileTarget = os.path.join(currentWalkDirTo, fil)
    fileOrigin = os.path.join(currentWalkDirFrom, fil)
    if not os.path.isfile(fileTarget):
      print ' [FILECOPY]', fil
      filesCopiedCount += 1
      shutil.copy(fileOrigin, fileTarget)
    else:
      # TODO: check whether sizes, dates and md5sums are the same. For awhile, just write a report. Implement real recopying later on.
      if os.path.getsize(fileOrigin) <> os.path.getsize(fileTarget):
	reportFileDifference(fileOrigin, fileTarget, REPORT_DIF_SIZE)
	continue
      print ' [SIZES are the same]'
      '''
      dateOfLastContentModificationFileOrigin = os.stat(fileOrigin)[8]
      dateOfLastContentModificationFileTarget = os.stat(fileTarget)[8]
      if dateOfLastContentModificationFileOrigin <> dateOfLastContentModificationFileTarget:
	reportFileDifference(fileOrigin, fileTarget, REPORT_DIF_LAST_MODIFICATION_DATE)
	continue
      '''
      # this will time-consuming but less probable to happen
      print ' [CALCULATING MD5]'
      md5FileOrigin = md5.md5(open(fileOrigin).read())
      md5FileTarget = md5.md5(open(fileTarget).read())
      if md5FileOrigin.digest() <>  md5FileTarget.digest():
	reportFileDifference(fileOrigin, fileTarget, REPORT_DIF_MD5)
	continue

print 'dirsCopiedCount:', dirsCopiedCount
print 'filesCopiedCount', filesCopiedCount

# coming reverse way to erase files that exist in target but don't exist in origin
print '''     ***
Now I'll be looking for files that exist in target
 but don't exist in origin, in order to erase them.
              ***'''

def dirToEraseIsInsideDirSetToBeErased(currentWalkDirTo, dirsToEraseList):
  for eachDir in dirsToEraseList:
    if currentWalkDirTo.find(eachDir) > -1:
      return True
  return False

dirsToEraseList = []
os.chdir(startDirTarget)
outFilename = 'bash-to-erase-extra-entries.sh.txt'
if os.path.isfile(outFilename):
  print 'Do you want to replace file', outFilename,'?'
  ans = raw_input('(s/n)(y/n) ')
  if ans not in ['n','N']:
    sys.exit(0)

outFile = open(outFilename, 'w')
outFile.write('# This file contains the shell commands to erase extra files in target backup tree folders' + LF)

for currentWalkDir, folders, files in os.walk(startDirTarget):
  print ' [CURRENT DIR]', currentWalkDir
  currentWalkDirTo = os.path.join(startDirTarget, currentWalkDir)
  if dirToEraseIsInsideDirSetToBeErased(currentWalkDirTo, dirsToEraseList):
    print 'Parent Dir already set to be erased !!! Continuing...'
    continue
  currentWalkDirFrom = takePathAboveOriginStartDir(currentWalkDirTo, startDirTarget, startDirOrigin)
  print ' [currentWalkDirFrom]', currentWalkDirFrom
  folders.sort()
  for folder in folders:
    print ' [CHECK DIR]', folder
    dirOrigin = os.path.join(currentWalkDirFrom, folder)
    print ' [origin DIR]', dirOrigin
    if not os.path.isdir(dirOrigin):
      print '# [bash-command to erase dirTarget]', folder
      dirsCopiedCount += 1
      dirTarget = os.path.join(currentWalkDirTo, folder)
      outFile.write('rm -rf "' + dirTarget + '"' + LF)
      dirsToEraseList.append(dirTarget)
  files.sort()
  for fil in files:
    print ' [CHECK FILE]', fil
    fileOrigin = os.path.join(currentWalkDirFrom, fil)
    print ' [origin file]', fileOrigin
    if not os.path.isfile(fileOrigin):
      print '# [bash-command to erase fileTarget]', fil
      fileTarget = os.path.join(currentWalkDirTo, fil)
      filesCopiedCount += 1
      outFile.write('rm -f "' + fileTarget + '"' + LF)
      #os.remove(fileTarget)
outFile.close()
reportFile.close()