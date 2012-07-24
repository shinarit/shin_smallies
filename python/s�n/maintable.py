#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import Tkinter

#class LabelWidget(Tkinter.Label):
class LabelWidget(Tkinter.Entry):
  def __init__(self, master, x, y, text):
    Tkinter.Entry.__init__(self, master = master)
    self.insert(0, text)
    self.config(state = 'readonly')
    self.grid(column = x, row = y)

class Table(Tkinter.Frame):
  def __init__(self, parent):
    Tkinter.Frame.__init__(self, parent)
    self.labels = {}

  #
  # toShow: [attr_to_show]
  # data: [{id: {'attr': value}}]
  #
  def Initialize(self, toShow, data):
    for column, item in enumerate(toShow):
      self.labels[(0, column)] = LabelWidget(self, column, 0, item)
    for row, sun in enumerate(data.iteritems()):
      for column, attr in enumerate(toShow):
        if attr in sun[1]:
          self.labels[(row + 1, column)] = LabelWidget(self, column, row + 1, self.GetAttribute(attr, sun[1], data))
   
  def GetAttribute(self, attr, sun, suns):
    print attr, ": ", sun[attr]
    if 'Nem' == attr or 'Tartózkodás' == attr:                       #list types
      index = sun[attr][1]
      if -1 != index:
        ret = sun[attr][0][index]
      else:
        ret = ''
    elif 'Apa' == attr or 'Anya' == attr:     #other hedgehogs
      ret = suns[sun[attr]]['Név']
    else:
      ret = sun[attr]
    if '' == ret:
      sun.pop(attr)
    return ret
    
  def Clear(self):
    map(LabelWidget.destroy, self.labels.itervalues())
    self.labels.clear()

  def Reinitialize(self, toShow, data):
    self.Clear()
    self.Initialize(toShow, data)
 
if __name__ == "__main__":
  cols = ['A', 'B', 'C', 'D']
  rows = 4
  tk = Tkinter.Tk()
  app= MainTable(tk, cols, {0:{'A':1, 'B': 2}, 'lol': {'B': 'musz', 'C': 14}, 'asd': {}})
  app.grid()
  app.mainloop()
  #app = EntryGrid(cols, rows)
 