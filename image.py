import cairo
import math

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

greens = [
    (0, .8, 1, .8),
    (0.5, 0, 1, 0),
    (1, 0, 0.2, 0)
]

sunburst = [
    (0, 1, 1, 1),
    (0.1, 1, 1, 0),
    (0.9, 1, 0, 0),
    (1, 0.5, 0, 0)
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
    (0, 1, 0.5, 1),
    (1, 0.3, 0.15, 0.3)
]

def get_colors(name):
    if name == 'green':
        return greens
    if name == 'sunburst':
        return sunburst
    if name == 'pink':
        return pinks
    if name == 'pink2':
        return pinks2
    return purple


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


def save_radial(maze, fname, color_name):
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

    if maze.dist:
        colors = get_colors(color_name)
        # center circle
        (red, green, blue) = gradient(0, sunburst)
        ctx.set_source_rgb(red, green, blue)
        ctx.arc(0.5, 0.5, cell_size, 0, 2 * math.pi)
        ctx.fill()

        # cell wedges
        for r in range(len(maze)):
            theta = 2 * math.pi / len(maze[r])
            inner_radius = r * cell_size
            outer_radius = inner_radius + cell_size

            for cell in maze[r]:
                theta_ccw = cell.col * theta
                theta_cw = theta_ccw + theta

                (red, green, blue) = gradient(maze.dist.intensity(cell), colors)
                ctx.set_source_rgb(red, green, blue)

                x1 = 0.5 + (inner_radius * math.cos(theta_cw))
                y1 = 0.5 + (inner_radius * math.sin(theta_cw))
                x2 = 0.5 + (outer_radius * math.cos(theta_cw))
                y2 = 0.5 + (outer_radius * math.sin(theta_cw))

                ctx.arc(0.5, 0.5, inner_radius, theta_ccw, theta_cw)
                ctx.line_to(x2, y2)
                ctx.arc_negative(0.5, 0.5, outer_radius, theta_cw, theta_ccw)
                ctx.close_path()
                ctx.fill()

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


def save_hex(maze, fname, color_name):
    hex_width = 100
    wall_width = 0.001

    #hex_width = size / len(maze)
    a_size = hex_width / 4
    b_size = hex_width / 2 * math.sqrt(3) / 2
    hex_height = b_size * 2

    img_width = int(3 * a_size * maze.cols + a_size + 0.5)
    img_height = int(hex_height * maze.rows + b_size + 0.5)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(surface)

    ctx.scale(img_width, img_height)

    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()

    ctx.translate(0.01, 0.01)
    ctx.scale(0.98, 0.98)

    if maze.dist:
        colors = get_colors(color_name)
        for cell in maze.all_cells():
            cx = hex_width/2 + 3 * cell.col * a_size
            cy = b_size + cell.row * hex_height
            cy += b_size if cell.col % 2 == 1 else 0

            x_fw = int(cx - hex_width / 2) / img_width
            x_nw = int(cx - a_size) / img_width
            x_ne = int(cx + a_size) / img_width
            x_fe = int(cx + hex_width / 2) / img_width

            y_n = int(cy - b_size) / img_height
            y_c = int(cy) / img_height
            y_s = int(cy + b_size) / img_height

            (red, green, blue) = gradient(maze.dist.intensity(cell), colors)
            ctx.move_to(x_fw, y_c)
            ctx.line_to(x_nw, y_s)
            ctx.line_to(x_ne, y_s)
            ctx.line_to(x_fe, y_c)
            ctx.line_to(x_ne, y_n)
            ctx.line_to(x_nw, y_n)
            ctx.close_path()
            ctx.set_source_rgb(red, green, blue)
            ctx.fill()

    for cell in maze.all_cells():
        cx = hex_width/2 + 3 * cell.col * a_size
        cy = b_size + cell.row * hex_height
        cy += b_size if cell.col % 2 == 1 else 0

        x_fw = int(cx - hex_width / 2) / img_width
        x_nw = int(cx - a_size) / img_width
        x_ne = int(cx + a_size) / img_width
        x_fe = int(cx + hex_width / 2) / img_width

        y_n = int(cy - b_size) / img_height
        y_c = int(cy) / img_height
        y_s = int(cy + b_size) / img_height

        if not cell.isLinked(cell.sw):
            ctx.move_to(x_fw, y_c)
            ctx.line_to(x_nw, y_s)

        if not cell.isLinked(cell.nw):
            ctx.move_to(x_fw, y_c)
            ctx.line_to(x_nw, y_n)

        if not cell.isLinked(cell.n):
            ctx.move_to(x_nw, y_n)
            ctx.line_to(x_ne, y_n)

        if not cell.isLinked(cell.ne):
            ctx.move_to(x_ne, y_n)
            ctx.line_to(x_fe, y_c)

        if not cell.isLinked(cell.se):
            ctx.move_to(x_fe, y_c)
            ctx.line_to(x_ne, y_s)

        if not cell.isLinked(cell.s):
            ctx.move_to(x_ne, y_s)
            ctx.line_to(x_nw, y_s)

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(wall_width)
        ctx.stroke()

    surface.write_to_png(fname)

def save_triangle(maze, fname, color):
    tri_width = 100
    half_width = tri_width / 2
    height = tri_width * math.sqrt(3) / 2
    half_height = height / 2

    wall_width = 0.001

    img_width = int(tri_width * (maze.cols + 1) / 2)
    img_height = int(height * maze.rows)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(surface)

    ctx.scale(img_width, img_height)

    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, 1, 1)
    ctx.fill()

    ctx.translate(0.01, 0.01)
    ctx.scale(0.98, 0.98)

    if maze.dist:
        colors = get_colors(color)
        for cell in maze.all_cells():
            cx = half_width + cell.col * half_width
            cy = half_height + cell.row * height

            west_x = int(cx - half_width) / img_width
            mid_x = int(cx) / img_width
            east_x = int(cx + half_width) / img_width

            if cell.upright():
                apex_y = int(cy - half_height) / img_height
                base_y = int(cy + half_height) / img_height
            else:
                apex_y = int(cy + half_height) / img_height
                base_y = int(cy - half_height) / img_height

            (red, green, blue) = gradient(maze.dist.intensity(cell), colors)
            ctx.move_to(west_x, base_y)
            ctx.line_to(east_x, base_y)
            ctx.line_to(mid_x, apex_y)
            ctx.close_path()
            ctx.set_source_rgb(red, green, blue)
            ctx.fill()

    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(wall_width)

    for cell in maze.all_cells():
        cx = half_width + cell.col * half_width
        cy = half_height + cell.row * height

        west_x = int(cx - half_width) / img_width
        mid_x = int(cx) / img_width
        east_x = int(cx + half_width) / img_width

        if cell.upright():
            apex_y = int(cy - half_height) / img_height
            base_y = int(cy + half_height) / img_height
        else:
            apex_y = int(cy + half_height) / img_height
            base_y = int(cy - half_height) / img_height

        if not cell.links[WEST]:
            ctx.move_to(west_x, base_y)
            ctx.line_to(mid_x, apex_y)
            ctx.stroke()

        if not cell.links[EAST]:
            ctx.move_to(east_x, base_y)
            ctx.line_to(mid_x, apex_y)
            ctx.stroke()

        no_south = cell.upright() and not cell.neighbors[SOUTH]
        not_linked = not cell.upright() and not cell.links[NORTH]

        if no_south or not_linked:
            ctx.move_to(east_x, base_y)
            ctx.line_to(west_x, base_y)
            ctx.stroke()

    surface.write_to_png(fname)
