#!/usr/bin/env python3
"""
localuserpylib/ytfunctions/yt_sufix_lang_map_fs.py
"""


def get_nsufix_fr_audioonlycode(audioonlycode: str | None) -> int | None:
  """
  audioonlycode is a str with "a number dash another number", this latter is the nsufix
  Example:
    '233-0' -> returns 0
    '233-5' -> returns 5
    and so on
  """
  try:
    pp = audioonlycode.split('-')
    nsufix = int(pp[1])
    return nsufix
  except (AttributeError, IndexError):
    pass
  return None


class SufixLanguageMapFinder:
  """
  This class finds a map (dict) of sufixes to languages
    for audio-only-codes available from the YouTube parameters
    (used via yt-dlp).

  Obs:
    1 - the parameter -F (or --format) in yt-dlp lists all available
    videocodes, including the audio-only-codes;

    2 - to be known better below, the user must enter an audio-only-code
    with sufix greater than 1 if the first scheme below is expected;

  At the time of writing, there are two main language sufix
    schemes observed from YouTube, they are:

  Scheme 1 (English as the original)
  ========
      0 -> de (Deutsch | German) [autodubbed]
      1 -> es (Español | Spanish) [autodubbed]
      2 -> fr (Français | French) [autodubbed]
      3 -> hi (Hindi) [autodubbed]
      4 -> id (Indonesian) [autodubbed]
      5 -> it (Italiano | Italian) [autodubbed]
      6 -> ja (Japanese) [autodubbed]
      7 -> pl (Poska | Polonese) [autodubbed]
      8 -> pt (Português | Portuguese) [autodubbed]
      9 -> en ((American) English) [original]

  This scheme (English as the original) will produce the following map-as-dict:
    {0: 'de', 1: 'es', 2: 'fr', 3: 'hi', ..., 9: 'en',}

  (@see also Obs-2 above)

  Scheme 2 (English autodubbed)
  ========
      0 -> en (English | English) [autodubbed]
      1 -> <ot> (<other> | "some other language") [original]

  This scheme (English autodubbed) will produce the following map-as-dict:
    {0: 'en', 1: '<ot>'}
  where:
    <ot> is the 2-letter-code for the other (original) language
  Example:
    {0: 'en', 1: 'pt'}
  """

  def __init__(self, audioonlycodes):
    self.audioonlycodes = audioonlycodes
    self.n_ongoing_lang = 0
    self._known_langs_case_ori_en = None
    self.lang_map = None
    self.eng_sufix = None
    self.process()

  @property
  def known_langs_case_ori_en(self):
    if self._known_langs_case_ori_en is not None:
      return self._known_langs_case_ori_en
    self._known_langs_case_ori_en = {
      0: 'de',
      1: 'es',
      2: 'fr',
      3: 'hi',
      4: 'id',
      5: 'it',
      6: 'ja',
      7: 'po',
      8: 'en',  # on some cases 8 may be English
      9: 'en',  # on most cases 9 may be English
    }
    return self._known_langs_case_ori_en

  def make_lang_map_via_eng_ori(self):
    self.lang_map = {}
    for audioonlycode in self.audioonlycodes:
      pp = audioonlycode.split('-')
      if len(pp) < 1:
        self.lang_map.update({0: 'un'})  # unknown, the user must filerename later on
        continue
      sufix = int(pp[1])
      self.lang_map.update({sufix: self.known_langs_case_ori_en[sufix]})
    return self.lang_map

  def make_lang_map_via_noneng_ori(self):
    self.lang_map = {0: 'en', 1: 'pt'}  # the user must filerename 'pt' for the correct one
    return self.lang_map

  def get_sufix_lang_dict(self):
    """
    the lang_dict maps the number sufix in audio-only-codes to
      the 2-letter language identifier

    The example below shows a 'context' known for discovering the languages:

    For example:
      ['233-0', '233-1'] should produce {0:'en': 1:'<the-other-lang>'}
      ['233-0', '233-9'] should produce {0:'de': 9:'en'}

    Obs:

      1)  when, in the audio-only-codes, no sufix greater than 1 is present:
        the mapping will be:
      0 -> en (English | English) [autodubbed]
      1 -> <ot> (<other> | "some other language") [original]

      2) when, in the audio-only-codes, a sufix greater than 1 is present,
        the mapping will be:
      0 -> de (Deutsch | German) [autodubbed]
      1 -> es (Español | Spanish) [autodubbed]
      2 -> fr (Français | French) [autodubbed]
      3 -> hi (Hindi) [autodubbed]
      4 -> id (Indonesian) [autodubbed]
      5 -> it (Italiano | Italian) [autodubbed]
      6 -> ja (Japanese) [autodubbed]
      7 -> pl (Poska | Polonese) [autodubbed]
      8 -> pt (Português | Portuguese) [autodubbed]
      9 -> en ((American) English) [original]

      Obs:
        sometimes English is sufixed 8, most times it's sufixed 9
    """
    if self.lang_map is not None:
      return self.lang_map
    self.eng_sufix = 0  # until proven differently
    for audioonlycode in self.audioonlycodes:
      try:
        audiocode_n_sufixnumber = audioonlycode.split('-')
        sufixnumber = audiocode_n_sufixnumber[1]
        sufixnumber = int(sufixnumber)
        if sufixnumber > 1:
          self.eng_sufix = 8 if sufixnumber < 9 else 9
      except AttributeError:
        pass
    if self.eng_sufix > 0:
      return self.make_lang_map_via_eng_ori()
    return self.make_lang_map_via_noneng_ori()

  def get_lang2lettercode_fr_numbersufix(self, nsufix):
    pdict = self.get_sufix_lang_dict()
    if pdict:
      try:
        return pdict[nsufix]
      except KeyError:
        pass
    return 'un'  # un for "unknown" instead of None

  def get_lang2lettercode_fr_audioonlycode(self, audioonlycode):
    nsufix = get_nsufix_fr_audioonlycode(audioonlycode)
    return self.get_lang2lettercode_fr_numbersufix(nsufix)

  def process(self):
    # this method initializes 'lazy' attributes
    self.get_sufix_lang_dict()

  def print_sufix_lang_map(self):
    print(str(self))

  def __str__(self):
    outstr = f"""SufixLanguageMapFinder:
    map = f{self.lang_map}
    """
    return outstr


