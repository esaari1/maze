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

    # link this cell to other
    def link(self, other): pass

    def hasLink(self): pass

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
