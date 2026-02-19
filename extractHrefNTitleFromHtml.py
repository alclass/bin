#!/usr/bin/env python3
"""
~/bin/extractHrefNTitleFromHtml.py
Extracts a pre-expected tuple from an XML-fragment.
This pre-expected tuple is as follows:

<a
  class="summary__link" href="/cdf/1811"
  title="Cours 1. Le meilleur des mondes possibles et le « problème du mal »"
>
They are found with the following 'logic':
    =======================
    for child in self.root:
      # from 'child', find all child's children named 'a'
      a_tag = child.findall('a')
      if len(a_tag) > 0:
        a_tag = child.findall('a')
        href = a_tag[0].attrib['href']  # it is expected only 1 element
        title = a_tag[0].attrib['title']
    =======================

Once this tuple is obtained, a wget-command may be issued to download and rename the htmlfile.
  @see on how the download-wget-command is mounted, properties curr_fn and curr_url
"""
import os
import sys
import lxml.etree as ET
chars_to_remove = ['.', ':', '?', '!']
default_fn = "z-htmls-to-download.xml.txt"
url_basedomain = 'https://books.openedition.org'


def remove_avoidable_chars_fr_str(stri):
  if stri is None or len(stri) == 0:
    return ""
  for char in chars_to_remove:
      stri = stri.replace(char, "")
  return stri


class Traverser:

  def __init__(self, fopath=None, fn=None, autoconfirmed=False):
    self.download_confirmed = False
    self.autoconfirmed = autoconfirmed
    self.fopath = fopath or os.getcwd()
    self.fn = fn or default_fn
    tree = ET.parse(self.fipath)
    self.root = tree.getroot()
    self.seq = 0
    self.curr_title = None
    self.curr_href = None
    self.curr_seq = None
    self.dictlist = []

  @property
  def fipath(self):
    return os.path.join(self.fopath, self.fn)

  @property
  def curr_idname(self):
    """
    Example of an expected href => href="/cdf/1811"
       from: class="summary__link" href="/cdf/1811"
    For the above exemple: curr_idname is 1811
    """
    if self.curr_href is not None:
      try:
        idname = self.curr_href.split('/')[-1]
        return idname
      except (AttributeError, IndexError):
        pass
    return ""

  @property
  def incoming_html_fn(self):
    title = self.curr_title.lstrip(' \t').rstrip(' \t\r\n')
    title = remove_avoidable_chars_fr_str(title)
    _html_fn = f"{self.curr_seq} id{self.curr_idname} {title}.html"
    _html_fn = _html_fn.replace("  ", " ").replace(" .", ".")
    return _html_fn

  @property
  def curr_url(self):
    _url = f"{url_basedomain}{self.curr_href}"
    return _url

  @property
  def wget_comm(self):
    comm = f'wget -c {self.curr_url} -O "{self.incoming_html_fn}"'
    return comm

  def set_currseq_currhref_currtitle(self, i, pdict):
    self.curr_seq = i + 1
    self.curr_href = pdict['href']
    self.curr_title = pdict['title']

  def roll_download(self):
    if not self.download_confirmed:
      scrmsg = "Download not confirmed, returning."
      print(scrmsg)
      return
    for i, pdict in enumerate(self.dictlist):
      self.set_currseq_currhref_currtitle(i, pdict)
      if self.curr_title is None:
        # curr_title is None when its related filename is already present in folder
        continue
      print(self.curr_seq, '=>', self.wget_comm)
      os.system(self.wget_comm)
    if len(self.dictlist) == 0:
      scrmsg = "No webpage to download, returning."
      print(scrmsg)
      return

  def remove_fr_dictlist_if_expectedfiles_present(self):
    i = 0
    while i < len(self.dictlist):
      pdict = self.dictlist[i]
      self.set_currseq_currhref_currtitle(i, pdict)
      expected_html_file_abspath = os.path.join(self.fopath, self.incoming_html_fn)
      if os.path.isfile(expected_html_file_abspath):
        print('\tFile has already been downloaded. Removing it from download list.')
        print('\t', self.incoming_html_fn)
        # this was thought-out so that (dynamic) seq_numbers are preserved in case some files are jumped over
        pdict['title'] = None
        continue
      i += 1

  def confirm_download(self):
    if self.autoconfirmed:
      self.download_confirmed = True
      return
    self.remove_fr_dictlist_if_expectedfiles_present()
    self.download_confirmed = False
    for i, pdict in enumerate(self.dictlist):
      self.set_currseq_currhref_currtitle(i, pdict)
      if self.curr_title is None:
        # curr_title is None when its related filename is already present in folder
        continue
      print(self.curr_seq, '=>', self.wget_comm)
    scrmsg = f"Confirm the {len(self.dictlist)} downloads above ? (Y, n) [ENTER] means Yes "
    ans = input(scrmsg)
    if ans in ['Y', 'y', '']:
      self.download_confirmed = True

  def traverse(self):
    for i, child in enumerate(self.root):
      # locseq = i + 1
      # print(locseq, child.attrib)
      # Find all immediate children named 'a'
      a_tag = child.findall('a')
      if len(a_tag) > 0:
        try:
          href = a_tag[0].attrib['href']
          title = a_tag[0].attrib['title']
          self.seq += 1
          pdict = {'href': href, 'title': title}
          print(pdict)
          self.dictlist.append(pdict)
        except (KeyError, IndexError):
          pass

  def process(self):
    self.traverse()
    self.confirm_download()
    self.roll_download()


def adhoctest1():
  """
  """
  pass


def get_args():
  fopath, fn, autoconfirmed = None, None, False
  for arg in sys.argv[1:]:
    if arg.startswith('-ac'):
      autoconfirmed = True
    elif arg.startswith('-dp='):
      fopath = arg[len('-dp='):]
    elif arg.startswith('-fn='):
      fn = arg[len('-fn='):]
  return fopath, fn, autoconfirmed


def process():
  fopath, fn, autoconfirmed = get_args()
  scrmsg = f"""Parameters:
  executing folder = [{fopath}]
  data filename = [{fn or "the default"}]
  rename-autoconfirmation = [{autoconfirmed}]
  """
  print(scrmsg)
  traverser = Traverser(
    fopath=fopath, fn=fn, autoconfirmed=autoconfirmed
  )
  traverser.process()


if __name__ == '__main__':
  """
  adhoctest1()
  process()
  """
  process()
