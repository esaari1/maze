import argparse

from distance import Distances
from generator import *
import grid
import image

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size', type=int, default=20)
parser.add_argument('-a', '--algorithm', choices=['binary', 'side', 'aldous', 'wilson', 'hunt', 'recurse'], default='recurse')
parser.add_argument('-c', '--color', choices=['green', 'sunburst', 'pink', 'pink2', 'purple'], default='sunburst')
parser.add_argument('-d', '--distances', choices=['none', 'center', 'corner', 'random'], default='none')
parser.add_argument('-t', '--triangle', action="store_true")
parser.add_argument('-f', '--filename', default='triangle.png')
args = parser.parse_args()

maze = grid.TriangleGrid(args.size, args.triangle)

if args.algorithm == 'binary':
    BinaryTree(maze)
elif args.algorithm == 'side':
    Sidewinder(maze)
elif args.algorithm == 'aldous':
    AldousBroder(maze)
elif args.algorithm == 'wilson':
    Wilson(maze)
elif args.algorithm == 'hunt':
    HuntAndKill(maze)
else:
    Recurse(maze)

if args.distances != 'none':
    if args.distances == 'center':
        row = int(maze.rows / 2)
        col = int(len(maze[row]) / 2)
        dist = Distances(maze[row][col])
    elif args.distances == 'corner':
        cell = None
        gen = maze.all_cells()
        while cell is None:
            cell = next(gen)
        dist = Distances(cell)
    else:
        dist = Distances(maze.random_cell())
    dist.calc_distances()
    maze.dist = dist

image.save_triangle(maze, args.filename, args.color)
