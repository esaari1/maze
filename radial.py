import argparse

from distance import Distances
from generator import *
import grid
import image

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--size', type=int, default=20)
parser.add_argument('-a', '--algorithm', choices=['binary', 'side', 'aldous', 'wilson', 'hunt', 'recurse'], default='recurse')
parser.add_argument('-c', '--color', choices=['green', 'sunburst', 'pink', 'pink2', 'purple'], default='sunburst')
parser.add_argument('-d', '--distance', action="store_true")
parser.add_argument('-f', '--filename', default='circle.png')
args = parser.parse_args()

maze = grid.PolarGrid(args.size)

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

if args.distance:
    dist = Distances(maze[0][0])
    dist.calc_distances()
    maze.dist = dist

image.save_radial(maze, args.filename, args.color)
