#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##        Author: Kovács Márton, unsigned.t@gmail.com, 2011                  ##
##                Snake game with multiple panels                            ##
###############################################################################

from Tkinter import *
import sys
import time
import random

class Direction:
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

class Graphics:
  FREE = 0
  BLOCK = 1

#####################################################################################
##     format: every data on new line, no empty lines                              ##
##     order: width, height, map data (sorfolytonos), snake startpositions         ##
#####################################################################################

class Map:
  def __init__(self, iterated):
    self.width = int(iterated.next())
    self.height = int(iterated.next())

    self.map = {}
    runx = 0
    runy = 0
    for coord in ((x,y) for y in range(self.height) for x in range(self.width)):
      self.map[coord] = int(iterated.next())

    self.snake = []
    for sn in iterated:
      (x, y) = sn.rstrip().split(';')
      self.snake.append((int(x), int(y)))

class Main:
  snake     = []
  map       = {}
  direction = Direction.RIGHT
  togo      = Direction.RIGHT
  food      = []
  PIXSIZE = 10                  # minimum 10
  SMALL_OFFSET = PIXSIZE/10
  NORMAL_OFFSET = PIXSIZE/5
  LARGE_OFFSET = 3*PIXSIZE/10
  MAPWIDTH = 20
  MAPHEIGHT = 15
  speed = 2000
  tim = time.time()
  
  def __init__(self):
    print Main.PIXSIZE, Main.SMALL_OFFSET, Main.NORMAL_OFFSET, Main.LARGE_OFFSET
    self.root = Tk()
    self.pause = False
    
    self.root.bind('<Up>', self.handleKeys)
    self.root.bind('<Down>', self.handleKeys)
    self.root.bind('<Left>', self.handleKeys)
    self.root.bind('<Right>', self.handleKeys)
    self.root.bind('p', self.handlePause)
    
    m = Map(open(Main.map, 'r'))
    Main.snake  = m.snake
    Main.map    = m.map
    Main.MAPWIDTH    = m.width
    Main.MAPHEIGHT   = m.height
   
    Main.food = [self.findFood()]

    self.windows = []
    self.createWindow(0, 1)
    self.createWindow(1, 1)
    self.createWindow(2, 1)
    self.createWindow(1, 0)
    self.createWindow(1, 2)

    self.windows[0].after(500, self.moveSnake)
    self.root.mainloop()

  def createWindow(self, x, y):
    win = Window(self.root);
    win.grid(row = y, column = x)
    self.windows.append(win)
    

  def findFood(self):
    try:
      return random.choice([coord for (coord, value) in Main.map.iteritems() if value == Graphics.FREE and (coord not in Main.snake)])
    except IndexError:
     return None

  def moveSnake(self):
    tim2 = time.time()
  
    if self.pause:
      return
  
    Main.direction = Main.togo
    if Main.direction == Direction.UP:
      Main.snake.insert(0, (Main.snake[0][0], (Main.snake[0][1] - 1) % Main.MAPHEIGHT))
    elif Main.direction == Direction.LEFT:
      Main.snake.insert(0, ((Main.snake[0][0] - 1) % Main.MAPWIDTH , Main.snake[0][1]))
    elif Main.direction == Direction.DOWN:
      Main.snake.insert(0, (Main.snake[0][0], (Main.snake[0][1] + 1) % Main.MAPHEIGHT))
    elif Main.direction == Direction.RIGHT:
      Main.snake.insert(0, ((Main.snake[0][0] + 1) % Main.MAPWIDTH, Main.snake[0][1]))

    if Main.snake[0] in Main.food:
      Main.food.remove(Main.snake[0])
      food = self.findFood()
      if food:
        Main.food.append(food)
      else:
        self.pause = True
        for window in self.windows:
          window.canvas.create_text((Main.MAPWIDTH*Main.PIXSIZE/2, Main.MAPHEIGHT*Main.PIXSIZE/2), fill='red', text='YOU WON', font=("Arial", 16, "bold"))
        return
    else:
      Main.snake.pop(-1)

    dest = Main.map[Main.snake[0]]
    if Main.snake[0] in Main.snake[1:] or dest == Graphics.BLOCK:
      self.pause = True
      for window in self.windows:
        window.canvas.create_text((Main.MAPWIDTH*Main.PIXSIZE/2, Main.MAPHEIGHT*Main.PIXSIZE/2), fill='red', text='YOU LOST', font=("Arial", 16, "bold"))
        window.canvas.create_rectangle(Main.snake[0][0]*Main.PIXSIZE + 1, Main.snake[0][1]*Main.PIXSIZE + 1, Main.snake[0][0]*Main.PIXSIZE + Main.PIXSIZE - 2, Main.snake[0][1]*Main.PIXSIZE + Main.PIXSIZE - 2, fill="", outline="red")
      return

    for win in self.windows:
      win.updateMap()

    self.windows[0].after(Main.speed, self.moveSnake)

    tim3 = time.time()
#    print 'Between calls: %d The call: %d The should be: %d' % (int(1000*(tim2 - Main.tim)), int(1000*(tim3 - tim2)), Main.speed)
    Main.tim = tim2
  
  def handleKeys(self, event):
    if 'Up' == event.keysym       and Main.direction != Direction.DOWN:
      Main.togo = Direction.UP
    elif 'Left' == event.keysym   and Main.direction != Direction.RIGHT:
      Main.togo = Direction.LEFT
    elif 'Down' == event.keysym   and Main.direction != Direction.UP:
      Main.togo = Direction.DOWN
    elif 'Right' == event.keysym  and Main.direction != Direction.LEFT:
      Main.togo = Direction.RIGHT

  def handlePause(self, event):
    self.pause = not self.pause
    if not self.pause:
      self.windows[0].after(Main.speed, self.moveSnake)

