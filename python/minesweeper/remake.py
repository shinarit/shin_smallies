#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
##  minesweeper with custom tiled grid  ##
##      author: tetra666@gmail.com      ##
##########################################

from Tkinter import *

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

  #static method for the common part of grid creation
  #shouldnt be called from outside
  @staticmethod
  def buildGrid(coords, fieldtype):
    for coord in coords:
      Field.grid[coord] = fieldtype(False, False, coord)

  #rectangle: (left, top, width, height)
  #the screen it should draw in
  @staticmethod
  def drawAll(canvas, rectangle):
    size = Field.grid.itervalues().next().getSize(rectangle)
    offset = (rectangle[0], rectangle[1])
    canvas.create_polygon(self.getPolygon(offset, size))
    map(lambda (coord, field): field.draw(canvas, map(lambda c, o: o + c*size, coord, rectangle[0:2]), size), Field.grid.iteritems())


class SquareField(Field):
  def __init__(self, isbomb, isvisible, coord):
    Field.__init__(self, isbomb, isvisible, coord)

  #pos: topleft corner
  #size: size of the square
  def draw(self, canvas, pos, size):
    print (pos[0], pos[1], size, size)
    canvas.create_rectangle((pos[0], pos[1], size, size))

  #generates a grid from an abstract size value (which is grid-dependent)
  #size should be a pair of the width and height of the grid
  #returns the "root" of the generated graph, it should be the middle element, but doesn't matter
#  @staticmethod
#  def buildGrid(size):
#    width, height = size
#    Field.buildGrid(((x,y) for x in range(width) for y in range(height)), SquareField)
#    return Field.grid[(width/2, height/2)]



if __name__ == '__main__':
  tk = Tk()
  canvas = Canvas(tk)
  canvas.grid()
  SquareField.buildGrid((2, 3))
  SquareField.drawAll(canvas, (50, 50, 200, 200))
  tk.mainloop()

