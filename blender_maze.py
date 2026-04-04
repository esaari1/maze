import bpy
import random
import math

# row 0 = top

# 0 = no open
# 1 = north open
# 2 = east open
NORTH = 1
EAST = 2

rows = 20
cols = 20
maze = [[0 for _ in range(cols)] for _ in range(rows)]

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), scale=(.5, .05, .5))
base_cube = bpy.context.active_object

def addCube(loc, rotate):
    new_cube = base_cube.copy()
    new_cube.data = base_cube.data.copy()
    new_cube.location = loc
    if rotate:
        new_cube.rotation_euler = (0, 0, math.pi/2)
    bpy.context.collection.objects.link(new_cube)

def blenderRender():
    for r in range(rows):
        for c in range(cols):
            if (not maze[r][c] & NORTH):
                addCube((c + 0.5, rows - r, 0.5), False)
            if (not maze[r][c] & EAST):
                addCube((c + 1, rows - r - 0.5, 0.5), True)

    # left side
    for r in range(rows):
        addCube((0, rows - r - 0.5, 0.5), True)

    # top
    for c in range(cols):
        addCube((c + .5, 0, 0.5), False)

    bpy.data.objects.remove(base_cube, do_unlink=True)

# Binary tree
def binaryTree():
    for c in range(cols - 1):
        # top row
        maze[0][c] = EAST

        for r in range(1, rows):
            val = random.randint(NORTH, EAST)
            maze[r][c] = val

    # right side
    for r in range(1, rows):
        maze[r][cols - 1] = NORTH

# Sidewinder
def sideWinder():
    # top row all open to east
    for c in range(cols - 1):
        maze[0][c] = EAST

    for r in range(1, rows):
        group = []

        for c in range(cols):
            group.append(c)
            val = random.randint(NORTH, EAST)

            if val == 2 and c < cols - 1:
                maze[r][c] = EAST
            else:
                # Open north side of random cell in group
                cell = random.choice(group)
                maze[r][cell] += NORTH
                group = []

def output():
    for row in maze:
        print(row)

binaryTree()
#sideWinder()
blenderRender()
