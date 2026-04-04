import random

class Mask():

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.bits = [[True for _ in range(cols)] for _ in range(rows)]

    def __getitem__(self, row): return self.bits[row]

    def count(self):
        cnt = 0
        for row in self.bits:
            for b in row:
                cnt += 1 if b else 0
        return cnt

    def random_cell(self):
        while True:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.bits[row][col]:
                return (row, col)

def from_file(fname):
    lines = []
    with open(fname) as f:
        for line in f:
            lines.append(line[:len(line) - 1])

    rows = len(lines)
    cols = len(lines[0])
    m = Mask(rows, cols)
    row = 0
    for line in lines:
        for col in range(cols):
            m[row][col] = False if (col >= len(line) or line[col] == " ") else True
        row += 1
    return m
