import random

class Cell():
    def __init__(self, row, col):
        self.neighbors = [None] * 4
        self.filtered_neighbors = []
        self.links = [False] * 4
        self.row = row
        self.col = col

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
    def link(self, other):
        idx = self.neighbors.index(other)
        self.links[idx] = True
        other.links[(idx + 2) % 4] = True
