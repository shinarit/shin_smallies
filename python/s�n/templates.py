#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Datatypes:
  TEXT = 0
  LONGTEXT = 1
  DATE = 2
  LIST = 3
  READONLY = 4

class Empty:
  HedgehogBasic = {
    'Tenyészet'               : (0, ''),
    'Név'                     : (0, ''),
    'Becenév'                 : (0, ''),
    'Született'               : (2, ''),
    'Apa'                     : (3, ((), -1)),                #create list on creation, store value otherwise ('név | tenyészet',)
    'Anya'                    : (3, ((), -1)),                #create list on creation, store value otherwise ('név | tenyészet',)
    'Szín'                    : (0, ''),
    'Nem'                     : (3, (('Fiú', 'Lány'), -1)),
    'Egyéb'                   : (1, ''),
    'Tartózkodás'             : (3, (('Otthon', 'Máshol'), -1))
#    'Féreghajtás'             : (0, '')                       #2011.11.11;*
  }
  #prepare: Apa, Anya, Státusz, Féreghajtás
  #process: Apa, Anya

  HedgehogOwn = {
    'Érkezés'                 : (2, ''),
    'Távozás'                 : (2, ''),
    'Súly'                    : (0, ''),                      #2011.11.11:240[:státusz];*
    'Státusz'                 : (4, 'Saját')                  #set when created Saját, Kölyök, Vendég, Felmenő
  }
  
  HedgehogChild = {
    'Alom'                    : (3, ((), -1)),                #create list on creation
    'Távozás'                 : (2, ''),
    'Súly'                    : (0, ''),                      #2011.11.11:240;*
    'Gazdi neve'              : (0, ''),
    'Gazdi címe'              : (0, ''),
    'Gazdi email'             : (0, ''),
    'Gazdi telefonszáma'      : (0, ''),
    'Gazdival tegeződés'      : (3, (('Igen', 'Nem'), -1)),
    'Tenyészetbe ment'        : (3, (('Igen', 'Nem'), -1)),
    'Tenyészet neve'          : (0, ''),
    'Státusz'                 : (4, 'Kölyök')
  }
  
  HedgehogLitter = {
    'Dátum'                   : (2, ''),
    'Fiú'                     : (3, ((), -1)),                #create list on creation
    'Lány'                    : (3, ((), -1)),                #create list on creation
    'Név'                     : (0, ''),
    'Kölykök'                 : (0, '')                       #needs special care
  }
