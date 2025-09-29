#!/usr/bin/env python3
"""
~/bin/cookiesFilter.py
Filters a subset of cookies.json to another file, say, cookies-filtered.json.

  For the time being, the json search-subset contains the following dict hardcoded:
    {"domain": ".youtube.com"}

  This means that all elements containing that key-pair will be taken to the output json file.
  The practical effect is that all cookies from youtube.com will be taken to the output file
     and those from other domains will not.

  See the following to-do for an addition of an input parameter that a subset-search-json-file
    may be entered as input to contain the key-value pairs that, in being in cookies.txt,
    will be transposed to the output cookies-filtered.json.

TODO:
  1 - establish an input parameter to inform a filename/filepath
  2 - this filename/filepath is for a jsonfile containing the cookies-search-subset
"""
import json
import os
hdir = os.path.expanduser("~")
default_inputfilename = 'cookies.json'
default_outputfilename = 'cookies-youtube.json'
default_datafolder_relpath = 'bin/bin_non_gitable'
default_filter_dict = {'domain': ".youtube.com"}


def get_datafolderpath():
  return os.path.join(hdir, default_datafolder_relpath)


class CookiesFilter:

  def __init__(self, filterdict=None):
    self.filterdict = filterdict or default_filter_dict
    self._filterset = None
    self.indictlist = []
    self.outdictlist = []
    self.filtered_count = 0

  @property
  def filterset(self):
    """
    The filterset is the form in which a subset search will occur

    To find out if the search-dict-element is contained in the dict-elem
      (i.e., it's a subset of it), the dict is transformed to set and
      set has a built-in method named .issubset()

    @see also the filter() method with this 'set-contains-subset' piece of coded
    """
    if self._filterset is None:
      self._filterset = set(self.filterdict.items())
    return self._filterset

  @property
  def infilepath(self):
    ifp = os.path.join(get_datafolderpath(), default_inputfilename)
    if not os.path.isfile(ifp):
      errmsg = f"Error: infilepath {ifp} does not exist."
      raise OSError(errmsg)
    return ifp

  @property
  def outfilepath(self):
    """
    Returns the output filepath
    Notice that this file may not exist, so os.path.isfile() is not used
    """
    ofp = os.path.join(get_datafolderpath(), default_outputfilename)
    return ofp

  @property
  def inputsize(self):
    _is = len(self.indictlist)
    return _is

  def read_input_dictlist_from_json(self):
    jsontext = open(self.infilepath).read()
    self.indictlist = json.loads(jsontext)

  def filter(self):
    self.outdictlist = []
    for eachdict in self.indictlist:
      try:
        largerset = set(eachdict.items())
      except TypeError:
        # some dict-elements (probably empty) are not hashable, so loop on for next one
        continue
      if self.filterset.issubset(largerset):
        # found an element that has (contains) the search-dict
        self.filtered_count += 1
        seq = self.filtered_count
        scrmsg = f"{seq} Found a match {largerset}"
        print(scrmsg)
        print('domain', eachdict['domain'])
        self.outdictlist.append(eachdict)

  def write_outfile(self):
    """
    Writes the output json file
    """
    scrmsg = f"Writing filtered json to [{self.infilepath}]"
    print(scrmsg)
    fd = open(self.outfilepath, 'w')
    text = json.dumps(self.outdictlist)
    fd.write(text)
    fd.close()

  def process(self):
    self.read_input_dictlist_from_json()
    self.filter()
    self.report()
    self.write_outfile()

  def report(self):
    outstr = f"""{self}
    input dict from json total elements = {self.inputsize}
    output dict to json total elements = {len(self.outdictlist)}
    """
    return outstr

  def __str__(self):
    outstr = f"""{self.__class__.__name__} | Filters a cookies text file to a subset
    inputfilepath = {self.infilepath}
    outputfilepath = {self.outfilepath}
    """
    return outstr


def process():
  """
  """
  cf_o = CookiesFilter()
  cf_o.process()


if __name__ == '__main__':
  """
  adhoctest1()
  adhoctest2()
  """
  process()
