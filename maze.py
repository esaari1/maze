import random
import sys

from distance import Distances
from generator import *
import grid
import image
import mask

rows = 20
cols = 20

maze = grid.Grid(rows, cols)

#BinaryTree(maze)
#Sidewinder(maze)
#AldousBroder(maze)
#Wilson(maze)
#HuntAndKill(maze)
Recurse(maze)

# Calculate distances from a random cell
#dist = Distances(random.choice(random.choice(maze.maze)))
dist = Distances(maze[0][0])
#dist = Distances(maze[int(rows/2)][int(cols/2)])
dist.calc_distances()
maze.dist = dist

maze.printMaze()

# Create a path from distance origin to lower right corner
# path = dist.path_to(maze[rows-1][cols-1])
# maze.dist = path
# maze.printMaze()

image.save_grid(maze, 'grid.png')

m = mask.from_file('sarah.txt')
maze2 = grid.MaskGrid(m)
Recurse(maze2)
maze2.dist = Distances(maze2[0][3])
maze2.dist.calc_distances()

image.save_grid(maze2, 'sarah.png')
