#!/bin/python
# -*- coding: utf-8 -*-
 
from Tkinter import *
import re

from templates import Datatypes

TextHeight = 3
NewValuePadding = 10
DateMatch = re.compile(r'[0-9]{4}\.[0-9][0-9]?\.[0-9][0-9]?\.?$')

def OnClose(wnd, callback):
  wnd.destroy()
  callback()

class Header:
  def __init__(self, parent, i = 0):
    self.namelabel = Label(parent, text='A tulajdonság neve')
    self.vallabel = Label(parent, text='A tulajdonság értéke')
    self.namelabel.grid(column = 0, row = i)
    self.vallabel.grid(column = 1, row = i)

class Value:
  def __init__(self, parent, key, item, i):
    self.namelabel = Label(parent, text = key)
    self.namelabel.grid(column = 0, row = i, sticky = N+W)
    
    self.type, value = item
    
    #simple string
    if self.type == Datatypes.TEXT:
      self.value = StringVar()
      self.value.set(value)
      self.valuebox = Entry(parent, textvariable = self.value, exportselection = False)
      
    #simple string
    elif self.type == Datatypes.LONGTEXT:
      self.valuebox = Text(parent, height = TextHeight)
      self.valuebox.insert(END, value)
      #self.valuebox.get(1.0 END)
      
    #simple string
    elif self.type == Datatypes.DATE:
      self.value = StringVar()
      if DateMatch.match(value):
        self.value.set(value)
      else:
        self.value.set("%s: Értelmetlen dátum" % value)
      self.valuebox = Entry(parent, textvariable = self.value, exportselection = False)
      
    #([list of values], selected index, -1 if none)
    elif self.type == Datatypes.LIST:
      self.value = StringVar()
      self.valuelist, index = value
      if -1 == index:
        txt = 'Válassz!'
      else:
        txt = self.valuelist[index]
      self.value.set(txt)
      self.valuebox = OptionMenu(parent, self.value, *self.valuelist)
    
    elif self.type == Datatypes.READONLY:
      self.value = value
      self.valuebox = Label(parent, text = self.value)

    else:
      pass #error
    
    self.valuebox.grid(column = 1, row = i, sticky = W)
  
  def GetValue(self):
    #simple string
    if self.type == Datatypes.TEXT:
      return self.value.get()
      
    #simple string
    elif self.type == Datatypes.LONGTEXT:
      return self.valuebox.get(1.0, END)
      
    #simple string
    elif self.type == Datatypes.DATE:
      txt = self.value.get()
      if None == DateMatch.match(txt):
        pass #error
      return self.value.get()
      
    #([list of values], selected index, -1 if none)
    elif self.type == Datatypes.LIST:
      try:
        index = self.valuelist.index(self.value.get())
      except ValueError:
        index = -1
      return (self.valuelist, index)

    elif self.type == Datatypes.READONLY:
      return self.value

    else:
      pass #error
    

#
# args: (name, (datatype, value))
#
class EditWindow(Frame):
  def __init__(self, args, callback):
    self.root = Toplevel()
    Frame.__init__(self, self.root)
    self.root.protocol('WM_DELETE_WINDOW', lambda wdw = self.root: self.OnClose(wdw, callback))
    self.callback = callback

    self.header = Header(self)
    
    self.values = []
    for i, (key, item) in enumerate(args.iteritems()):
      self.values.append((key, Value(self, key, item, i + 1)))
    
    self.value = None
    self.Ok = Button(self, text = "Oké", command = self.OnOk)
    self.Cancel = Button(self, text = "Mégcse", command = lambda wdw = self.root: self.OnClose(wdw, callback))
    self.Ok.grid(column = 0, row = len(self.values) + 2)
    self.Cancel.grid(column = 1, row = len(self.values) + 2)
  
  def OnOk(self):
    self.value = {}
    for name, value in self.values:
      self.value[name] = value.GetValue()
    self.OnClose(self.root, self.callback)
  
  def OnClose(self, wnd, callback):
    wnd.destroy()
    callback(self.value)
    