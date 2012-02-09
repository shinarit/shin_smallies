#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import random
import sys
import itertools

MAX_SIZE = 50

def Max(lhs, rhs):
  if lhs > rhs:
    return lhs
  else:
    return rhs

def Min(lhs, rhs):
  if lhs > rhs:
    return rhs
  else:
    return lhs

class TooManyBombs:
  pass

class Field:
  def __init__(self, isbomb, isvisible):
    self.isbomb = isbomb
    self.isvisible = isvisible
    self.bombs = 0
    self.issigned = False

def CalculateBomb(grid, orig, dist):
  res = 0
  collect = set([orig])
  for i in range(0, dist):
    toadd = set()
    for pos in collect:
      steps = grid.GetSteps(pos)
      for step in steps:
        toadd.add((pos[0] + step[0], pos[1] + step[1]))
    collect |= toadd
  
  for pos in collect:
    if grid.FindField(pos) and grid.FindField(pos).isbomb:
      res += 1

  return res

def ExpandZero(table, pos):
  grid = table.table
  zeros = set([pos])
  size = 0
  while size != len(zeros):
    size = len(zeros)
    toadd = set()
    for pos in zeros:
      grid[pos].isvisible = True
      Redraw(table, pos)
      steps = table.GetSteps(pos)
      for step in steps:
        newpos = (pos[0] + step[0], pos[1] + step[1])
        if table.FindField(newpos):
          grid[newpos].isvisible = True
          Redraw(table, newpos)
          if 0 == grid[newpos].bombs:
            toadd.add(newpos)
    zeros |= toadd

def FillTable(poslist, bombnum, grid):
  table = {}
  num = 0
  for pos in poslist:
    table[pos] = Field(False, False)
    num += 1
  if num < bombnum:
    raise TooManyBombs()
  
  places = table.keys()
  i = 0
  while i < bombnum :
    field = table[places[random.randint(0, len(places) - 1)]]
    if not field.isbomb :
      field.isbomb = True
      i += 1

  return table


def CalculateBombs(grid, dist):
  places = grid.table.keys()
  for place in places:
    grid.table[place].bombs = CalculateBomb(grid, place, dist)


def CreateCanvas(grid):
  canvas = Canvas(grid.tk)
  canvas.pack(side='top', fill='both')
  canvas.xview_moveto(0)
  canvas.yview_moveto(0)
  canvas["bg"] = "white"
  canvas["width"] = 800
  canvas["height"] = 600

  canvas.bind('<Button-1>', grid.Click)
  canvas.bind('<Button-3>', grid.RightClick)
  
  return canvas

def HandleClick(table, event):
  pos = table.FindPos(event.x, event.y)
  if pos:
    print pos[0], pos[1]
    field = table.table[pos]
    print field.bombs
    if field.isvisible:
      return
    if field.isbomb:
      for f in table.table:
        table.table[f].isvisible = True
      RedrawAll(table)
    else:
      field.isvisible = True
      if 0 == field.bombs:
        ExpandZero(table, pos)
      Redraw(table, pos)
  else:
    print 'not found'

def HandleRightClick(table, event):
  pos = table.FindPos(event.x, event.y)
  field = table.FindField(pos)
  if field:
    field.issigned = not field.issigned
    Redraw(table, pos)

def RedrawAll(table):
  for field in table.table.iteritems():
    bg = 'gray'
    if field[1].issigned:
      text = '!'
      bg = 'dim gray'
    else:
      text = ''
    if field[1].isvisible:
      bg = 'white'
      if field[1].isbomb:
        text = 'B'
      elif field[1].bombs != 0:
        text = str(field[1].bombs)
    
    field = table.GetCoords(field[0])
    table.DrawField(field[0], field[1], txt = text, fill = bg)

def Redraw(table, pos):
  field = table.FindField(pos)
  if field.issigned:
    text = '!'
  else:
    text = ''
  bg = 'gray'
  if field.isvisible:
    bg = 'white'
    if field.isbomb:
      text = 'B'
    elif field.bombs != 0:
      text = str(field.bombs)
  
  field = table.GetCoords(pos)
  table.DrawField(field[0], field[1], txt = text, fill = bg)

#
# ----------------------------------------------------------------------------------------
#


class Grid():
  def __init__(self, sizex, sizey, bombnum, dist):
    self.fieldsize = 30

    self.tk = Tk()

    self.table = FillTable(((x,y) for x in range(sizex) for y in range(sizey)), bombnum, self)
    
    CalculateBombs(self, dist)

    self.canvas = CreateCanvas(self)
    self.canvas.grid()
    
    width = int(self.canvas.cget('width'))
    height = int(self.canvas.cget('height'))
    
    self.fieldsize = Min(width/sizex, height/sizey)
    self.padx = (width - sizex*self.fieldsize) / 2
    self.pady = (height - sizey*self.fieldsize) / 2

    RedrawAll(self)

    self.tk.mainloop()

  def DrawField(self, x, y, fill = 'gray', outline = 'black', txt = ''):
    size = self.fieldsize
    self.canvas.create_polygon([(x, y), (x + size, y), (x + size, y + size), (x, y + size)], fill = fill, outline = "black")
    self.canvas.create_text((x + size/2, y + size/2), text = txt)

  def Click(self, event):
    HandleClick(self, event)

  def RightClick(self, event):
    HandleRightClick(self, event)

  def FindPos(self, x, y):
    pos = ((x - self.padx)/self.fieldsize, (y - self.pady)/self.fieldsize)
    if pos in self.table:
      return pos
    else:
      return None
  
  def FindField(self, pos):
    return self.table.get(pos)

  def GetSteps(self, pos):
    return ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))

  def GetCoords(self, pos):
    return (self.padx + pos[0]*self.fieldsize, self.pady + pos[1]*self.fieldsize)

