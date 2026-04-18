import random

class Cell():
    def __init__(self, row, col):
       self.row = row
       self.col = col
       self.neighbors = []
       self.links = []

    def __repr__(self):
        return f'{self.row} {self.col}'

    # Return any random neighbor
    def randomNeighbor(self):
        filtered_neighbors = [n for n in self.neighbors if n]
        return random.choice(filtered_neighbors)

    # Return a random neighbor that has no associated links
    def randomUnlinkedNeighbor(self):
        filtered_neighbors = [n for n in self.neighbors if n and all(not l for l in n.links)]
        if len(filtered_neighbors) == 0:
            return None
        return random.choice(filtered_neighbors)

    # Return a random neighbor that has at least 1 associated link
    def randomLinkedNeighbor(self):
        filtered_neighbors = [n for n in self.neighbors if n and any(l for l in n.links)]
        if len(filtered_neighbors) == 0:
            return None
        return random.choice(filtered_neighbors)

    def link(self, other): pass
    def hasLink(self): pass
    def isLinked(self, other): pass
    def upNeighbor(self): pass
    def rightNeighbor(self): pass


class GridCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.neighbors = [None] * 4
        self.filtered_neighbors = []
        self.links = [False] * 4

    def link(self, other):
        idx = self.neighbors.index(other)
        self.links[idx] = True
        other.links[(idx + 2) % 4] = True

    def hasLink(self):
        return any(l for l in self.links)

    def isLinked(self, other):
        if other in self.neighbors:
            idx = self.neighbors.index(other)
            return self.links[idx]
        return False

    def upNeighbor(self):
        return self.neighbors[0]

    def rightNeighbor(self):
        return self.neighbors[1]

class PolarCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.cw = None
        self.ccw = None
        self.inward = None
        self.outward = []

    def link(self, other):
        self.links.append(other)
        other.links.append(self)

    def hasLink(self):
        return len(self.links) > 0

    def isLinked(self, other):
        if other is None:
            return False
        return other in self.links

    # Return a random neighbor that has no associated links
    def randomUnlinkedNeighbor(self):
        filtered_neighbors = [n for n in self.neighbors if n and len(n.links) == 0]
        if len(filtered_neighbors) == 0:
            return None
        return random.choice(filtered_neighbors)

    def upNeighbor(self):
        return self.inward

    def rightNeighbor(self):
        return self.ccw


class HexCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.n = None
        self.s = None
        self.nw = None
        self.sw = None
        self.ne = None
        self.se = None

    def link(self, other):
        self.links.append(other)
        other.links.append(self)

    def add_neighbor(self, other):
        if other:
            self.neighbors.append(other)
            other.neighbors.append(self)

    def hasLink(self):
        return len(self.links) > 0

    def isLinked(self, other):
        if other is None:
            return False
        return other in self.links

    # Return a random neighbor that has no associated links
    def randomUnlinkedNeighbor(self):
        filtered_neighbors = [n for n in self.neighbors if n and len(n.links) == 0]
        if len(filtered_neighbors) == 0:
            return None
        return random.choice(filtered_neighbors)

    def upNeighbor(self):
        return self.n

    def rightNeighbor(self):
        if self.col % 2 == 0:
            return self.se
        else:
            return self.ne


class TriangleCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.neighbors = [None] * 4
        self.links = [False] * 4

    def upright(self):
        return (self.row + self.col) % 2 == 0

    def add_neighbor(self, other, dir):
        if other:
            self.neighbors[dir] = other
            other.neighbors[(dir + 2) % 4] = self

    def link(self, other):
        idx = self.neighbors.index(other)
        self.links[idx] = True
        other.links[(idx + 2) % 4] = True

    def isLinked(self, other):
        if other in self.neighbors:
            idx = self.neighbors.index(other)
            return self.links[idx]
        return False
