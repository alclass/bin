#!/usr/bin/env python3
import glob, os

DEFAULT_SUBTITLE_EXT = '.srt'
DEFAULT_VIDEOFILE_EXT = '.mp4'

class Rename:
  '''

  '''
  def __init__(self, workfolder_absdir = None, no_confirm = False):
    self.videofile_ext = None
    self.subtitle_ext  = None
    self.videofilenames    = []; self.n_filenames = 0
    self.subtitlefilenames = []; self.n_subtitles = 0
    self.rename_pairs      = []; self.n_renames = 0
    self.workfolder_absdir = None
    self.set_workfolder_absdir(workfolder_absdir)
    self.no_confirm = no_confirm
    self.confirm_rename = False
    self.rename_process()

  def set_workfolder_absdir(self, workfolder_absdir):
    if self.workfolder_absdir is None:
      self.workfolder_absdir = os.path.




  def rename_process(self):
    '''

    :return:
    '''
    self.verify_defaults()
    self.load_video_n_subs_lists()
    self.prepare_for_rename()
    if self.confirm_rename:
      self.do_rename()
    self.show_numbers()

  def verify_defaults(self):
    '''

    :return:
    '''
    if self.videofile_ext is None:
      self.videofile_ext = DEFAULT_VIDEOFILE_EXT
    if self.subtitle_ext is None:
      self.subtitle_ext = DEFAULT_SUBTITLE_EXT

  def load_video_n_subs_lists(self):

    self.videofilenames = glob.glob('*' + self.videofile_ext)
    self.videofilenames = sorted( self.videofilenames )

    self.subtitlefilenames = glob.glob('*' + self.subtitle_ext)
    self.subtitlefilenames = sorted( self.subtitlefilenames )

    self.n_filenames = self.videofilenames
    self.n_subtitles = self.subtitlefilenames
    if len(self.n_filenames) != len(self.n_subtitles):
      error_msg = 'Number of videofiles (%d) is different than number of subtitles (%d)' %(self.n_filenames, self.n_subtitles)
      raise Except(error_msg)

  def prepare_for_rename(self):
    '''

    :return:
    '''

    for i, videofilename in enumerate(self.videofilenames):
      if not os.path.isfile(videofilename):
        continue
      videoname, _ = os.path.splitext(videofilename)
      subfilename = self.subtitlefilenames[i]
      _, subext = os.path.splitext(subfilename)
      subNewnamefile = videoname + subext
      if os.path.isfile(subNewnamefile):
        continue
      seq = i + 1
      print (seq, ' => Rename:')
      print ('FROM =>', subfilename )
      print ('BASE =>', videofilename )
      print ('TO   =>', subNewnamefile )
      rename_pair = (subfilename, subNewnamefile)
      self.rename_pairs.append(rename_pair)

    print ('n_rename_pairs', len(self.rename_pairs))

    if self.no_confirm:
      self.confirm_rename = True

    ans = input('Rename them (y/N) ? ')
    self.confirm_rename = False
    if ans in ['y', 'Y']:
      self.confirm_rename = True

  def do_rename(self):
    '''

    :return:
    '''
    self.n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      subfilename    = rename_pair[0]
      subNewnamefile = rename_pair[1]
      if not os.path.isfile(subfilename):
        continue
      if os.path.isfile(subNewnamefile):
        continue
      seq = i + 1
      print (seq, ' => Renaming now:')
      print ('FROM ', subfilename)
      print ('TO   ', subNewnamefile)
      os.rename(subfilename, subNewnamefile)
      self.n_renames += 1

  def show_numbers(self):
    '''

    :return:
    '''
    print ('Number of rename pairs:', len(self.rename_pairs))
    print ('Number of renamed:', self.n_renames)

def walkup_folders():
  entries = os.listdir('.')
  for entry in entries:
    if os.path.isdir(entry):
      absdir = os.path.absdir('.')
      workfolder_absdir = os.path.join(absdir, entry)






def process():
  Rename()

if __name__ == '__main__':
  process()
