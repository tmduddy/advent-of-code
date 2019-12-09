import csv
from tqdm import tqdm

with open('input-files/day3.csv', 'r') as wire_file:
    reader = csv.reader(wire_file, delimiter=',')
    wire_list = [row for row in reader]

wire_1 = wire_list[0]
wire_2 = wire_list[1]


def man_dist(point):
    p = (0, 0)
    q = point
    return (abs(p[0] - q[0]) + abs(p[1]-q[1]))

start = (0,0)

def generate_moves(wire):
    x_1, y_1 = start

    all_points = []
    segment = 0
    for move in wire:
        direction = move[0]
        magnitude = int(move[1:])
        
        if direction == 'U':
            y_range = range(y_1, y_1 + magnitude+1)
            points = [(x_1, y) for y in y_range]
            y_1 += magnitude
        elif direction == 'D':
            y_range = range(y_1, y_1-magnitude-1, -1)
            points = [(x_1, y) for y in y_range]
            y_1 -= magnitude
        elif direction == 'L':
            x_range = range(x_1, x_1-magnitude-1, -1)
            points = [(x, y_1) for x in x_range]
            x_1 -= magnitude
        elif direction == 'R':
            x_range = range(x_1, x_1 + magnitude + 1)
            points = [(x, y_1) for x in x_range]
            x_1 += magnitude
        if segment == 0:
            all_points.append(points)
        else:
            all_points.append(points[1:])
        segment += 1
    return all_points

wire_1_points = [point for move_list in generate_moves(wire_1) for point in move_list]
wire_1_set = set(wire_1_points)

wire_2_points = [point for move_list in generate_moves(wire_2) for point in move_list]
wire_2_set = set(wire_2_points)

intersections = list(wire_1_set.intersection(wire_2_set))
intersections.remove((0,0))

time_distances = []
time_dict = {}
for point in intersections:
    combined_distance = wire_1_points.index(point) + wire_2_points.index(point)
    time_distances.append(combined_distance)
    time_dict[str(point)] = combined_distance


distances = list(map(man_dist, intersections))

print(min(time_distances))
print(time_dict)