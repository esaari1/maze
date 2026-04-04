import random

from cell import Cell

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
        for row in self.maze:
            for cell in row:
                if cell:
                    if cell.row > 0:
                        cell.neighbors[NORTH] = self.maze[cell.row - 1][cell.col]
                    if cell.row < rows - 1:
                        cell.neighbors[SOUTH] = self.maze[cell.row + 1][cell.col]
                    if cell.col > 0:
                        cell.neighbors[WEST] = self.maze[cell.row][cell.col - 1]
                    if cell.col < cols - 1:
                        cell.neighbors[EAST] = self.maze[cell.row][cell.col + 1]

    def prepare(self):
        self.maze = [[Cell(row, col) for col in range(self.cols)] for row in range(self.rows)]

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
                    self.maze[r][c] = Cell(r, c)

    def random_cell(self):
        (row, col) = self.mask.random_cell()
        return self.maze[row][col]
