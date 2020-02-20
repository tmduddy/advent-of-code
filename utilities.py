def create_canvas(path):
    xs = [loc[0] for loc in path]
    ys = [loc[1] for loc in path]
    x_offset = 0
    y_offset = 0
    min_x = min(xs)
    min_y = min(ys)
    if min_x <= 0:
        x_offset = abs(min_x) + 1
    if min_y <= 0:
        y_offset = abs(min_y) + 1
    num_xs = max(xs) + x_offset
    num_ys = max(ys) + y_offset
    canvas = [['' for _ in range(num_ys)] for _ in range(num_xs)]
    return canvas, x_offset, y_offset