def adhoc_test1():
  """
  """
  # example 1
  print('='*20)
  print('example 1')
  print('='*20)
  audioonlycodes = ['233-0', '233-1', '233-5', '233-9']
  print('1 Input', audioonlycodes)
  setter = SufixLanguageMapFinder(audioonlycodes)
  setter.print_sufix_lang_map()
  nsufix = 5
  lang = setter.get_lang2lettercode_fr_numbersufix(nsufix)
  scrmsg = f"get_lang2lettercode_fr_numbersufix({nsufix}) = {lang}"
  print(scrmsg)
  audioonlycode = '233-5'
  lang = setter.get_lang2lettercode_fr_audioonlycode(audioonlycode)
  scrmsg = f"get_lang2lettercode_fr_audioonlycode({audioonlycode}) = {lang}"
  print(scrmsg)
  # example 2
  print('='*20)
  print('example 2')
  print('='*20)
  audioonlycodes = ['233-0', '233-1']
  print('2 Input', audioonlycodes)
  setter = SufixLanguageMapFinder(audioonlycodes)
  setter.print_sufix_lang_map()
  nsufix = 1
  lang = setter.get_lang2lettercode_fr_numbersufix(nsufix)
  scrmsg = f"get_lang2lettercode_fr_numbersufix({nsufix}) = {lang}"
  print(scrmsg)
  # ==============
  print('Testing a non-existing sufix-lang')
  nsufix = 1000
  lang = setter.get_lang2lettercode_fr_numbersufix(nsufix)
  scrmsg = f"get_lang2lettercode_for_numbersufix({nsufix}) = {lang}"
  print(scrmsg)


def process():
  pass


if __name__ == '__main__':
  """
  adhoc_test2()
  """
  process()
  adhoc_test1()
