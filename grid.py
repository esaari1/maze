import math
import random

from cell import GridCell, PolarCell, HexCell, TriangleCell

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

    def all_cells(self):
        for row in self.maze:
            for cell in row:
                yield cell

    def cell_at(self, row, col):
        if row < 0 or row > len(self.maze) -1:
            return None
        if col < 0 or col > len(self.maze[row]) - 1:
            return None
        return self.maze[row][col]

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


class HexGrid(Grid):
    def __init__(self, rows, cols):
        super().__init__(rows, cols)

    def prepare(self):
        self.maze = [[HexCell(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def init_cells(self):
        for cell in self.all_cells():
            if cell.col % 2 == 0:
                north_diag = cell.row - 1
                south_diag = cell.row
            else:
                north_diag = cell.row
                south_diag = cell.row + 1

            cell.n = self.cell_at(cell.row - 1, cell.col)
            cell.nw = self.cell_at(north_diag, cell.col - 1)
            cell.ne = self.cell_at(north_diag, cell.col + 1)
            cell.s = self.cell_at(cell.row + 1, cell.col)
            cell.sw = self.cell_at(south_diag, cell.col - 1)
            cell.se = self.cell_at(south_diag, cell.col + 1)

            cell.add_neighbor(cell.n)
            cell.add_neighbor(cell.nw)
            cell.add_neighbor(cell.ne)
            cell.add_neighbor(cell.s)
            cell.add_neighbor(cell.sw)
            cell.add_neighbor(cell.se)


class TriangleGrid(Grid):
    def __init__(self, rows, asTriangle):
        self.asTriangle = asTriangle
        if asTriangle:
            if rows % 2 == 0:
                rows += 1
            cols = (rows * 2) - 1
        else:
            cols = int(rows * 1.7)
            if cols % 2 == 0:
                cols += 1

        super().__init__(rows, cols)

    def prepare(self):
        if self.asTriangle:
            self.maze = [[None for col in range(self.cols)] for row in range(self.rows)]
            mid_col = int(self.cols / 2)

            for row in range(self.rows):
                col_count = ((row+1) * 2) - 1
                hcol_count = int(col_count / 2)

                for col in range(mid_col - hcol_count, mid_col + hcol_count + 1):
                    self.maze[row][col] = TriangleCell(row, col)
        else:
            self.maze = [[TriangleCell(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def init_cells(self):
        for cell in self.all_cells():
            if cell:
                if cell.upright():
                    cell.add_neighbor(self.cell_at(cell.row + 1, cell.col), SOUTH)
                else:
                    cell.add_neighbor(self.cell_at(cell.row - 1, cell.col), NORTH)

                cell.add_neighbor(self.cell_at(cell.row, cell.col + 1), EAST)
                cell.add_neighbor(self.cell_at(cell.row, cell.col - 1), WEST)

    def random_cell(self):
        row = random.choice(self.maze)
        return random.choice([c for c in row if c])

    def all_cells(self):
        for row in self.maze:
            for cell in row:
                if cell:
                    yield cell
