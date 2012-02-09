#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##          Author: Kovács Márton, unsigned.t@gmail.com, 2011                ##
##           Map editor for snake game with multiple panels                  ##
###############################################################################

import snake

from Tkinter import Canvas, Tk
import sys

sizex = 800
sizey = 600

def GetPos(x, y):
  return (x * width / sizex, y * height / sizey)

def Click(event):
  (x, y) = GetPos(event.x, event.y)
  
  if terrain[(x, y)] == snake.Graphics.FREE:
    color = 'black'
    terrain[(x, y)] = snake.Graphics.BLOCK
  else:
    color = 'white'
    terrain[(x, y)] = snake.Graphics.FREE
  
  drawer.create_rectangle(x*pxxsize, y*pxysize, x*pxxsize + pxxsize, y*pxysize + pxysize, fill = color)

def RightClick(event):
  (x, y) = GetPos(event.x, event.y)
  if (x, y) in start:
    start.remove((x, y))
    drawer.create_rectangle(x*pxxsize + 5, y*pxysize + 5, x*pxxsize + pxxsize - 5, y*pxysize + pxysize - 5, fill = 'white')
  else:
    start.append((x, y))
    drawer.create_rectangle(x*pxxsize + 5, y*pxysize + 5, x*pxxsize + pxxsize - 5, y*pxysize + pxysize - 5, fill = 'red')
    
def Save(event):
  f = open(savename, 'w')

  f.write("%d\n%d\n" % (width, height))

  for coord in ((x,y) for y in range(height) for x in range(width)):
    f.write("%d\n" % terrain[coord])

  for coord in start:
    f.write("%d;%d\n" % coord)

if __name__ == "__main__":
  width = int(sys.argv[1])
  height = int(sys.argv[2])
  
  if len(sys.argv) > 3:
    savename = sys.argv[3]
  else:
    savename = 'result_map'

  pxxsize = float(sizex) / width
  pxysize = float(sizey) / height

  drawer = Canvas(width = sizex, height = sizey, bg = 'white')

  terrain = {}
  for coord in ((x,y) for y in range(height) for x in range(width)):
    terrain[coord] = snake.Graphics.FREE
    drawer.create_rectangle(coord[0]*pxxsize, coord[1]*pxysize, coord[0]*pxxsize + pxxsize, coord[1]*pxysize + pxysize, fill = 'white')

  start = []

  drawer.grid()

  drawer.bind('<Button-1>', Click)
  drawer.bind('<Button-3>', RightClick)
  drawer.bind('<Button-2>', Save)

  drawer.mainloop()
  

