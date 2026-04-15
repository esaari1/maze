import queue

class Distances():
    def __init__(self, root):
        self.distances = {}
        self.root = root
        self.distances[self.root] = 0
        self.max = 0
        self.max_len = 1

    def calc_distances(self):
        q = queue.Queue()
        q.put(self.root)

        while not q.empty():
            cell = q.get()
            for n in cell.neighbors:
                if n not in self.distances and cell.isLinked(n):
                    self.distances[n] = self.distances[cell] + 1
                    self.max = self.distances[n]
                    q.put(n)
        self.max_len = len(str(self.max))

    def get_rgb(self, cell):
        if cell not in self.distances:
            return (1, 1, 1)
        intensity = (self.max - self.distances[cell]) / self.max
        dark = intensity
        light = (128 + (127 * intensity)) / 255
        return (dark, light, dark)

    def intensity(self, cell):
        if cell not in self.distances:
            return 1
        return self.distances[cell] / self.max

    def path_to(self, end_cell):
        curr = end_cell
        path = Distances(self.root)
        path.distances[curr] = self.distances[curr]
        path.max = path.distances[curr]
        path.max_len = len(str(self.max))

        while curr != self.root:
            for idx in range(len(curr.neighbors)):
                n = curr.neighbors[idx]
                if curr.links[idx] and self.distances[n] < self.distances[curr]:
                    curr = n
                    path.distances[n] = self.distances[n]
                    break
        return path
