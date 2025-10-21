#!/usr/bin/env python3
"""
localuserpylib/ytfunctions/yt_str_fs_vids_sufix_lang_map_etc.py
Contains functions related YouTube names, id's, languages and their codes.
"""
# from collections.abc import Iterable
# from typing import Tuple
from typing import Generator
from typing import Any
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
# another pattern to extract a ytid is the following: https://www.youtube.com/shorts/<ytid>
# but the ytid will generalized as a split('/')[-1] and then tested as an 11-char ENC64 str
ytvideobaseurl = "https://www.youtube.com/watch?v="
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
  if match:
    return match.group(1)
  # lastly, test also a pattern like this one: https://www.youtube.com/shorts/<ytid>
  # but generalize it to its ending as '/' + ytid
  pp = p_supposed_ytid.split('/')
  if len(pp) < 2:  # minimally url must be at least "<site>/<ytid>" case which would make it 2: len(pp)=2
    return None
  ytid = pp[-1]
  if is_str_a_ytid(ytid):
    return ytid
  return None


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


def get_validated_ytid_or_raise(ytid):
  verify_ytid_validity_or_raise(ytid)
  return ytid


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


def trans_str_sfx_n_2letlng_map_to_dict_or_raise(pdict):
  """
  Transforms a string represent a number-and-twoletterlanguagecode map into a dict, noting:
  1 - the elements (key and value) in the incoming string, do not need to be enclosed within simple or double quotes
    1 - 1 if it has quotes, no problem, they are stripped off for its dict conversion
  2 - the outgoing dict has an int key (the language index or sufix [its semantic is considered here])
    and a string value (which is the twoletterlanguagecode)

  Initially written for:
    1 - script dlYouTubeWhenThereAreDubbed that contains this dict in question as an input parameter
    2 - the output dict will serve to instantiate a SufixLangMapper mapper object
  """
  if isinstance(pdict, dict):
    return pdict
  outdict = {}
  pp = pdict.split(',')
  for elem in pp:
    try:
      if elem.find(':') < 0:
        continue
      pair = elem.split(':')
      pair0 = pair[0].strip(' \t\r\n"\'')
      number = int(pair0)
      twolettercode = pair[1]
      twolettercode = twolettercode.strip(' \t\r\n"\'')
      if len(twolettercode) != 2:
        wrnmsg = f"Warning: a twolettercode should have 2 letter, it has {len(twolettercode)} in {pdict}"
        print(wrnmsg)
        continue
      outdict.update({number: twolettercode})
    except (IndexError, ValueError) as e:
      wrnmsg = f"Error: sfx_n_2letlng_dict is malformed with elem [{elem}] in strdict [{pdict}] | {e}"
      print(wrnmsg)
      continue
  return outdict


class LangAttr:

  def __init__(self, langless_audiocode, nsufix, twolettercode, seq_order):
    self.langless_audiocode = langless_audiocode
    self.nsufix = nsufix
    self.twolettercode = twolettercode
    self.seq_order = seq_order

  @property
  def audioonlycode(self):
    aoc = f"{self.langless_audiocode}-{self.nsufix}"
    return aoc

  @property
  def langname(self) -> str:
    try:
      _langname = TWOLETTER_N_LANGUAGENAME_DICTMAP[self.twolettercode]
      return _langname
    except IndexError:
      pass
    return 'not-known'

  def __str__(self):
    la = self.langless_audiocode
    aoc = self.audioonlycode
    tlc = self.twolettercode
    ln = self.langname
    outstr = f"""{self.__class__.__name__}
    seq_order = {self.seq_order} | twolettercode = {tlc} |  language name = {ln}
    langless_audiocode = {la} | nsufix = {self.nsufix} | audioonlycode = {aoc}"""
    return outstr


