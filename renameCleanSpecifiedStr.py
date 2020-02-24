import glob, os, sys

sys.exit(1)

det_str = '   YouTube 360p'
files = glob.glob('*.mp4')
n_renames = 0
for eachFile in files:
  if eachFile.find(det_str):
    newname = eachFile.replace(det_str, '')
    newname = newname.replace('  ', ' ')
    if os.path.isfile(newname):
        continue
    print ('FROM:', eachFile)
    print ('TO:', newname)
    os.rename(eachFile, newname)
    n_renames += 1
print('n_renames', n_renames)