class Hexgrid():
  def __init__(self, sizex, sizey, bombnum, dist):
    self.fieldsize = 30

    self.tk = Tk()

    self.table = FillTable(((x,y) for x in range(sizex) for y in range(sizey)), bombnum, self)
    
    CalculateBombs(self, dist)

    self.canvas = CreateCanvas(self)
    self.canvas.grid()
    
    width = int(self.canvas.cget('width'))
    height = int(self.canvas.cget('height'))
    
    self.fieldsize = Min(width/(sizex + 1), height/sizey)
    self.padx = (width - sizex*self.fieldsize) / 4
    self.pady = (height - sizey*self.fieldsize * 3 / 4) / 2

    RedrawAll(self)

    self.tk.mainloop()

  def DrawField(self, x, y, fill, txt):
    size = self.fieldsize
    self.canvas.create_polygon([(x, y + size/4), (x, y + size*3/4), (x + size/2, y + size), (x + size, y + size*3/4), (x + size, y + size/4), (x + size/2, y)], fill = fill, outline = "black")
    self.canvas.create_text((x + size/2, y + size/2), text = txt)

  def Click(self, event):
    HandleClick(self, event)

  def RightClick(self, event):
    HandleRightClick(self, event)

  def FindPos(self, x, y):
    pos = min((pow(x - self.GetCoords(pos)[0] - self.fieldsize/2, 2) + pow(y - self.GetCoords(pos)[1] - self.fieldsize/2, 2), pos) for pos in self.table.iterkeys())[1]
    if (pow(x - self.GetCoords(pos)[0] - self.fieldsize/2, 2) + pow(y - self.GetCoords(pos)[1] - self.fieldsize/2, 2)) <= pow(self.fieldsize / 2, 2):
      return pos
    else:
      return None

  def FindField(self, pos):
    return self.table.get(pos)

  def GetSteps(self, pos):
    if 0 == pos[1]%2:
      return ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))
    else:
      return ((1, 0), (0, 1), (1, 1), (-1, 0), (1, -1), (0, -1))

  def GetCoords(self, pos):
    return (self.padx + pos[0]*self.fieldsize + (pos[1]%2)*self.fieldsize/2, self.pady + pos[1]*self.fieldsize*3/4)


class Trigrid():
  def __init__(self, sizex, sizey, bombnum, dist):
    self.fieldsize = 30

    self.tk = Tk()

    self.table = FillTable(((x,y) for x in range(sizex) for y in range(sizey)), bombnum, self)
    
    CalculateBombs(self, dist)

    self.canvas = CreateCanvas(self)
    self.canvas.grid()
    
    width = int(self.canvas.cget('width'))
    height = int(self.canvas.cget('height'))
    
    self.fieldsize = Min(width/(sizex + 1), height/sizey)
    self.padx = (width - sizex*self.fieldsize) / 4
    self.pady = (height - sizey*self.fieldsize * 3 / 4) / 2

    RedrawAll(self)

    self.tk.mainloop()

  def DrawField(self, x, y, fill, txt):
    size = self.fieldsize
    pos = self.FindPos(x + size/2, y + size/2)
    if 0 == (pos[0] + pos[1]) % 2:
      self.canvas.create_polygon([(x, y), (x + size, y), (x + size / 2, y + size)], fill = fill, outline = "black")
    else:
      self.canvas.create_polygon([(x, y + size), (x + size, y + size), (x + size / 2, y)], fill = fill, outline = "black")
    self.canvas.create_text((x + size/2, y + size/2), text = txt)

  def Click(self, event):
    HandleClick(self, event)

  def RightClick(self, event):
    HandleRightClick(self, event)

  def FindPos(self, x, y):
    pos = min((pow(x - self.GetCoords(pos)[0] - self.fieldsize/2, 2) + pow(y - self.GetCoords(pos)[1] - self.fieldsize/2, 2), pos) for pos in self.table.iterkeys())[1]
    if (pow(x - self.GetCoords(pos)[0] - self.fieldsize/2, 2) + pow(y - self.GetCoords(pos)[1] - self.fieldsize/2, 2)) <= pow(self.fieldsize / 2, 2):
      return pos
    else:
      return None

  def FindField(self, pos):
    return self.table.get(pos)

  def GetSteps(self, pos):
    if 0 == pos[1]%2:
      return ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))
    else:
      return ((1, 0), (0, 1), (1, 1), (-1, 0), (1, -1), (0, -1))

  def GetCoords(self, pos):
    return (self.padx + pos[0]*self.fieldsize / 2, self.pady + pos[1]*self.fieldsize)



if __name__ == "__main__":
  random.seed()
#grids parameters: width, height, bomb numbers, sensor distance
#  g = Grid(10, 10, 5, 1)
  g = Hexgrid(20, 15, 15, 3)
#  g = Trigrid(20, 10, 3, 1)

