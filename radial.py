from generator import *
import grid
import image

maze = grid.Grid(8, 8)
Recurse(maze)

image.save_radial(maze)
