import os, sys

datafile_n = int(sys.argv[1])
datafilename = 'z_url_wget_dispatcher%d.urls.txt' %datafile_n
print datafilename

urls_str = open(datafilename, 'r').read()
urls_to_filter = urls_str.split()
urls = []
for i, url in enumerate(urls_to_filter):
  if url.startswith('https://'):
    nseq = i + 1
    print nseq, 'Adding', url
    urls.append(url)
total = len(urls)
print 'There are %d URLs' %total

ans = raw_input('Is datafilename above okay? (y/N) ')
if ans in ['n','N']:
  sys.exit(0)

for i, url in enumerate(urls):
  urlprint = url
  if len(url) > 20:
    urlprint = url[0:20]
  print i+1,'of', total, ' :: Downloading:'
  comm = 'wget -c "%s"' %url
  retval = os.system(comm)
  print 'retval', retval

