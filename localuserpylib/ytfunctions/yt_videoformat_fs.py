#!/usr/bin/env python3
"""
localuserpylib/ytfunctions/yt_videoformat_fs.py
Contains functions related to YouTube's video formats.
"""
import os.path
import re
# import sys
TWOLETTER_N_LANGUAGENAME_DICTMAP = {
  'ar': 'Arabic',
  'de': 'German',
  'en': 'English',
  'es': 'Spanish',
  'fr': 'French',
  'hi': 'Hindi',
  'id': 'Indonesian',
  'it': 'Italian',
  'ja': 'Japanese',
  'ma': 'Mandarin Chinese',
  'ml': 'Malaysian',
  'po': 'Polish',
  'pt': 'Portuguese',
  'ro': 'Romanian',
  'ru': 'Russian',
  'uk': 'Ukrainian',
}
INTEREST_LANGUAGES = ['de', 'fr', 'en', 'es', 'it', 'ru']
twoletterlangcodes = list(TWOLETTER_N_LANGUAGENAME_DICTMAP.keys())
barred_twoletterlangcodes = '|'.join(twoletterlangcodes)
# restr_2lttcds = r'\[' + barred_twoletterlangcodes + r'\]+'
restr_2lttcds = r'^.*?\[([a-z]{2})\].*$'
recmp_2lttcds = re.compile(restr_2lttcds)


class YTVFTextExtractor:
  """
  YTVFTextExtractor = YouTube Video Format Text Extractor
  :return:
  """
  def __init__(self, videoformatouput: str):
    self.videoformatouput = videoformatouput
    self.langdict = {}
    self.videocode = None
    self.audiocode = None
    self.lines: list = self.videoformatouput.split('\n')
    self.video_is_dubbed = False
    self.video_is_avmerged = False

  def find_languages_knowing_audiocode(self):
    """
    Each language is a dashed-number either appended to the audiocode
      or the videocode is the video is non-merged.
    :return:
    """
    if self.video_is_dubbed:
      if self.video_is_avmerged:
        for i in range(30):
          strdashed = f"{self.audiocode}-{i}"
          pos = self.videoformatouput.find(strdashed)
          if pos > -1:
            print(strdashed, 'found at pos', pos)
            trunk = self.videoformatouput[pos: pos+150]
            line = trunk.split('\n')[0]
            mo = recmp_2lttcds.match(line)
            twoletter = None
            if mo:
              twoletter = mo.group(1)
              print('found 2letter', twoletter)
            if twoletter in INTEREST_LANGUAGES:
              self.langdict[i] = twoletter

  def find_audio_formats_or_the_smaller_video(self):
    """
    These are the following:

    a) audio merging a+v formats may be 140 249 250 251
      a-1 if having dubs, they are accompanied by a "dash-number"
    b) direct video (a mergeless-format) is code 91
      b-2 the series 92 93 94 95 has each one bigger in resolution
    """
    self.video_is_dubbed = None
    self.video_is_avmerged = None
    for strcode in ['249-', '140-', '250-', '251-']:
      if self.videoformatouput.find(strcode) > -1:
        self.audiocode = strcode[:-1]
        # this may be contract onwards
        # because some audiocode have a dashedsufix such as "-drc"
        # and also an equivalent audiocode following by " " (blank)
        self.video_is_dubbed = True
        self.video_is_avmerged = True
        break
    for strcode in ['249 ', '140 ', '250 ', '251 ']:
      if self.videoformatouput.find(strcode) > -1:
        self.audiocode = strcode[:-1]
        self.video_is_dubbed = False
        self.video_is_avmerged = True
        break
    for strcode in ['160 ', '278 ', '394 ']:
      self.videocode = strcode[:-1]
      break
    if self.videocode is None:
      for strcode in ['91 ', '92 ', '93 ', '94 ']:
        if self.videoformatouput.find(strcode) > -1:
          self.videocode = strcode[:-1]
          self.video_is_avmerged = False

  @property
  def composedcode(self):
    """
    It is the code that goes with the parameter -f in yt-dlp

    Examples:
      1) -f 160+249 (merged, non-dubbed)
      2) -f 160+249-0 (merged, dubbed to a specific language)
      3) -f 160+249-1 (idem but to another language)
      4) -f 91 (non-merged, non-dubbed)
      5) -f 91-0 (non-merged, dubbed to a specific language)
      6) -f 91-1 (idem but to another language)
    """
    _composedcode = ''
    if self.video_is_avmerged:
      _composedcode = f"{self.videocode}+{self.audiocode}"
    else:
      _composedcode = f"{self.videocode}"
    _composedcode = _composedcode + '-X' if self.video_is_dubbed else _composedcode
    return _composedcode

  def extract_code_n_lang(self):
    for line in self.lines:
      vfcode = None
      line = line.lstrip(' \t').rstrip(' \t\r\n')
      pp = line.split(' ')
      should_be_number_or_dashed = pp[0]
      if not self.video_is_dubbed:
        vfcode = int(should_be_number_or_dashed)
      else:
        pp = should_be_number_or_dashed.split('-')
        print(pp)
      if vfcode is None:
        continue
      match_o = recmp_2lttcds.match(line)
      if match_o:
        twoletter = match_o.group(1)
        print(twoletter)

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    videocode = {self.videocode}
    audiocode = {self.audiocode}
    video_is_dubbed = {self.video_is_dubbed}
    video_is_avmerged = {self.video_is_avmerged}
    composedcode = {self.composedcode}
    """
    return outstr


def adhoctest2():
  """
  dp = "/media/user/BRAPol SSD2T ori/Tmp/vi tmp/Sci tmp vi/Gen Sci tmp vi/Sabine Hossenfelder Gen Sci yu"
  fn = "video-formats-sabine-MukMOZ0J.txt"
  fn = sys.argv[1]
  """
  dp = "/media/friend/BRAPol SSD2T ori/Tmp/vi tmp/Sci tmp vi/Gen Sci tmp vi/3Blue1Brown (Sci etc) yu/test"
  fn = "video-formats 2025-09-23 8' vd-es Large Language Models explained briefly-LPZh9BOjkQs.txt"
  print(fn)
  fp = os.path.join(dp, fn)
  text = open(fp).read()
  extractor = YTVFTextExtractor(text)
  extractor.find_audio_formats_or_the_smaller_video()
  print(extractor)
  extractor.find_languages_knowing_audiocode()
  print(extractor.langdict)


def adhoctest1():
  """
  """
  print(twoletterlangcodes)
  print(barred_twoletterlangcodes)
  print(restr_2lttcds)
  test = 'dadfa kljçlf [en] ads'
  print(test)
  mo = recmp_2lttcds.match(test)
  print(mo)
  if mo:
    print('2 letter', mo.group(1))


def process():
  pass


if __name__ == '__main__':
  """
  process()
  adhoctest1()
  adhoctest2()
  """
  adhoctest2()
