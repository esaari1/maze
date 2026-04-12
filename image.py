import cairo
import math

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

greens = [
    (0, 0.9, 1, 0.9),
    (0.5, 0, 1, 0),
    (1, 0, 0.1, 0)
]

sunburst = [
    (0, 1, 1, 1),
    (0.1, 1, 1, 0),
    (0.9, 1, 0, 0),
    (1, 0, 0, 0)
]

pinks = [
    (0, 1, 0.71, 0.76),
    (1, 0.67, 0.2, 0.42)
]

pinks2 = [
    (0, 0.67, 0.2, 0.42),
    (1, 0.62, 0, 1)
]

purple = [
    (0, 1, 0, 1),
    (1, 0.2, 0, 0.2)
]

def gradient(t, colors):
    idx = 0
    while t > colors[idx+1][0] and idx < len(colors):
        idx += 1
    t = (t - colors[idx][0]) / (colors[idx+1][0] - colors[idx][0])
    r = colors[idx][1] + t * (colors[idx+1][1] - colors[idx][1])
    g = colors[idx][2] + t * (colors[idx+1][2] - colors[idx][2])
    b = colors[idx][3] + t * (colors[idx+1][3] - colors[idx][3])
    return (r, g, b)


def save_grid(maze, fname):
    img_width, img_height = maze.cols * 50, maze.rows * 50
    wall_width = 0.001
    wall_height = 0.001

    if maze.cols > maze.rows:
        img_width = int(maze.cols / maze.rows * img_height)
        wall_width = maze.cols / maze.rows * wall_height
    if maze.rows > maze.cols:
        img_height = int(maze.rows / maze.cols * img_width)
        wall_height = maze.rows / maze.cols * wall_width

    cell_h = (img_width / maze.rows) / img_width
    cell_w = (img_height / maze.cols) / img_height

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(surface)

    ctx.scale(img_width, img_height)

    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()

    ctx.translate(0.05, 0.05)
    ctx.scale(0.9, 0.9)

    if maze.dist:
        for r in range(maze.rows):
            for c in range(maze.cols):
                if maze[r][c] and maze[r][c] in maze.dist.distances:
                    (red, green, blue) = gradient(maze.dist.intensity(maze[r][c]), greens)
                    ctx.rectangle(c * cell_w, r * cell_h, cell_w , cell_h)
                    ctx.set_source_rgb(red, green, blue)
                    ctx.fill()

    ctx.set_source_rgb(0, 0, 0)

    for r in range(maze.rows):
        for c in range(maze.cols):
            if maze[r][c] and not maze[r][c].links[NORTH]:
                ctx.move_to(c * cell_w, r * cell_h)
                ctx.rel_line_to(cell_w, 0)
                ctx.set_line_width(wall_width)
                ctx.stroke()

            if maze[r][c] and not maze[r][c].links[EAST]:
                ctx.move_to((c + 1) * cell_w, r * cell_h)
                ctx.rel_line_to(0, cell_h)
                ctx.set_line_width(wall_height)
                ctx.stroke()

            if maze[r][c] and not maze[r][c].links[SOUTH]:
                ctx.move_to(c * cell_w, (r + 1) * cell_h)
                ctx.rel_line_to(cell_w, 0)
                ctx.set_line_width(wall_width)
                ctx.stroke()

            if maze[r][c] and not maze[r][c].links[WEST]:
                ctx.move_to(c * cell_w, r * cell_h)
                ctx.rel_line_to(0, cell_h)
                ctx.set_line_width(wall_height)
                ctx.stroke()

    # top and left size limes
    # ctx.move_to(1, 0)
    # ctx.line_to(0, 0)
    # ctx.line_to(0, 1)
    # ctx.set_source_rgb(0, 0, 0)
    # ctx.stroke()

    surface.write_to_png(fname)


def save_radial(maze, fname):
    size = 1000
    hsize = size / 2
    wall_width = 0.001
    cell_size = (hsize / maze.rows) / hsize / 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)

    ctx.scale(size, size)

    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()

    ctx.translate(0.01, 0.01)
    ctx.scale(0.98, 0.98)

    for r in range(1, maze.rows):
        theta = 2 * math.pi / len(maze[r])
        inner_radius = r * cell_size
        outer_radius = inner_radius + cell_size

        for cell in maze[r]:
            theta_ccw = cell.col * theta
            theta_cw = theta_ccw + theta

            if not cell.isLinked(cell.inward):
                ctx.new_sub_path()
                ctx.arc(0.5, 0.5, inner_radius, theta_ccw, theta_cw)

            if not cell.isLinked(cell.cw):
                x1 = 0.5 + (inner_radius * math.cos(theta_cw))
                y1 = 0.5 + (inner_radius * math.sin(theta_cw))
                x2 = 0.5 + (outer_radius * math.cos(theta_cw))
                y2 = 0.5 + (outer_radius * math.sin(theta_cw))

                ctx.move_to(x1, y1)
                ctx.line_to(x2, y2)

    ctx.new_sub_path()
    ctx.arc(0.5, 0.5, 0.5, 0, 2 * math.pi)

    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(wall_width)
    ctx.stroke()

    surface.write_to_png(fname)
