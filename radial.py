from generator import *
import grid
import image

maze = grid.PolarGrid(10)

#BinaryTree(maze)
#Sidewinder(maze)
#AldousBroder(maze)
#Wilson(maze)
#HuntAndKill(maze)
Recurse(maze)

image.save_radial(maze, 'circle.png')
