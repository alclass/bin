#!/usr/bin/env python3
import os
import sys


class Renamer:
  
  def __init__(self, extension=None, number_of_zeroes=1,
               base_char_size=1, no_confirmation_prompt=False):
    if extension is None:
      raise ValueError('Extension should be entered.')
    self.extension = extension
    try:
      self.number_of_zeroes = int(number_of_zeroes)
      self.base_char_size = int(base_char_size)
    except ValueError:
      self.number_of_zeroes = 1
      self.base_char_size = 1
    self.no_confirmation_prompt = no_confirmation_prompt
    self.rename_pairs = []
    self.process()

  def process(self):
    self.search_renames()
    if self.no_confirmation_prompt or self.confirm_renames():
      self.do_renames()
    
  def search_renames(self):
    files = os.listdir('.')
    sorted(files)
    dot_extension = '.' + self.extension
    for filename in files:
      extless_name, extracted_ext = os.path.splitext(filename)
      if extracted_ext.lower() == dot_extension.lower():
        tam = len(extless_name)
        if tam == self.base_char_size:
          new_filename = '0'*self.number_of_zeroes + filename
          rename_pair = (filename, new_filename)
          self.rename_pairs.append(rename_pair)

  def confirm_renames(self):
    if len(self.rename_pairs) == 0:
      print('Nothing to rename.')
      return False
    for i, rename_pair in enumerate(self.rename_pairs):
      seq = i + 1
      print(seq, 'Rename:')
      old_name, new_name = rename_pair
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
    msg = 'Confirm the %d renames above ? (*Y/n) ' % len(self.rename_pairs)
    ans = input(msg)
    if ans in ['y', 'Y', '']:
      return True
    print('No renames were done.')
    return False
    
  def do_renames(self):
    print('-'*40)
    n_renames = 0
    for i, rename_pair in enumerate(self.rename_pairs):
      old_name, new_name = rename_pair
      seq = i + 1
      if not os.path.isfile(old_name):
        print('File [' + old_name + '] does not exist.')
        continue
      if os.path.isfile(new_name):
        print('File [' + new_name + '] already exists.')
        continue
      print(seq, 'Rename:')
      print('FROM: >>>%s' % old_name)
      print('TO:   >>>%s' % new_name)
      os.rename(old_name, new_name)
      n_renames += 1
    print('-'*40)
    print('Finished %d/%d renames.' % (n_renames, len(self.rename_pairs)))


def get_args():
  """
  Arguments:
      -e=<file's extension>
      -n=<number of zeroes>
      -b=<base char size>
      -y does not prompt for confirmation, it renames directly
  """
  extension = None
  number_of_zeroes = None
  base_char_size = None
  no_confirmation_prompt = False
  for arg in sys.argv:
    try:
      if arg == '-h' or arg == '--help':
        # print get_args.__doc__
        return None, None, None, False, get_args.__doc__
      elif arg.startswith('-e='):
        extension = arg[len('-e='):]
      elif arg.startswith('-n='):
        number_of_zeroes = arg[len('-n='):]
      elif arg.startswith('-b='):
        base_char_size = arg[len('-b='):]
      elif arg == '-y':
        no_confirmation_prompt = True
    except IndexError:
      pass
  return extension, number_of_zeroes, base_char_size, no_confirmation_prompt, None


def process():
  extension, number_of_zeroes, base_char_size, no_confirmation_prompt, help_text = get_args()
  if help_text is not None or extension is None:
    print(help_text)
    sys.exit(0)
  Renamer(extension, number_of_zeroes, base_char_size, no_confirmation_prompt)


if __name__ == '__main__':
  process()
