#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cookielib
from turulchan import Post
from time import sleep

from Tkinter import *
import tkFileDialog
import os

#ezt külön fájlba kéne pakolni, de úgy nehezebb a terjesztés :C
import Tkinter

class Meter(Tkinter.Frame):
    def __init__(self, master, width=300, height=20, bg='white', fillcolor='orchid1',\
                 value=0.0, text=None, font=None, textcolor='black', *args, **kw):
        Tkinter.Frame.__init__(self, master, bg=bg, width=width, height=height, *args, **kw)
        self._value = value

        self._canv = Tkinter.Canvas(self, bg=self['bg'], width=self['width'], height=self['height'],\
                                    highlightthickness=0, relief='flat', bd=0)
        self._canv.pack(fill='both', expand=1)
        self._rect = self._canv.create_rectangle(0, 0, 0, self._canv.winfo_reqheight(), fill=fillcolor,\
                                                 width=0)
        self._text = self._canv.create_text(self._canv.winfo_reqwidth()/2, self._canv.winfo_reqheight()/2,\
                                            text='', fill=textcolor)
        if font:
            self._canv.itemconfigure(self._text, font=font)

        self.set(value, text)
        self.bind('<Configure>', self._update_coords)

    def _update_coords(self, event):
        '''Updates the position of the text and rectangle inside the canvas when the size of
        the widget gets changed.'''
        # looks like we have to call update_idletasks() twice to make sure
        # to get the results we expect
        self._canv.update_idletasks()
        self._canv.coords(self._text, self._canv.winfo_width()/2, self._canv.winfo_height()/2)
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*self._value, self._canv.winfo_height())
        self._canv.update_idletasks()

    def get(self):
        return self._value, self._canv.itemcget(self._text, 'text')

    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        self._value = value
        if text == None:
            #if no text is specified use the default percentage string:
            text = str(int(round(100 * value))) + ' %'
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*value, self._canv.winfo_height())
        self._canv.itemconfigure(self._text, text=text)
        self._canv.update_idletasks()

#/ezt külön fájlba kéne pakolni, de úgy nehezebb a terjesztés :C

tablak = ('a', 'b', 'c', 'd', 'diy', 'f', 'g', 'int', 'k', 'm', 'p', 't', 'v', 'w', 'x', 'z', 'h', 's')
files = []
cookies=cookielib.CookieJar()

def SelectFiles():
  global files
  global tk
  res = tkFileDialog.askopenfilenames(parent = gui, title = 'Fájlok. Elég uncsi.')
  files = [file.decode('utf-8').encode('latin2') for file in tk.tk.splitlist(res)]

def SelectDir():
  global files
  res = tkFileDialog.askdirectory(parent = gui, title = 'Könyvtárválasztós dialógus. Húúúúú.')
  files = [res + '/' + file for file in os.listdir(res)]  
  files.sort()

def csapasd():
  global files
  
  global tablaVar
  global edits
  
  global progress
  
  for i, f in enumerate(files):
    value = float(i)/len(files)
    progress.set(value = value, text = f)
    done = False
    while not done:  
      err = 0
      try:
#        print 'Post(%s, %s, %s, cookies, %s, %s, %s)' % (tablaVar.get(), edits[0][1].get(), f, edits[1][1].get(), edits[2][1].get(), edits[3][1].get())
        print "Most megy:", f
        Post(tablaVar.get(), edits[0][1].get(), f, cookies, edits[1][1].get(), edits[2][1].get(), edits[3][1].get())
        done = True
      except Exception as e:
        err += 1
        progress.set(value = value, text = '%s ujra: %d' % (f, err))
        print "Valami végérvényesen :("
        print e
        sleep(10)
    print "Elszállt:", f
  progress.set(value = 0.0, text = 'Elszállt minden galambom...')


tk = Tk()
tk.title('TURULKAMION frontend')
gui = Frame()
gui.grid()
rowc = 0

tablaLabel = Label(gui, text = 'Tábla:')
tablaLabel.grid(column = 0, row = rowc, sticky = W)
tablaVar = StringVar()
tablaVar.set('b')
tablaOption = OptionMenu(gui, tablaVar, *tablak)
tablaOption.grid(column = 1, row = rowc, sticky = W)
rowc += 1

cats = ('Fonák', 'Név', 'Email', 'Üzenet')
edits = []
for item in cats:
  var = StringVar()
  edits.append((Label(gui, text = item), var, Entry(gui, textvariable = var, exportselection = False)))
  edits[-1][0].grid(column = 0, row = rowc, sticky = W)
  edits[-1][2].grid(column = 1, row = rowc, sticky = W)
  rowc += 1

fileLabel = Label(gui, text = 'Útelágazódáshoz érkeztél: fájlok ösvénye vagy a könyvtár misztériuma?')
fileLabel.grid(column = 0, columnspan = 2, row = rowc, sticky = W)
rowc += 1

filesButton = Button(gui, text = 'A fájlokat választom!', command = SelectFiles)
filesButton.grid(column = 0, row = rowc)
dirButton = Button(gui, text = 'Hol vannak a könyvtáraim?', command = SelectDir)
dirButton.grid(column = 1, row = rowc)
rowc += 1

sendButton = Button(gui, text = 'Szállj szállj, szabad madár!', command = csapasd)
sendButton.grid(column = 0, columnspan = 2, row = rowc)
rowc += 1

progress = Meter(gui, fillcolor = 'green', text = 'Ó, miért váratsz...')
progress.grid(column = 0, columnspan = 2, row = rowc)
rowc += 1

tk.mainloop()
