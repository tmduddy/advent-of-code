import os
from intcode import IntcodeParser
from utilities import create_canvas

droid = IntcodeParser()
intcode = droid.get_intcode_from_file('input-files/day15.csv')

'''
1 N
2 S
3 W
4 E
'''

def draw_canvas(path):
    canvas, x_off, y_off = create_canvas(path)
    path_dict[(0,0)] = 'S'
    for loc in path:
        value = path_dict[loc]
        row = loc[1] + y_off - 2
        col = loc[0] + x_off - 2
        canvas[row][col] = value
    for row in canvas:
        print(''.join(row))

location = [0, 0]
path = [(0,0)]
direction = 1
counter = 0
pos = 0
rel = 0
path_dict = {}
while True:
    value, halt_code, pos, rel, intcode = droid.parse_intcode(
        intcode,
        init_input=direction,
        init_pos=pos,
        init_rel_base=rel,
        print_out=False,
        halt_on_output=True
    )

    if value == 0:
        look_location = location.copy()
        if direction == 1:
            look_location[1] += 1
            direction = 4
        elif direction == 2:
            look_location[1] -= 1
            direction = 3
        elif direction == 3:
            look_location[0] -= 1
            direction = 1
        elif direction == 4:
            look_location[0] += 1
            direction = 2
        path.append(tuple(look_location))
        path_dict[tuple(look_location)] = '◻️ '
    elif value in [1,2]:
        if direction == 1:
            location[1] += 1
        elif direction == 2:
            location[1] -= 1
        elif direction == 3:
            location[0] -= 1
        elif direction == 4:
            location[0] += 1
        path.append(tuple(location))
        path_dict[tuple(location)] = '◼️ '
    if value == 2:
        path_dict[tuple(location)] = '*'
        break
    draw_canvas(path)
    os.system('clear')