class SufixLanguageMapper:

  def __init__(self, pdict: dict[int, str] | str, audiomainnumber=249):
    self.no_dubs = False
    self.indict: dict[int, str] = pdict
    self._dict_as_items = None
    self.at_number = 0
    self.reached_end = False
    self.twolettercodes_given = []
    self.audiomainnumber = audiomainnumber
    self.treat_indict()

  def treat_indict(self):
    if self.indict is None:
      errmsg = f"Error: the sufix and language dict {self.indict} is malformed or None"
      raise ValueError(errmsg)
    if isinstance(self.indict, str):
      self.indict = trans_str_sfx_n_2letlng_map_to_dict_or_raise(self.indict)

  @property
  def dict_as_items_in_order(self) -> list[tuple[int, str]]:
    """
    About type-annotation:
    if the return had not the list() function, the return type-annotation should be:
      Iterable[Tuple[int, str]] when the iterable (without list()) is returned
    """
    if self._dict_as_items is not None:
      return self._dict_as_items
    ordered_dict = sorted(self.indict.items(), key=lambda pair: pair[0])
    self._dict_as_items = list(ordered_dict)
    return self._dict_as_items

  @property
  def nsufices_in_order(self) -> list[int]:
    """
    Returns the nsufix numbers in ascending order
    Example:
      suppose langdict = [1:'pt', 0:'en']  # out of sequencing order purposefully for the example
      then dict_as_items_in_order = [(0, 'en'), (1, 'pt')]  # in ascending order on nsufix
      then nsufices_in_order = [0, 1]
    :return:
    """
    nsufices = [e[0] for e in self.dict_as_items_in_order]
    return nsufices

  @property
  def audioonlycodes(self) -> list[str]:
    """
    Returns the audioonlycode list
    This list is dynamically formed at each call
    :return: aocs
    """
    aocs = []
    for item in self.dict_as_items_in_order:
      numbersufix = item[0]
      audioonlycode = f"{self.audiomainnumber}-{numbersufix}"
      aocs.append(audioonlycode)
    return aocs

  @property
  def size(self) -> int:  # Iterable[Tuple[int, str]] when the iterable (without list()) is returned
    return len(self.indict)

  def turn_off_dubs(self):
    self.no_dubs = True

  def get_first_2lettlangcode(self) -> str | None:
    if self.no_dubs:
      return 'un'  # 'unique' (no dubs)
    try:
      twolettercode = self.dict_as_items_in_order[0][1]
      return twolettercode
    except IndexError:
      pass
    return 'un'  # 'un' above means 'no dubs', but here it would mean 'unknown'

  def get_first_langobj(self) -> LangAttr:
    if self.no_dubs:
      langer = LangAttr(
        langless_audiocode=self.audiomainnumber,
        nsufix=-1,
        twolettercode='un',  # un stands for 'unique' and also that there's only the original language
        seq_order=1
      )
      return langer
    pair = self.dict_as_items_in_order[0]
    nsufix = pair[0]
    twolettercode = pair[1]
    langer = LangAttr(
      langless_audiocode=self.audiomainnumber,
      nsufix=nsufix,
      twolettercode=twolettercode,
      seq_order=1
    )
    return langer

  def get_ith_2lettlangcode_1idxbased(self, n) -> str | None:
    try:
      i = n - 1
      return self.dict_as_items_in_order[i][1]
    except IndexError:
      pass
    return 'un'

  @staticmethod
  def get_langname_fr_2lettercode(twolettercode):
    try:
      return TWOLETTER_N_LANGUAGENAME_DICTMAP[twolettercode]
    except IndexError:
      pass
    return 'unknown'

  def get_nsufix_fr_idx(self, idx) -> int:
    try:
      nsufix = self.dict_as_items_in_order[idx][0]
      return nsufix
    except KeyError:
      pass
    return -1

  def get_twolettercode_fr_idx(self, idx) -> str:
    try:
      twolettercode = self.dict_as_items_in_order[idx][1]
      return twolettercode
    except KeyError:
      pass
    return 'un'

  def get_twolettercode_fr_nsufix(self, nsfx) -> str:
    """
    The different between this method and the one is that this one the index is the key itself.
    For the other, the index is its sequencial one.
    """
    try:
      twolettercode = self.indict[nsfx]
      return twolettercode
    except KeyError:
      pass
    return 'un'

  def get_twolettercode_n_langname_fr_nsufix(self, nsfx) -> tuple[str, str]:
    twolettercode = self.get_twolettercode_fr_nsufix(nsfx)
    langname = self.get_langname_fr_2lettercode(twolettercode)
    return twolettercode, langname

  def get_langname_fr_idx(self, idx) -> str:
    twolettercode = self.get_twolettercode_fr_idx(idx)
    return self.get_langname_fr_2lettercode(twolettercode)

  def get_langname_fr_sufix_n(self, nsfx) -> str:
    twolettercode = self.get_twolettercode_fr_nsufix(nsfx)
    return self.get_langname_fr_2lettercode(twolettercode)

  def get_audioonlycodesufix_fr_idx(self, idx) -> int | None:
    try:
      pair = self.dict_as_items_in_order[idx]
      nsufix = pair[0]
      return nsufix
    except KeyError:
      pass
    return None

  def get_audioonlycode_fr_idx(self, idx) -> str | None:
    nsufix = self.get_audioonlycodesufix_fr_idx(idx)
    if nsufix is None:
      return None
    audioonlycode = f"{self.audiomainnumber}-{nsufix}"
    return audioonlycode

  def get_audioonlycode_for_1baseidx(self, onebasedidx: int) -> str | None:
    i = onebasedidx - 1
    return self.get_audioonlycode_fr_idx(i)

  def traverse_sufix_n_twolettercode(self) -> Generator[tuple[int, str], Any, None]:
    """
    Traverses (loops over with yield [a generator]) the items in self.indict
    This method is "disconnected" with next(), beucase:
      1 - next() consumed a list that is initiated from self.indict
      2 - this method, on the contrary, loops over original self.indict
    """
    items = self.indict.items()
    items = sorted(items, key=lambda i: i[0])  # this keeps the ordering from least to greatest nsufix (the langnumber)
    for item in items:
      yield item

  def loop_over_langs(self) -> Generator[LangAttr, Any, None]:
    """
    In terms of functionality, the main attribute (or property) of this object
      is the dict_mapping of nsufix with 2-letter-code items

    This method loops over the these items transforming them into LangAttr objects.
      These 'langer' objects will be "consumed" in the client-caller that issues the
      yt-dlp download runs.

    :return:
    """
    for i, pair in enumerate(self.traverse_sufix_n_twolettercode()):
      seq_order = i + 1
      nsufix = pair[0]
      twolettercode = pair[1]
      langer = LangAttr(
        langless_audiocode=self.audiomainnumber,
        nsufix=nsufix,
        twolettercode=twolettercode,
        seq_order=seq_order
      )
      yield langer

  def __str__(self):
    outstr = f"""
    {self.indict}
    """
    return outstr


