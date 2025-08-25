#!/usr/bin/env python3
"""
localuserpylib/ytfunctions/yt_str_fs_vids_sufix_lang_map_etc.py
"""
import os
import string
import re
YTID_CHARSIZE = 11
enc64_valid_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + '_-'
# Example for the regexp below: https://www.youtube.com/watch?v=abcABC123_-&pp=continuation
ytid_url_w_watch_regexp_pattern = r'watch\?v=([A-Za-z0-9_-]{11})(?=(&|$))'
cmpld_ytid_url_w_watch_re_pattern = re.compile(ytid_url_w_watch_regexp_pattern)
ytid_in_ytdlp_filename_pattern = r'\[([A-Za-z0-9_-]{11})\]'
cmpld_ytid_in_ytdlp_filename_pattern = re.compile(ytid_in_ytdlp_filename_pattern)
ytid_instr_af_equalsign = r'\=([A-Za-z0-9_-]{11})(?=(&|$))'
cmpld_ytid_instr_af_equalsign_pattern = re.compile(ytid_instr_af_equalsign)
ytvideobaseurl = "https://www.youtube.com/watch?v="


def is_str_enc64(line: str | None) -> bool:
  blist = list(map(lambda c: c in enc64_valid_chars, line))
  if False in blist:
    return False
  return True


def is_str_a_ytid(ytid: str | None) -> bool:
  if ytid is None or len(ytid) != YTID_CHARSIZE:
    return False
  return is_str_enc64(ytid)


def get_match_ytid_af_equalsign_or_itself(line):
  """
  Gets a ytid after an "=" (equal sign) or returns the input itself
  :return:
  """
  match = cmpld_ytid_instr_af_equalsign_pattern.search(line)
  return line if match is None else match.group(1)


def extract_ytid_from_yturl_or_itself_or_none(p_supposed_ytid: str | None) -> str | None:
  """
  Extracts ytid from a YouTube-type URL (when ytid is preceded by '?watch=')
  Noting:
    if ytid is None, return None
    if ytid is already a 'ytid sole', return it as is
    if ytid is preceded by '?watch=', match/extract/return ytid
    if regex above can't match, return None

  Example of an extraction from a YouTube-like URL:
    url = "https://www.youtube.com/watch?v=abcABC123_-&pp=continuation"
  The extraction result is:
    ytid = "abcABC123_-"

    Obs: "abcABC123_-" in the example is hypothetical (an ENC64 11-char string)!
  """
  if p_supposed_ytid is None:
    return None
  if is_str_a_ytid(p_supposed_ytid):
    ytid = p_supposed_ytid
    return ytid
  match = cmpld_ytid_url_w_watch_re_pattern.search(p_supposed_ytid)
  return match.group(1) if match else None


def leftstrip_ytvideourl_out_of_str(s: str | None) -> str:
  """
  Returns the input string left-stripped of the YouTube's base-URL
      or empty '' (if input is None or empty)
      or itself (i.e., the input as is)
    Obs: input comes here already passed through a strip(whitespace) operation,
         so this first stripping is not needed at this point
  :param s:
  :return: s (filtered)
  """
  if s is None or s == '':
    return ''
  base = ytvideobaseurl
  if s.startswith(base):
    return s.strip(base)
  else:
    return s


def read_ytids_from_strlines(strlines: list | None) -> list:
  """
  Filters a str list into a list of ytid's

  The data text (here incoming as str lines) must be formed in two ways,
    they are:
      1 - either its ytid is at the beginning (white space ' \t\r\n is filtered out)
      2 - or its ytid is in a URL of the following kind:
        2-1 one with '=' (an equal sign) preceding the ytid
        Obs: in an obvious way, that will also include '?watch=' preceding the ytid
  """
  # strip left and right whitespace ' \t\r\n'
  lines = map(lambda line: line.strip(' \t\r\n'), strlines)
  # lines = list(lines)
  # left-strip beginning YouTube base URL in lines if any
  lines = filter(lambda line: leftstrip_ytvideourl_out_of_str(line), lines)
  # further than the filter above, remove lines if it has a ytid after the '=' sign
  # lines = list(lines)
  # pick up ytid's in string when they happen after '=' (the equal sign)
  lines = map(lambda line: get_match_ytid_af_equalsign_or_itself(line), lines)
  # lines = list(lines)
  # remove lines if it does not have exactly 11-char (YTID_CHARSIZE)
  ytdis = filter(lambda line: len(line) == YTID_CHARSIZE, lines)
  # ytdis = list(ytdis)
  # remove from the remaining 11-char lines those not ENC64-complying
  ytdis = list(filter(lambda line: is_str_enc64(line), ytdis))
  return ytdis


def read_ytids_from_file_n_get_as_list(p_filepath: str) -> list:
  """
  Reads text data file and returns its str lines

    Obs:
      At this version, OSError or IOError try/except was not implemented below,
      but if path or file is missing or a disk error occurs, an exception is expected

  """
  if p_filepath is None or not os.path.isfile(p_filepath):
    return []
  strlines = open(p_filepath, 'r').readlines()
  return read_ytids_from_strlines(strlines)


