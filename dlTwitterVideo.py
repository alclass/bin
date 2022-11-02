#!/usr/bin/env python3
"""
dlTwitterVideo.py
This script:
 1) receives a list of twitter-video-urls,
 2) post-accesses a twitter-video-site download-page,
 3) scrapes the smallest-sized video url in the download-page
 4) shows the download  urls
 5) asks confirmation and,
 6) if confirmed, issues wget-download commands
 7) if network was working, the downloads must be found in the current running directory

Usage:
$dlTwitterVideo.py <video_twitter_copied_url1> [<video_twitter_copied_url2>] [...] [<video_twitter_copied_url_n>]
"""
import os
import sys
import requests
from bs4 import BeautifulSoup


HTTPPOST_PAGE_URL = 'https://www.savetweetvid.com/downloader'
HTTPPOST_FIELDNAME = 'url'
CHARS_TO_REPLACE = '!?.:"“”/\\|'


def do_download(videourls_videotitles_tuplelist):
  for i, videourls_videotitles_tuple in enumerate(videourls_videotitles_tuplelist):
    videourl, videotitle = videourls_videotitles_tuple
    seq = i + 1
    print(seq, 'Downloading')
    comm = 'wget -c "%s" -O "%s"' % (videourl, videotitle)
    print(comm)
    os.system(comm)


def confirm_downloads(videourls_videotitles_tuplelist):
  n_videos = 0
  for videourls_videotitles_tuple in videourls_videotitles_tuplelist:
    videourl, videotitle = videourls_videotitles_tuple
    n_videos += 1
    comm = '%d =>$wget -c "%s" -O "%s"' % (n_videos, videourl, videotitle)
    print(comm)
  if n_videos == 0:
    print('No videos to download')
    return False
  scr_msg = 'Download the %d videos above (*Y/n)' % n_videos
  ans = input(scr_msg)
  if ans in ['Y', 'y', '']:
    return True
  return False


def extract_smallest_video_url(bsoup):
  btn_items = bsoup.find_all(class_="btn")
  video_urls = []
  smallest_video_url = None
  for item in btn_items:
    try:
      video_url = item['href']
      video_urls.append(video_url)
    except KeyError:
      pass
  if len(video_urls) > 0:
    smallest_video_url = video_urls[0]
  return smallest_video_url


def extract_video_title(bsoup):
  carditems = bsoup.find_all(class_="card-text")
  carditemtext = None
  if len(carditems) > 0:
    carditem = carditems[0]
    carditemtext = carditem.text
    for char in CHARS_TO_REPLACE:
      carditemtext = carditemtext.replace(char, '')
      carditemtext = carditemtext[:70] if len(carditemtext) > 70 else carditemtext
      carditemtext = carditemtext + '.mp4'
  return carditemtext


def scrape_html(req):
  """
  items = soup.find_all('a')
  soup.find_all(class_="class_name")
  for item in items:
    print(item)

  :param req:
  :return:
  """
  htmltext = req.text
  bsoup = BeautifulSoup(htmltext, 'html.parser')
  smallest_video_url = extract_smallest_video_url(bsoup)
  video_title = extract_video_title(bsoup)
  videourls_videotitles_tuple = smallest_video_url, video_title
  return videourls_videotitles_tuple


def download(twitter_video_url):
  """
  form action="https://www.savetweetvid.com/downloader"
  input name="url"
  json_text = req.json()
  print(json_text)
  :return:
  """
  print('Requesting', HTTPPOST_PAGE_URL)
  print('Video url', twitter_video_url)
  req = requests.post(
    HTTPPOST_PAGE_URL,
    data={HTTPPOST_FIELDNAME: twitter_video_url},
  )
  print('HTTP Response')
  return req


def process_videos(twitter_video_urls):
  videourls_videotitles_tuplelist = []
  for twitter_video_url in twitter_video_urls:
    req = download(twitter_video_url)
    videourls_videotitles_tuple = scrape_html(req)
    url, title = videourls_videotitles_tuple
    if url is not None and title is not None:
      videourls_videotitles_tuplelist.append(videourls_videotitles_tuple)
  bool_ans = confirm_downloads(videourls_videotitles_tuplelist)
  if bool_ans:
    do_download(videourls_videotitles_tuplelist)


def get_urls_args():
  twitter_video_urls = []
  for arg in sys.argv:
    if arg.startswith('-h') or arg.startswith('--help'):
      print(__doc__)
      return []
    elif arg.startswith('http'):
      twitter_video_urls.append(arg)
  return twitter_video_urls


def process():
  """
  twitter_video_url = "https://twitter.com/i/status/1587495522494980100"
  twitter_video_urls = get_args()
  :return:
  """
  twitter_video_urls = get_urls_args()
  if len(twitter_video_urls) > 0:
    process_videos(twitter_video_urls)


if __name__ == '__main__':
  process()
