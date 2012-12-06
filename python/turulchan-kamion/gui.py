#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Module containing GUI for the image dumper.
"""

import cookielib
from turulchan import Post, GetMaxSize
from time import sleep
from Tkinter import *

import tkFileDialog, tkMessageBox
import os
import Tkinter
import threading

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

        

class Csapato(threading.Thread):
    """class so uploading is interactive"""
    def __init__(self, tablaVar, files, progress, edits, on_error, abort):
        self.tablaVar = tablaVar
        self.files = files
        self.progress = progress
        self.edits = edits
        self.on_error = on_error
        self.abort = abort
        self.cookies=cookielib.CookieJar()
        
        threading.Thread.__init__( self )

    def run(self):
        """Do uploading."""
        size = GetMaxSize(self.tablaVar.get(), self.cookies)
        fail = 0
        good = 0
        abort = False
        for i, f in enumerate(self.files):
            if abort:
                break
            value = float(i)/len(self.files)
            self.progress.set(value = value, text = f)
            done = False
            while not done:  
                err = 0
                try:
                    print "Most megy:", f
                    reply = Post(self.tablaVar.get(), self.edits[0][1].get(), f, self.cookies, self.edits[1][1].get(), self.edits[2][1].get(), self.edits[3][1].get(), password = self.edits[4][1].get(), max_size = size)
                    done = True
                    if '<h1 style="font-size: 3em;">Error</h1>' in reply:
                        error = reply.split('<h2 style="font-size: 2em;font-weight: bold;text-align: center;">')[1].split('</h2>')[0].strip()
                        print "Hiba!",error
                        fail += 1
                        if self.on_error:
                            tkMessageBox.showerror(message=error,title='Hiba')
                        if self.abort:
                            abort = True
                            break
                    else:
                        print "Elszállt:",f
                        good += 1
                except Exception as e:
                    err += 1
                    self.progress.set(value = value, text = '%s ujra: %d' % (f, err))
                    print "Valami végérvényesen :("
                    print e
                    sleep(10)
        self.progress.set(value = 0.0, text = 'Sikeresen elküldve: %d Sikertelen: %d'%(good,fail))
        
        
class KamionGUI:
    def SelectFiles(self):
        """Show file selecting dialog."""
        res = tkFileDialog.askopenfilenames(parent = self.gui, title = 'Fájlok. Elég uncsi.')
        self.files = [file for file in self.tk.tk.splitlist(res)]
        self.files.sort()

    def SelectDir(self):
        """Show ditectory selecting dialog."""
        res = tkFileDialog.askdirectory(parent = self.gui, title = 'Könyvtárválasztós dialógus. Húúúúú.')
        self.files = [res + '/' + file for file in os.listdir(res)]  
        self.files.sort()
#(self, tablaVar, files, progress, edits, on_error, abort):
    def csapasd(self):
        """Do uploading."""
        cs = Csapato(self.tablaVar, self.files, self.progress, self.edits, self.on_error, self.abort)
        cs.start()

    def PauseOnError(self,value):
        """Toggle showing of error dialog, which pauses dumping."""
        self.on_error = value

    def AbortOnError(self,value):
        """Toggle aborting on error."""
        self.abort = value

    def __init__(self):
        """Build GUI."""
        self.tablak = ('a', 'b', 'c', 'd', 'diy', 'f', 'g', 'int', 'k', 'm', 'p', 't', 'v', 'w', 'x', 'z', 'h', 's')
        self.files = []
        self.on_error = True # pause on error
        self.abort = False # abort on error
        self.tk = Tk()
        self.tk.title('TURULKAMION frontend')
        self.gui = Frame()
        self.gui.grid()
        rowc = 0
        tablaLabel = Label(self.gui, text = 'Tábla:')
        tablaLabel.grid(column = 0, row = rowc, sticky = W)
        self.tablaVar = StringVar()
        self.tablaVar.set('b')
        tablaOption = OptionMenu(self.gui, self.tablaVar, *self.tablak)
        tablaOption.grid(column = 1, row = rowc, sticky = W)
        rowc += 1
        cats = ('Fonák', 'Név', 'Email', 'Üzenet', 'Jelszó')
        self.edits = []
        for item in cats:
            var = StringVar()
            self.edits.append((Label(self.gui, text = item), var, Entry(self.gui, textvariable = var, exportselection = False)))
            self.edits[-1][0].grid(column = 0, row = rowc, sticky = W)
            self.edits[-1][2].grid(column = 1, row = rowc, sticky = W)
            rowc += 1
        fileLabel = Label(self.gui, text = 'Útelágazódáshoz érkeztél: fájlok ösvénye vagy a könyvtár misztériuma?')
        fileLabel.grid(column = 0, columnspan = 2, row = rowc, sticky = W)
        rowc += 1
        filesButton = Button(self.gui, text = 'A fájlokat választom!', command = self.SelectFiles)
        filesButton.grid(column = 0, row = rowc)
        dirButton = Button(self.gui, text = 'Hol vannak a könyvtáraim?', command = self.SelectDir)
        dirButton.grid(column = 1, row = rowc)
        rowc += 1
        sendButton = Button(self.gui, text = 'Szállj szállj, szabad madár!', command = self.csapasd)
        sendButton.grid(column = 0, columnspan = 2, row = rowc)
        rowc += 1
        self.progress = Meter(self.gui, fillcolor = 'green', text = 'Ó, miért váratsz...')
        self.progress.grid(column = 0, columnspan = 2, row = rowc)
        rowc += 1

    def Run(self):
        """Enter tk mainloop."""
        self.tk.mainloop()

if __name__=="__main__":
    a = KamionGUI()
    a.Run()
