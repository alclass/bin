#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import fundos

class Invest(object):
  def __init__(self, fundoId, evtDate, valorCota, valor):
    self.fundoId, self.evtDate, self.valorCota, self.valor = fundoId, evtDate, valorCota, valor
  def __str__(self):
    outStr = '%d %s %f %f' %(self.fundoId, self.evtDate, self.valorCota, self.valor)



fundoId = fundos.getFundoId('Petrobras', 'Itaú')

csvFile='2010-03-25 fundo Petrobras detalhado.csv'

csv.csvReader(csvFile)
tipo = pReader[1]

isAplic = True
isResgate = True

pos = tipo.find('APLICACAO')
if pos > -1:
  # ok a
  isAplic = True
  
pos = tipo.find('RESGATE')
if pos > -1:
  # ok a
  isResgate = True
  
if isAplic or isResgate:
  evtDate = pReader[0]
  valorCota =  pReader[3]
  valor = pReader[10]
  if isResgate:
    valor = -valor
  invObj = Invest(fundoId, evtDate, valorCota, valor)
  
    
  
  