class SufixLanguageMapFinder:
  """
  DEPRECATED: this class will be substituted by the one above SufixLanguageMapper

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
      10: 'u1',  # unknown1 (the language set may grow to more ones)
      11: 'u2',  # unknown1
      12: 'en',  # unknown2
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

def fetch_langdict_w_videoformatoutput(videoformatoutput):
  """
  vfo = videoformatoutput
  TWOLETTER_N_LANGUAGENAME_DICTMAP.values()
  :param videoformatoutput:
  :return:
  """

  return {}


def adhoctest6():
  # testing strdict having 'unordered keys'
  strdict = '1:fr,0:de,5:it,2:es,11:en,8:ru'
  langmapper = SufixLanguageMapper(strdict)
  print(langmapper)
  for langer in langmapper.loop_over_langs():
    scrmsg = f"langer {langer}"
    print(scrmsg)


def adhoctest5():
  strdict = '0:en,1:pt'
  langmapper = SufixLanguageMapper(strdict)
  print(langmapper)
  for item in langmapper.traverse_sufix_n_twolettercode():
    print(item)
  first_2lett = langmapper.get_first_2lettlangcode()
  print('first_2lett', first_2lett)
  print(langmapper.dict_as_items_in_order)
  any_2lett = langmapper.get_ith_2lettlangcode_1idxbased(2)
  print('2lett 1bidx', 2, any_2lett)
  audioonlycode = langmapper.get_audioonlycode_fr_idx(0)
  scrmsg = f"audioonlycode for idx {0} = {audioonlycode}"
  print(scrmsg)
  audioonlycode = langmapper.get_audioonlycode_for_1baseidx(1)
  scrmsg = f"audioonlycode for 1-base idx {1} = {audioonlycode}"
  print(scrmsg)
  onebasedidx = 2
  audioonlycode = langmapper.get_audioonlycode_for_1baseidx(onebasedidx)
  scrmsg = f"audioonlycode for 1-base idx {onebasedidx} = {audioonlycode}"
  print(scrmsg)
  print(langmapper.audioonlycodes)


def adhoctest4():
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


def adhoctest3():
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


def adhoctest2():
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


def adhoctest1():
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
  adhoctest5()
  adhoctest6()
