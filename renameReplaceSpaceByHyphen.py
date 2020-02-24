import glob, os, sys

sys.exit(1)

files = glob.glob('*.mp4')
n_renames = 0
for eachFile in files:
  prefix = eachFile[:7]
  firststripped = lstripped = eachFile[7:]
  if lstripped.startswith('10'):
    lstripped = lstripped[0:2] + '-' + lstripped[3:]
  else:
    lstripped = lstripped[0:1] + '-' + lstripped[2:]
  newname = prefix + lstripped
  if os.path.isfile(newname):
    continue
  print ('FROM:', eachFile)
  print ('M:', firststripped)
  print ('TO:', newname)
  os.rename(eachFile, newname)
  n_renames += 1
print('n_renames', n_renames)
