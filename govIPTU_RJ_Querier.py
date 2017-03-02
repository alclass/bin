#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
govIPTU_RJ_Querier.py

This Python script was initially designed to query the SMF-RJ system on IPTU payments.
At the time of this writing the system accepts a GET-URL query with the following aspect:
http://www2.rio.rj.gov.br/smf/siam/consultaresult.asp?guiaux=%(n_guiaux)s&nrguia=%(n_guia)s&inscricao=%(n_inscricao_sem_dv)s&dv=%(verification_digit)s&exercicio=%(ano_exercicio)s&controle=%(letra_controle)s
'''
import os

class IPTU_Immeuble:
  '''
  class IPTU_Immeuble
  '''
  URL_BASE_IPTU_STATUS_OPENFREE_QUERY = 'http://www2.rio.rj.gov.br/smf/siam/consultaresult.asp?guiaux=%(n_guiaux)s&nrguia=%(n_guia)s&inscricao=%(n_inscricao_sem_dv)s&dv=%(verification_digit)s&exercicio=%(ano_exercicio)s&controle=%(letra_controle)s'

  def __init__(self, n_inscricao, n_guiaux = '00', n_guia = '00', ano_exercicio = None, letra_controle = 'S'):
    '''
    constructor

    :param n_inscricao:
    :param n_guiaux:
    :param n_guia:
    :param ano_exercicio:
    :param letra_controle:
    '''
    self.n_guiaux       = n_guiaux
    self.n_guia         = n_guia
    self.ano_exercicio  = ano_exercicio
    self.letra_controle = letra_controle
    self.n_inscricao    = n_inscricao

  @property
  def n_inscricao_sem_dv(self):
    return self.n_inscricao[:-1]

  @property
  def verification_digit(self):
    return self.n_inscricao[-1]

  @property
  def default_local_filename(self):
    default_local_filename_dict = {
      'n_guia': self.n_guia,
      'n_inscricao': self.n_inscricao,
      'ano_exercicio': self.ano_exercicio,
    }
    return '%(n_inscricao)s_%(ano_exercicio)s_g%(n_guia)s.html' %default_local_filename_dict

  def form_http_get_dict(self):
    return {
		  'n_guiaux'           : self.n_guiaux,
		  'n_guia'             : self.n_guia,
		  'n_inscricao_sem_dv' : self.n_inscricao_sem_dv,
		  'verification_digit' : self.verification_digit,
		  'ano_exercicio'      : self.ano_exercicio,
		  'letra_controle'     : self.letra_controle, 
	 }

  def form_url_iptu_query(self):
    return self.URL_BASE_IPTU_STATUS_OPENFREE_QUERY %self.form_http_get_dict()

  def form_download_wget_local_cli_str(self, local_filename = None):
    if local_filename == None:
      local_filename = self.default_local_filename
    iptu_url = self.form_url_iptu_query()
    wget_local_cli_str = 'wget -c "%(iptu_url)s" -O "%(local_filename)s"' %{'iptu_url':iptu_url, 'local_filename':local_filename}
    return wget_local_cli_str

  def download_wget_local(self, local_filename = None, online=True):
    '''

    :param local_filename:
    :param online:
    :return:
    '''

    comm = self.form_download_wget_local_cli_str(local_filename)
    if online:
      os.system(comm)
    else:
      print ('Mode OFFLINE:')
      print ('============:')
      iptu_url = self.form_url_iptu_query()
      print ('iptu_url: ', iptu_url)
      print ('local_filename: ', local_filename)


# Example for a url for fetching IPTU payment status
immeuble = None
def mount_n_return_example_immeuble_obj():
  global immeuble

  if immeuble ==None:
    immeuble = IPTU_Immeuble(
      n_guiaux='00',
      n_guia='01',
      n_inscricao='04569315',  # Costa Ferraz number
      ano_exercicio='2016',
      letra_controle='S',
    )
  return immeuble

def show_example_of_immeuble_url():
  '''

  :return:
  '''
  immeuble = mount_n_return_example_immeuble_obj()
  url = immeuble.form_url_iptu_query()
  print ('URL test')
  print (url)

def test_ad_hoc_1_assert_example_immeuble_url():
  print ('test_ad_hoc_1_assert_example_immeuble_url()')
  immeuble = mount_n_return_example_immeuble_obj()
  url = immeuble.form_url_iptu_query()
  expected_str = 'http://www2.rio.rj.gov.br/smf/siam/consultaresult.asp?guiaux=00&nrguia=01&inscricao=0456931&dv=5&exercicio=2016&controle=S'
  assert url == expected_str
  print ('OK passed Test 1')

def test_ad_hoc_2_assert_default_local_filename():
  print ('test_ad_hoc_2_assert_default_local_filename()')
  immeuble = mount_n_return_example_immeuble_obj()
  expected_str_for_local_filename = '04569315_2016_g01.html'
  assert immeuble.default_local_filename == expected_str_for_local_filename
  print ('OK passed Test 2')

def test_ad_hoc_3_assert_download_wget_comm():
  print ('test_ad_hoc_3_assert_download_wget_comm()')
  immeuble = mount_n_return_example_immeuble_obj()
  comm_from_obj = immeuble.form_download_wget_local_cli_str(None)
  url = immeuble.form_url_iptu_query()
  filename = immeuble.default_local_filename
  comm_expected = 'wget -c "%(url)s" -O "%(filename)s"' %{'url':url,'filename':filename}
  assert comm_from_obj == comm_expected
  print ('OK passed Test 3')

def tests_ad_hoc():
  test_ad_hoc_1_assert_example_immeuble_url()
  test_ad_hoc_2_assert_default_local_filename()
  test_ad_hoc_3_assert_download_wget_comm()

if __name__ == '__main__':
  tests_ad_hoc()
  show_example_of_immeuble_url()
