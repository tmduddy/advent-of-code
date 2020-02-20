from random import randrange, seed
import os
from intcode import IntcodeParser
from utilities import create_canvas
from time import sleep

droid = IntcodeParser()
intcode = droid.get_intcode_from_file('input-files/day15.csv')

location = [0, 0]
path = [(0,0)]
direction = 2
counter = 0
pos = 0
rel = 0
path_dict = {(0,0): '🎾'}
can_size = 42
canvas = [['◻️ ' for _ in range(can_size)] for _ in range(can_size)]
'''
1 N
2 S
3 W
4 E
'''
direction_list = [2,4,1,4,1,4,2,3,2,3,2,3,1,3,2,3,1,3,2,4,2,3,1,3,  2,4,2,3,2,4,1,4,2,4,2,4,1,4,1,3,1,4,1,4,2,4,1,4,1,3,2,3,1,3,2,3,2,4,5,3,1,3,2,3,2,3,1,4,1,4,1,3]
dir_count = 0
seed(1) # consistent random seed
while counter < 200000:
    value, halt_code, pos, rel, intcode = droid.parse_intcode(
        intcode,
        init_input=direction,
        init_pos=pos,
        init_rel_base=rel,
        print_out=False,
        halt_on_output=True,
        debug=False
    )
    print(counter, len(path), direction, value)
    if value == 0:
        look_location = location.copy()
        if direction == 1:
            look_location[1] += 1
        elif direction == 2:
            look_location[1] -= 1
        elif direction == 3:
            look_location[0] -= 1
        elif direction == 4:
            look_location[0] += 1
        dir_count += 1
        new_dir = direction_list[dir_count]
        direction = new_dir if new_dir != 5 else direction_list[dir_count + 1]
        path.append(tuple(look_location))
        path_dict[tuple(look_location)] = '❇️ '
    elif value in [1,2]:
        if direction_list[dir_count+1] == 5:
            dir_count += 1
            direction = direction_list[dir_count]

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
        print('found')
        path_dict[tuple(location)] = '♋️ '
        row = path[counter][1] + (len(canvas) // 2)
        col = path[counter][0] + (len(canvas) // 2)
        canvas[row][col] = '♋️'
        break
    #draw_canvas(path)
    
    row = path[counter][1] + (len(canvas) // 2)
    col = path[counter][0] + (len(canvas) // 2)
    canvas[row][col] = path_dict[path[counter]]

    for row in canvas:
        print(''.join(row))
    sleep(.15)
    os.system('clear')
    if counter % 2500 == 0:
        print(counter)
    counter += 1

row = len(canvas) // 2
col = len(canvas) // 2
canvas[row][col] = '👌🏻'
for row in canvas:
    print(''.join(row))
