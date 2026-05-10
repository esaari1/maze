import argparse

from distance import Distances
from generator import *
import grid
import image
import mask

def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{x} is not a valid float")
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"{x} is not in range [0.0, 1.0]")
    return x

def calc_distances(maze, distances):
    if distances != 'none':
        if distances == 'center':
            dist = Distances(maze[int(rows/2)][int(cols/2)])
        elif distances == 'corner':
            cell = None
            gen = maze.all_cells()
            while cell is None:
                cell = next(gen)
            dist = Distances(cell)
        else:
            dist = Distances(random.choice(random.choice(maze.maze)))
        dist.calc_distances()
        maze.dist = dist


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--algorithm', choices=['binary', 'side', 'aldous', 'wilson', 'hunt', 'recurse'], default='recurse')
parser.add_argument('-b', '--braid', type=restricted_float, help='Remove dead ends. Value if probabbility of removal, between 0 and 1')
parser.add_argument('-c', '--color', choices=['green', 'sunburst', 'pink', 'pink2', 'purple'], default='sunburst')
parser.add_argument('-d', '--distances', choices=['none', 'center', 'corner', 'random'], default='none')
parser.add_argument('-f', '--filename', default='grid.png')
parser.add_argument('-i', '--inset', type=restricted_float, help='Inset maze walls by a percent of cell size', default=0)
parser.add_argument('-m', '--mask')
parser.add_argument('-s', '--size', type=int, default=20)
args = parser.parse_args()

rows = args.size
cols = args.size

if args.mask:
    m = mask.from_file(args.mask)
    maze = grid.MaskGrid(m)
else:
    maze = grid.Grid(rows, cols)

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

if args.braid:
    maze.braid(args.braid)

calc_distances(maze, args.distances)
#maze.printMaze()
image.save_grid(maze, args.filename, args.color, args.inset)
