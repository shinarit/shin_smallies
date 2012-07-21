#!/bin/python
# -*- coding: utf-8 -*-
 
from Tkinter import *
import cPickle as pickle

import maintable
import editwindow
import templates
from error import Error

class MainWindow(Frame):

  SunFile     =   'sunok.dat'
  Config = {  'desiredattributes' : ['Név', 'Becenév', 'Tenyészet', 'Született', 'Apa', 'Anya', 'Szín', 'Nem', 'Státusz', 'Tartózkodás', 'Utolsó féreghajtás', 'Egyéb']
                  }

  def __init__(self, root):
    Frame.__init__(self)
    self.root = root
    self.messagebus = []

    self.cfg = MainWindow.Config
    self.sunok = self.ReadDB(MainWindow.SunFile)
    #ReadDB('sün', MainWindow.SunFile, self.sunok)

    #omnom
    self.sunok = {1: {'Név' : 'elso sun', 'Tenyészet': 'elso tenyeszet', 'Nem': (('Fiú', 'Lány'), 0), 'Apa': 2, 'Státusz': (('Saját', 'Kölyök', 'Vendég', 'Felmenő'), 0)},
                  2: {'Név' : 'masodik sun', 'Tenyészet': 'masodik tenyeszet', 'Nem': (('Fiú', 'Lány'), 1), 'Anya': 1}}
    
    self.tbl = maintable.Table(self)
    self.tbl.Initialize(self.cfg['desiredattributes'], self.sunok)
    self.tbl.grid(row = 1, column = 0, columnspan = len(self.cfg['desiredattributes']))
    
    self.newsunbtn = Button(self, text = "Új sün felvétele", command = self.AddNewHedgie)
    self.newsunbtn.grid(row = 0, column = 1, pady = 20)
    
    self.typevar = StringVar()
    self.typebox = OptionMenu(self, self.typevar, *('Saját', 'Kölyök', 'Vendég', 'Felmenő'))
    self.typebox.grid(row = 0, column = 0)
   
    self.grid()
    
    self.editsunwnd = None

  def AddNewHedgie(self):
    if not self.editsunwnd:
      self.editsunwnd = editwindow.EditWindow(self.PrepareHedgieEdit(templates.Empty.HedgehogBasic.copy()), self.AddHedgieClosed)
      self.editsunwnd.grid()
    else:
      self.editsunwnd.focus_set()
  
  def AddHedgieClosed(self, val):
    print val
    
    self.editsunwnd = None

  def ReadDB(self, filename):
    try:
      file = open(filename, 'r')
    except IOError:
      self.messagebus.append('|ReadDB| %s: %s' % (Error.FileOpen, filename))
      return None

    try:
      db = pickle.load(file)
    except pickle.UnpicklingError:
      self.messagebus.append('|ReadDB| %s: üres adatbázis használata' % Error.Unpickle)
      return None

    return db

  def SaveDB(self, filename, db):
    try:
      file = open(filename, 'w')
    except IOError:
      self.messagebus.append('|SaveDB| %s: %s' % (Error.FileOpen, filename))
      return None

    try:
      pickle.dump(db, file)
    except pickle.PicklingError:
      self.messagebus.append('|SaveDB| %s' % Error.Pickle)
      return None

  def GetBoysGirls(self, hdg):
    delimiter = ' | '
    fiuk    = [delimiter.join((sun['Név'], sun['Tenyészet'])) for sun in self.sunok.itervalues() if sun['Nem'][0][sun['Nem'][1]] == 'Fiú']
    lanyok  = [delimiter.join((sun['Név'], sun['Tenyészet'])) for sun in self.sunok.itervalues() if sun['Nem'][0][sun['Nem'][1]] == 'Lány']
    fiuk.sort()
    lanyok.sort()
    print fiuk
    print lanyok

    try:
      fiuk.remove(delimiter.join((hdg['Név'][1], hdg['Tenyészet'][1])))
    except ValueError:
      pass
    try:
      lanyok.remove(delimiter.join((hdg['Név'][1], hdg['Tenyészet'][1])))
    except ValueError:
      pass

    fiuk = tuple(fiuk)
    lanyok = tuple(lanyok)
    
    return fiuk, lanyok    

  def PrepareHedgieEdit(self, hdg):
    #general: set daddy and mother names
    fiuk, lanyok = self.GetBoysGirls(hdg)
    
    if len(fiuk) == 0:
      fiuk = ('Nincs még kiválasztható fiú', )
    if len(lanyok) == 0:
      lanyok = ('Nincs még kiválasztható lány', )

    apa = hdg['Apa']
    if len(apa) == 1:
      try:
        apa = fiuk.index(apa)
      except ValueError:
        apa = -1
    else:
      apa = -1
    
    anya = hdg['Anya']
    if len(anya) == 1:
      try:
        anya = fiuk.index(anya)
      except ValueError:
        anya = -1
    else:
      anya = -1
    
    hdg['Apa'] = (3, (fiuk, apa))
    hdg['Anya'] = (3, (lanyok, anya))
    
    return hdg
