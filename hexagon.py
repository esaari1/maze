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
parser.add_argument('-f', '--filename', default='hex.png')
args = parser.parse_args()

maze = grid.HexGrid(args.size, args.size)

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
        dist = Distances(maze[int(args.size / 2)][int(args.size / 2)])
    elif args.distances == 'corner':
        cell = None
        gen = maze.all_cells()
        while cell is None:
            cell = next(gen)
        dist = Distances(cell)
    else:
        dist = Distances(random.choice(random.choice(maze.maze)))
    dist.calc_distances()
    maze.dist = dist

image.save_hex(maze, args.filename, args.color)
