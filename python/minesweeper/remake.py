#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
##  minesweeper with custom tiled grid  ##
##      author: tetra666@gmail.com      ##
##########################################

from Tkinter import *

class Field:
  grid = {}
  def __init__(self, isbomb, isvisible):
    self.isbomb = isbomb
    self.isvisible = isvisible
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
  
  

  #static method
  #generates a grid from an abstract size value (which is grid-dependent)
  #returns the "root" of the generated graph, it should be the middle element, but doesn't matter
  @staticmethod
  def buildGrid(size):
    return None    


class SquareField(Field):
  def __init__(self, isbomb, isvisible):