def verify_ytid_validity_or_raise(ytid):
  if not is_str_a_ytid(ytid):
    errmsg = (
      f"""
      Please check the value entered for/with ytid
        => its entered value is "{ytid}"

      Rules for a valid ytid:
      =======================
      a) it must have {YTID_CHARSIZE} characters
      b) all of them must be ENC64 *

      * All 64 ENC64 characters are: "{enc64_valid_chars}"

      Please, correct the observations(s) above and retry.
      """
    )
    raise ValueError(errmsg)


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


def trans_list_as_uniq_keeping_order_n_makingnewlist(ytids):
  copiedlist = list(ytids)
  return trans_list_as_uniq_keeping_order_n_mutable(copiedlist)


def trans_list_as_uniq_keeping_order_n_mutable(ytids):
  """
  Unicizes input list using an element to element comparison

  Obs:
    The problem with list(set(listvar)), which also unicizes a list, is that
      it does not maintain the original sequencial ordering
  """
  if ytids is None:
    return None
  if len(ytids) == 0:
    return []
  if len(ytids) == 1:
    return ytids
  i = 1
  while i < len(ytids):
    # look up backwardly
    elem_deleted = False
    for j in range(i-1, -1, -1):
      if ytids[i] == ytids[j]:
        del ytids[i]
        elem_deleted = True
        break
    if not elem_deleted:
      i += 1
  return ytids


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

  def find_sufix_number_either_dub_eng_or_ori_eng(self):
    for audioonlycode in self.audioonlycodes:
      try:
        audiocode_n_sufixnumber = audioonlycode.split('-')
        sufixnumber = audiocode_n_sufixnumber[1]
        sufixnumber = int(sufixnumber)
        if sufixnumber > 1:
          self.eng_sufix = 8 if sufixnumber < 9 else 9
      except (AttributeError, IndexError, ValueError):
        self.eng_sufix = 0

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
    # the next for is to establish English either as sufix 0 or 8 or 9
    self.find_sufix_number_either_dub_eng_or_ori_eng()
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
    """
    This method, using the 'process' name as a convention,
      calls another method that will initialize (lazily)'
      all the object's attributes
    :return:
    """
    self.get_sufix_lang_dict()

  def print_sufix_lang_map(self):
    print(str(self))

  def __str__(self):
    outstr = f"""SufixLanguageMapFinder:
    map = f{self.lang_map}
    """
    return outstr


def adhoc_test4():
  print('-'*30)
  print('adhoc_test4: cmpld_ytid_instr_af_equalsign_pattern')
  t = 'https://www.youtube.com/watch?v=Gjg471uIL9k&pp=wgIGCgQQAhgD'
  print(t)
  match = cmpld_ytid_instr_af_equalsign_pattern.search(t)
  if match:
    print(match.group(1))
  else:
    print("didn't match")
  testlist = ['d', 'c', 'a', 'b', 'a', 'a', 'c']
  uniqlist = trans_list_as_uniq_keeping_order_n_makingnewlist(testlist)
  scrmsg = f"testlist {testlist} | uniqlist {uniqlist}"
  print(scrmsg)
  testlist = ['a', 'a']
  uniqlist = trans_list_as_uniq_keeping_order_n_makingnewlist(testlist)
  scrmsg = f"testlist {testlist} | uniqlist {uniqlist}"
  print(scrmsg)
  testlist = ['a']
  uniqlist = trans_list_as_uniq_keeping_order_n_makingnewlist(testlist)
  scrmsg = f"testlist {testlist} | uniqlist {uniqlist}"
  print(scrmsg)


def adhoc_test3():
  print('-'*30)
  print('adhoc_test3: extract_ytid_from_yturl_or_itself_or_none')
  t = 'https://www.youtube.com/watch?v=Gjg471uIL9k&pp=wgIGCgQQAhgD'
  ytid = extract_ytid_from_yturl_or_itself_or_none(t)
  scrmsg = f"""Testing {t}
  Resulting {ytid}"""
  print(scrmsg)
  t = 'https://www.youtube.com/watch?v=abcABC123_-&pp=continuation'
  ytid = extract_ytid_from_yturl_or_itself_or_none(t)
  scrmsg = f"""Testing {t}
  Resulting {ytid}"""
  print(scrmsg)
  # return ytid


def adhoc_test2():
  """
  https://www.youtube.com/watch?v=GnFNf7Q7tH4
  https://www.youtube.com/watch?v=_8iL9SdyJng

  :return:
  """
  print('-'*30)
  print('adhoctest2: extracting ytid from strings when ytid comes after "="')
  strlines = []
  url = 'https://www.youtube.com/watch?v=GnFNf7Q7tH4'
  strlines.append(url)
  print(1, url)
  url = 'https://www.youtube.com/watch?v=_8iL9SdyJng'
  strlines.append(url)
  print(2, url)
  result = read_ytids_from_strlines(strlines)
  print('result', result)


def adhoc_test1():
  """
  """
  print('-'*30)
  print('adhoctest1: SufixLanguageMapFinder')
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
  process()
  adhoc_test1()
  adhoc_test2()
  adhoc_test3()
  """
  adhoc_test4()
