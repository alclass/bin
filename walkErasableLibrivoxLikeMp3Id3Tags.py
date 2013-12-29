#!/usr/bin/env python
#--*--encoding:utf-8--*--
import eyeD3, glob, os, sys

tagGlobal = eyeD3.Tag()
IS_TO_DELETE = False

try:
  delParam = sys.argv[1]
  if delParam == '-del':
    IS_TO_DELETE = True
except IndexError:
    pass  

class Mp3Tag():
  def __init__(self, tagArtist, tagAlbum, tagTitle):
    self.tagArtist = tagArtist
    self.tagAlbum  = tagAlbum
    self.tagTitle  = tagTitle
  def untuple(self):
    tagArtist = self.tagArtist
    tagAlbum  = self.tagAlbum
    tagTitle  = self.tagTitle
    return tagArtist, tagAlbum, tagTitle
  def put(self, targetMp3File):
    tagArtist, tagAlbum, tagTitle = self.untuple()
    if not tagArtist or not tagAlbum or not tagTitle:
      print 'Can not update file', targetMp3File, ':: Data missing:', self
      return 0
    #print 'Updating the 3 fields for', targetMp3File
    tagGlobal.link(targetMp3File)
    tagGlobal.header.setVersion(eyeD3.ID3_ANY_VERSION) # eyeD3.ID3_V1_1
    tagGlobal.setArtist(tagArtist)
    tagGlobal.setAlbum (tagAlbum)
    tagGlobal.setTitle (tagTitle)
    tagGlobal.update()
    return 1
  def __str__(self):
    tagArtist, tagAlbum, tagTitle = self.untuple()
    s ='''Tag (3 fields):
tagArtist = %(tagArtistk)s
tagAlbum = %(tagAlbumk)s
tagTitle = %(tagTitlek)s''' \
    %{'tagArtistk':tagArtist, 'tagAlbumk':tagAlbum, 'tagTitlek':tagTitle}
    return s

def processMp3Tag(sourceMp3, targetMp3):
  print '='*40
  print ' [processMp3Tag] sourceMp3', sourceMp3
  tagGlobal.link(sourceMp3)
  tagArtist = tagGlobal.getArtist()
  tagAlbum  = tagGlobal.getAlbum()
  tagTitle  = tagGlobal.getTitle()
  mp3Tag    = Mp3Tag(tagArtist, tagAlbum, tagTitle)
  try:
    print mp3Tag
  except UnicodeEncodeError:
    print 'UnicodeEncodeError'
  print 'Updating targetMp3',
  retVal = mp3Tag.put(targetMp3)
  print 'retVal =', retVal
  if retVal == 1:
    if IS_TO_DELETE:
      print 'Delete', sourceMp3
      os.remove(sourceMp3)
    newName = targetMp3.replace('_64kb','')
    print 'Rename', targetMp3, '>>>', newName
    os.rename(targetMp3, newName)

def preProcess(sourceMp3):
  if sourceMp3.find('24k') > -1:
    return
  targetMp3 = sourceMp3[:-4] + '.24k.mp3'
  if not os.path.isfile(targetMp3):
    print 'targetMp3', targetMp3, 'does not exist. Continuing.'
    return
  print 'processMp3Tag(sourceMp3, targetMp3)', sourceMp3, targetMp3
  processMp3Tag(sourceMp3, targetMp3)


mp3s = glob.glob('*.mp3')
mp3s = mp3s + glob.glob('*.MP3')
mp3s = mp3s + glob.glob('*.Mp3')
mp3s = mp3s + glob.glob('*.mP3')


absPathBase = os.path.abspath('.')
for thisDir, folders, files in os.walk(absPathBase):
  currentAbsPath = os.path.join(absPathBase, thisDir)
  print 'currentAbsPath', currentAbsPath
  os.chdir(currentAbsPath)
  for sourceMp3 in files:
    if sourceMp3[-4:] == '.mp3':
      print 'preProcess(sourceMp3)', sourceMp3
      preProcess(sourceMp3)
