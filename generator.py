import random

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def BinaryTree(maze):
    for cell in maze.all_cells():
        neighbors = []
        if cell.upNeighbor(): neighbors.append(cell.upNeighbor())
        if cell.rightNeighbor(): neighbors.append(cell.rightNeighbor())

        if len(neighbors) > 0:
            n = random.choice(neighbors)
            cell.link(n)


def Sidewinder(maze):
    # top row all open to east
    for c in range(maze.cols - 1):
        maze[0][c].link(maze[0][c+1])

    for r in range(1, maze.rows):
        group = []

        for c in range(maze.cols):
            group.append(c)
            val = random.randint(NORTH, EAST)

            if val == EAST and c < maze.cols - 1:
                maze[r][c].link(maze[r][c+1])
            else:
                # Open north side of random cell in group
                cell = random.choice(group)
                maze[r][cell].link(maze[r-1][cell])
                group = []

# Random walk
def AldousBroder(maze):
    cell = maze.random_cell()
    unvisited = maze.rows * maze.cols - 1

    while unvisited > 0:
        next_cell = cell.randomNeighbor()

        if all(not item for item in next_cell.links):
            cell.link(next_cell)
            unvisited -= 1
        cell = next_cell


def Wilson(maze):
    # set all cells as unvisited
    unvisited = []
    for row in maze:
        for cell in row:
            unvisited.append(cell)

    first = random.choice(unvisited)
    unvisited.remove(first)

    while len(unvisited) > 0:
        cell = random.choice(unvisited)
        path = [cell]

        while cell in unvisited:
            cell = cell.randomNeighbor()

            if cell in path:
                position = path.index(cell)
                path = path[:position+1]
            else:
                path.append(cell)

        for i in range(len(path) - 1):
            path[i].link(path[i + 1])
            unvisited.remove(path[i])

def HuntAndKill(maze):
    cell = maze.random_cell()

    while cell:
        # get an unvisited neighbor
        neighbor = cell.randomUnlinkedNeighbor()
        if neighbor:
            cell.link(neighbor)
            cell = neighbor
        else:
            # hunt for new cell
            cell = None
            for r in range(maze.rows):
                for c in range(maze.cols):
                    if maze[r][c] and maze[r][c].links == [False] * 4:
                        neighbor = maze[r][c].randomLinkedNeighbor()
                        if neighbor:
                            cell = maze[r][c]
                            cell.link(neighbor)
                            break

def Recurse(maze):
    stack = []
    cell = maze.random_cell()
    stack.append(cell)

    while len(stack) > 0:
        current = stack[len(stack) - 1]
        neighbor = current.randomUnlinkedNeighbor()
        if neighbor:
            current.link(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()
