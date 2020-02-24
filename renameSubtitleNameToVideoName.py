import glob, os
SUBTITLE_EXT = '.srt'
VIDEO_EXT = '.mp4'

n_renames = 0
mp4s = glob.glob('*'+VIDEO_EXT)
sorted( mp4s )

subs = glob.glob('*'+SUBTITLE_EXT)
sorted( subs )

if len(mp4s) != len(subs):
  raise Except('len(mp4s) != len(subs)')

print ('oi')

for i, videofilename in enumerate(mp4s):
  videoname, _ = os.path.splitext(videofilename)
  subfilename = subs[i]
  _, subext = os.path.splitext(subfilename)
  subNewname = videoname + subext
  if os.path.isfile(subNewname):
    continue
  print ('FROM ', videofilename )
  print ('FROM ', subfilename )
  print ('TO ', subNewname )
  os.rename(subfilename, subNewname)
  n_renames += 1

print ('n_renames', n_renames)
