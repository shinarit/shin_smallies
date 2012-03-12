#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
##  minesweeper with custom tiled grid  ##
##      author: tetra666@gmail.com      ##
##########################################

from Tkinter import *
import random

class Field:
  grid = {}
  def __init__(self, isbomb, isvisible, coord):
    self.isbomb = isbomb
    self.isvisible = isvisible
    self.coord = coord

    self.bombs = -1
    self.issigned = False

  def isBomb(self):
    return self.isbomb
  
  def setBomb(self, state = True):
    self.isbomb = state

  def isVisible(self):
    return self.isvisible

  def isSigned(self):
    return self.issigned

  def countBombs(self):
    if self.bombs == -1:
      #calculate
      pass
    return self.bombs
  
  #offset: (x, y) offset, the topleft corner of the drawing area
  #size: an abstract size value, determined by the actual class
  def getPolygon(self, offset, size):
    pass

  def getCenter(self, offset, size):
    pass

  #static method for the common part of grid creation
  #shouldnt be called from outside
  @staticmethod
  def buildGrid(coords, fieldtype):
    for coord in coords:
      Field.grid[coord] = fieldtype(False, False, coord)

  #bombnum tells how many bombs to place
  @staticmethod
  def fillBombs(bombnum):
    map(lambda field: field.setBomb(), random.sample(Field.grid.values(), bombnum))

  #rectangle: (left, top, width, height)
  #the screen it should draw in
  @classmethod
  def drawAll(cls, canvas, rectangle):
    size = cls.getSize((rectangle[2], rectangle[3]))

    offset = (rectangle[0], rectangle[1])
    map(lambda (coord, field): canvas.create_polygon(field.getPolygon(offset, size), fill = 'red', outline = 'black'), Field.grid.iteritems())

  #coords are the offset-corrected values within the rectangle
  #sizes are the (width, height) of the rectangle
  @classmethod
  def handleClick(cls, coords, sizes):
    dummy = Field.grid.itervalues().next()
    sizes = dummy.getSize(sizes)

    field = findField(coords, sizes)
    if field:
      pass

class SquareField(Field):
  DefSize = 100
  MyPolygon = ((0, 0), (DefSize, 0), (DefSize, DefSize), (0, DefSize))

  def __init__(self, isbomb, isvisible, coord):
    Field.__init__(self, isbomb, isvisible, coord)

  def getPolygon(self, offset, size):
    return map(lambda (x, y): (x*size/SquareField.DefSize + offset[0] + size*self.coord[0], y*size/SquareField.DefSize + offset[1] + size*self.coord[1]), SquareField.MyPolygon)

  def getCenter(self, offset, size):
    return (offset[0] + self.coord[0]*size + size//2, offset[1] + self.coord[1]*size + size//2)

  #sizes: (width, height)
  @staticmethod
  def getSize(sizes):
    botright = max(Field.grid.iterkeys())
    return min(sizes[0]/(botright[0] + 1), sizes[1]/(botright[1] + 1))

  #generates a grid from an abstract size value (which is grid-dependent)
  #size should be a pair of the width and height of the grid
  #returns the "root" of the generated graph, it should be the middle element, but doesn't matter
  @staticmethod
  def buildGrid(size):
    width, height = size
    Field.buildGrid(((x,y) for x in range(width) for y in range(height)), SquareField)



if __name__ == '__main__':
  tk = Tk()
  canvas = Canvas(tk)
  canvas.grid()
  grid = SquareField
  grid.buildGrid((20, 3))
  grid.fillBombs(10)
  grid.drawAll(canvas, (50, 50, 200, 200))
  tk.mainloop()

