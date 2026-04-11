import math
import random

from cell import Cell, GridCell, PolarCell

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.dist = None
        self.prepare()
        self.init_cells()

    def prepare(self):
        self.maze = [[GridCell(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def init_cells(self):
        for row in self.maze:
            for cell in row:
                if cell:
                    if cell.row > 0:
                        cell.neighbors[NORTH] = self.maze[cell.row - 1][cell.col]
                    if cell.row < self.rows - 1:
                        cell.neighbors[SOUTH] = self.maze[cell.row + 1][cell.col]
                    if cell.col > 0:
                        cell.neighbors[WEST] = self.maze[cell.row][cell.col - 1]
                    if cell.col < self.cols - 1:
                        cell.neighbors[EAST] = self.maze[cell.row][cell.col + 1]

    def __getitem__(self, row): return self.maze[row]

    def __len__(self): return len(self.maze)

    def random_cell(self): return random.choice(random.choice(self.maze))

    def content_of(self, cell):
        if self.dist:
            if cell in self.dist.distances:
                return str(self.dist.distances[cell]).ljust(self.dist.max_len)
            return " " * self.dist.max_len
        return " "

    def cell_width(self):
        if self.dist:
            return 2 + self.dist.max_len
        return 3

    def printMaze(self):
        bar = "-" * self.cell_width()
        spaces = " " * self.cell_width()
        print(f'+{(bar + "+") * self.cols}')

        for row in self.maze:
            top = "|"
            bottom = "+"
            for cell in row:
                top += f' {self.content_of(cell)} {" " if cell and cell.links[EAST] else "|"}'
                bottom += spaces if cell and cell.links[SOUTH] else bar
                bottom += "+"

            print(top)
            print(bottom)

class MaskGrid(Grid):
    def __init__(self, mask):
        self.mask = mask
        super().__init__(mask.rows, mask.cols)

    def prepare(self):
        self.maze = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mask[r][c]:
                    self.maze[r][c] = GridCell(r, c)

    def random_cell(self):
        (row, col) = self.mask.random_cell()
        return self.maze[row][col]


class PolarGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows, 1)

    # Setup as a unit circle (radius 1)
    def prepare(self):
        self.maze = []
        self.maze.append([PolarCell(0, 0)])
        row_height = 1 / self.rows

        for row in range(1, self.rows):
            self.maze.append([])
            inner_radius = row / self.rows
            inner_circumfeence = 2 * math.pi * inner_radius

            prev_count = len(self.maze[row - 1])
            cell_width = inner_circumfeence / prev_count
            ratio = round(cell_width / row_height)

            cells = prev_count * ratio
            for col in range(cells):
                self.maze[row].append(PolarCell(row, col))

    def init_cells(self):
        for row in self.maze:
            for cell in row:
                if cell.row > 0:
                    column = (cell.col + 1) % len(row)
                    cell.cw = self.maze[cell.row][column]
                    cell.cw.ccw = cell
                    cell.neighbors.append(cell.cw)
                    cell.cw.neighbors.append(cell)

                    column = cell.col if cell.col > 0 else len(row) - 1
                    cell.ccw = self.maze[cell.row][cell.col - 1]
                    cell.ccw.cw = cell
                    cell.neighbors.append(cell.ccw)
                    cell.ccw.neighbors.append(cell)

                    ratio = len(self.maze[cell.row]) / len(self.maze[cell.row - 1])
                    parent = self.maze[cell.row - 1][int(cell.col / ratio)]
                    parent.outward.append(cell)
                    cell.inward = parent
                    cell.neighbors.append(cell.inward)
                    cell.inward.neighbors.append(cell)

    def random_cell(self):
        row = random.choice(self.maze)
        return random.choice(row)