def pairs(lst):
    i = iter(lst)
    first = prev = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first

#draw piece by piece, simple squares with a bigger head
#you cant really tell the direction in which the segments will fold up
def OrigDrawSnake(canvas):
  for coord in Main.snake:
    canvas.create_rectangle(coord[0]*Main.PIXSIZE + Main.NORMAL_OFFSET, coord[1]*Main.PIXSIZE + Main.NORMAL_OFFSET, coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, fill="gray")
  coord = Main.snake[0]
  canvas.create_rectangle(coord[0]*Main.PIXSIZE + Main.SMALL_OFFSET, coord[1]*Main.PIXSIZE + Main.SMALL_OFFSET, coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.NORMAL_OFFSET, coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.NORMAL_OFFSET, fill="gray")

def DrawSegment(canvas, coord, direction):
  if Direction.UP == direction:
    canvas.create_rectangle(  coord[0]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.SMALL_OFFSET,
                              coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, fill="gray", outline="gray")
    canvas.create_rectangle(  coord[0]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, fill="gray", outline="gray")
  elif Direction.DOWN == direction:
    canvas.create_rectangle(  coord[0]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.NORMAL_OFFSET, fill="gray", outline="gray")
  elif Direction.LEFT == direction:
    canvas.create_rectangle(  coord[0]*Main.PIXSIZE + Main.SMALL_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, fill="gray", outline="gray")
  elif Direction.RIGHT == direction:
    canvas.create_rectangle(  coord[0]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.NORMAL_OFFSET,
                              coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.NORMAL_OFFSET,
                              coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, fill="gray", outline="gray")
#  canvas.create_rectangle(  coord[0]*Main.PIXSIZE + Main.NORMAL_OFFSET,
#                            coord[1]*Main.PIXSIZE + Main.NORMAL_OFFSET,
#                            coord[0]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET,
#                            coord[1]*Main.PIXSIZE + Main.PIXSIZE - Main.LARGE_OFFSET, fill="gray")

def DrawPair(canvas, first, second):
  if -1 == (first[0] - second[0]) or 1 < (first[0] - second[0]):    #first is left from second (or through the edge)
    DrawSegment(canvas, first, Direction.RIGHT)
    DrawSegment(canvas, second, Direction.LEFT)
  elif 1 == (first[0] - second[0]) or -1 > (first[0] - second[0]):  #first is right from second (or through the edge)
    DrawSegment(canvas, first, Direction.LEFT)
    DrawSegment(canvas, second, Direction.RIGHT)
  elif -1 == (first[1] - second[1]) or 1 < (first[1] - second[1]):  #first is up from second (or through the edge)
    DrawSegment(canvas, first, Direction.DOWN)
    DrawSegment(canvas, second, Direction.UP)
  else:                                                             #first is down from second (or through the edge)
    DrawSegment(canvas, first, Direction.UP)
    DrawSegment(canvas, second, Direction.DOWN)

#draw by pairs
#you can see the direction but not so easy and its ugly
def DrawSnake(canvas):
  for i in range(0, len(Main.snake) - 1):
    DrawPair(canvas, Main.snake[i], Main.snake[i+1])
#  for (first, second) in pairs(Main.snake):
#    DrawPair(canvas, first, second)
  coord = Main.snake[0]
  canvas.create_rectangle(coord[0]*Main.PIXSIZE + 1, coord[1]*Main.PIXSIZE + 1, coord[0]*Main.PIXSIZE + Main.PIXSIZE - 2, coord[1]*Main.PIXSIZE + Main.PIXSIZE - 2, fill="gray")
  

class Window(Frame):
  def __init__(self, master):
    Frame.__init__(self, master)
    self.canvas = Canvas(self, width = Main.MAPWIDTH * Main.PIXSIZE, height = Main.MAPHEIGHT * Main.PIXSIZE)
    self.canvas.grid()
    self.updateMap()

  def updateMap(self):
    todel = self.canvas.find_all()
    for item in todel:
      self.canvas.delete(item)
    self.canvas.create_rectangle(0, 0, Main.MAPWIDTH * Main.PIXSIZE, Main.MAPHEIGHT * Main.PIXSIZE, fill="white")

    #drawing the map    
    for (coord, unit) in Main.map.iteritems():
      if unit == Graphics.BLOCK:
        self.canvas.create_rectangle(coord[0]*Main.PIXSIZE, coord[1]*Main.PIXSIZE, coord[0]*Main.PIXSIZE + Main.PIXSIZE - 1, coord[1]*Main.PIXSIZE + Main.PIXSIZE - 1, fill="black")

    #drawing the snake
    DrawSnake(self.canvas)
    
    #drawing foods
    for coord in Main.food:
      self.canvas.create_rectangle(coord[0]*Main.PIXSIZE + 1, coord[1]*Main.PIXSIZE + 1, coord[0]*Main.PIXSIZE + Main.PIXSIZE - 2, coord[1]*Main.PIXSIZE + Main.PIXSIZE - 2, fill="red")

if __name__ == "__main__":

  if len(sys.argv) < 2:
    print "Usage: %s <map name> [speed]" % sys.argv[0]
    sys.exit(1)

  Main.map = sys.argv[1]

  if len(sys.argv) > 2:
    Main.speed = Main.speed/int(sys.argv[2])

  app = Main()

