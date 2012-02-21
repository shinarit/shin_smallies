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

  #static method for the common part of grid creation
  #shouldnt be called from outside
  @staticmethod
  def buildGrid(coords, fieldtype):
    for coord in coords:
      Field.grid[coord] = fieldtype(False, False, coord)


class SquareField(Field):
  def __init__(self, isbomb, isvisible, coord):
    Field.__init__(self, isbomb, isvisible, coord)

  #pos: topleft corner
  #size: size of the square
  def draw(self, canvas, pos, size):
    print pos, size

  @staticmethod
  def drawAll(canvas, width, height):
    botright = max(Field.grid.iterkeys())
    size = min(width/(botright[0] + 1), height/(botright[1] + 1))
    map(lambda (coord, field): field.draw(canvas, map(lambda x: x*size, coord), size), Field.grid.iteritems())


  #generates a grid from an abstract size value (which is grid-dependent)
  #size should be a pair of the width and height of the grid
  #returns the "root" of the generated graph, it should be the middle element, but doesn't matter
  @staticmethod
  def buildGrid(size):
    width, height = size
    Field.buildGrid(((x,y) for x in range(width) for y in range(height)), SquareField)
    return Field.grid[(width/2, height/2)]




