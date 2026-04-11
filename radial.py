from generator import *
import grid
import image

maze = grid.PolarGrid(10)
Recurse(maze)

image.save_radial(maze)
