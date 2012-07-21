#!/bin/python
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
    if 'Nem' == attr or 'Státusz' == attr:                       #list types
      return sun[attr][0][sun[attr][1]]
    if 'Apa' == attr or 'Anya' == attr:     #other hedgehogs
      return suns[sun[attr]]['Név']
    return str(sun[attr])
    
  def Clear(self):
    map(Label.destroy, self.labels.itervalues())
    self.labels.clear()

  def Reinitialize(self, toShow, data):
    self.Clear()
    self.Initialize(toShow, data)


textFont1 = ("Arial", 10, "bold italic")
textFont2 = ("Arial", 16, "bold")
textFont3 = ("Arial", 8, "bold")
 
class LabelWidget2(Tkinter.Entry):
  def __init__(self, master, x, y, text):
    self.text = Tkinter.StringVar()
    self.text.set(text)
    Tkinter.Entry.__init__(self, master=master)
    self.config(relief="ridge", font=textFont1,
          bg="#ffffff000", fg="#000000fff",
          readonlybackground="#ffffff000",
          justify='center',
          textvariable=self.text,
          state="readonly")
    self.grid(column=x, row=y)
 
class EntryWidget(Tkinter.Entry):
  def __init__(self, master, x, y, init = ''):
    Tkinter.Entry.__init__(self, master=master)
    self.value = Tkinter.StringVar()
    self.config(textvariable=self.value,
          relief="ridge", font=textFont1,
          bg="#ddddddddd", fg="#000000000",
          justify='center')
    self.grid(column=x, row=y)
    self.value.set(init)
 
 
class MainTable(Tkinter.Frame):
  def __init__(self, parent, desired, stuff):
    Tkinter.Frame.__init__(self, parent)
    self.cols = desired[:]
 
    self.datagrid = {}
 
# header
    column = 0
    for label in desired:
      LabelWidget2(self, column, 0, label)
      column += 1
 
    row = 1
 
# table
    for key, data in stuff.iteritems():
      column = 0
      for label in desired:
        val = ''
        if label in data:
          val = data[label]
        w = EntryWidget(self, column, row, val)
        self.datagrid[(0, label)] = w.value
        def handler(event, col = column, row = row):
          return self.__changehandler(col, row)
        w.bind(sequence="<FocusOut>", func = handler)
        column += 1
      row += 1
 
 
  def __changehandler(self, col, row):
    pass
 
class EntryGrid(Tkinter.Tk):
  ''' Dialog box with Entry widgets arranged in columns and rows.'''
  def __init__(self, colList, row, title="Entry Grid"):
    self.cols = colList[:]
    self.colList = colList[:]
    self.colList.insert(0, "")
    self.rows = row
    Tkinter.Tk.__init__(self)
    self.title(title)
 
    self.mainFrame = Tkinter.Frame(self)
    self.mainFrame.config(padx='3.0m', pady='3.0m')
    self.mainFrame.grid()
    self.make_header()
 
    self.gridDict = {}
    for i in range(0, len(self.colList)):
      for j in range(0, self.rows):
        w = EntryWidget(self.mainFrame, i, j+1)
        self.gridDict[(i-1,j)] = w.value
        def handler(event, col=i-1, row=j):
          return self.__entryhandler(col, row)
        w.bind(sequence="<FocusOut>", func=handler)
    self.mainloop()
 
  def make_header(self):
    self.hdrDict = {}
    for i, label in enumerate(self.colList):
      def handler(event, col=i, row=0, text=label):
        return self.__headerhandler(col, row, text)
      w = LabelWidget2(self.mainFrame, i, 0, label)
      self.hdrDict[(i,0)] = w
      w.bind(sequence="<KeyRelease>", func=handler)
 
  def __entryhandler(self, col, row):
    s = self.gridDict[(col,row)].get()
    if s.upper().strip() == "EXIT":
      self.destroy()
    elif s.strip():
      print s
 
  def __headerhandler(self, col, row, text):
    ''' has no effect when Entry state=readonly '''
    self.hdrDict[(col,row)].text.set(text)
 
  def get(self, x, y):
    return self.gridDict[(x,y)].get()
 
  def set(self, x, y, v):
    self.gridDict[(x,y)].set(v)
    return v
 
if __name__ == "__main__":
  cols = ['A', 'B', 'C', 'D']
  rows = 4
  tk = Tkinter.Tk()
  app= MainTable(tk, cols, {0:{'A':1, 'B': 2}, 'lol': {'B': 'musz', 'C': 14}, 'asd': {}})
  app.grid()
  app.mainloop()
  #app = EntryGrid(cols, rows)
 