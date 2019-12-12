from intcode import parse_intcode

def get_fresh_intcode(day_num):
    with open(f'input-files/day{day_num}.csv', 'r') as f:
        return [row for row in f][0].split(',')

def robot(intcode, init_loc=(0,0), init_color=1, init_dir='U'):
    loc = init_loc
    loc_x, loc_y = loc
    current_color = init_color
    dir = init_dir
    first_cycle = True

    pos = 0
    rel_pos = 0

    cycle = "paint"
    painted_locs = {}
    
    while True:
        # get current loc's color
        if painted_locs.get(loc, False):
            current_color = painted_locs[loc]
        elif first_cycle:
            current_color = init_color
            first_cycle = False
        else:
            current_color = 0
        
        # run intcode
        value, halt_code, pos, rel_pos, intcode = parse_intcode(intcode, init_input=current_color, init=True, init_pos=pos, init_rel_base=rel_pos,halt_on_output=True, debug=False)
        
        # exit on HLT 99
        if halt_code == 99:
            break

        if cycle == "paint":
            new_color = value

            if new_color != current_color:
                painted_locs[loc] = new_color
            cycle = "location"

        elif cycle == "location":
            dir_num = value
            # convert dir_num to dir
            if dir == 'U':
                new_dir = 'L' if dir_num == 0 else 'R'
            elif dir == "D":
                new_dir = 'R' if dir_num == 0 else 'L'
            elif dir == 'L':
                new_dir = 'D' if dir_num == 0 else 'U'
            elif dir == "R":
                new_dir = 'U' if dir_num == 0 else 'D'
            
            if new_dir == 'U':
                loc_y += 1
            elif new_dir == "D":
                loc_y -= 1
            elif new_dir == 'L':
                loc_x -= 1
            elif new_dir == "R":
                loc_x += 1

            dir = new_dir
            loc = (loc_x, loc_y)
            cycle = "paint"
    return painted_locs

intcode = get_fresh_intcode(11)
painted_locs = {(0, 0): 0, (1, 0): 1, (1, -1): 1, (6, -1): 1, (6, 0): 1, (7, 0): 1, (8, 0): 1, (9, -1): 1, (11, 0): 1, (12, 0): 1, (13, 0): 1, (14, -1): 1, (14, 0): 1, (16, -1): 1, (16, 0): 1, (17, 0): 1, (18, 0): 1, (19, 0): 1, (21, -1): 1, (22, 0): 1, (23, 0): 1, (24, -1): 1, (26, -1): 1, (27, 0): 1, (28, 0): 1, (29, -1): 1, (31, 0): 1, (31, -1): 1, (32, 0): 1, (33, 0): 1, (34, 0): 1, (36, -1): 1, (36, 0): 1, (37, 0): 1, (38, 0): 1, (39, 0): 1, (38, -2): 1, (37, -2): 1, (36, -3): 1, (36, -2): 1, (33, -2): 1, (32, -2): 1, (31, -2): 1, (31, -3): 1, (29, -3): 1, (28, -3): 1, (26, -3): 1, (26, -2): 1, (21, -2): 1, (21, -3): 1, (18, -2): 1, (17, -2): 1, (16, -3): 1, (16, -2): 1, (13, -2): 1, (12, -3): 1, (9, -2): 1, (8, -3): 1, (7, -3): 1, (6, -3): 1, (6, -2): 1, (1, -2): 1, (1, -3): 1, (1, -4): 1, (1, -5): 1, (2, -5): 1, (3, -5): 1, (4, -5): 1, (6, -5): 1, (6, -4): 1, (8, -4): 1, (9, -5): 1, (11, -4): 1, (11, -5): 1, (12, -5): 1, (13, -5): 1, (14, -5): 1, (16, -5): 1, (16, -4): 1, (17, -5): 1, (18, -5): 1, (19, -5): 1, (21, -4): 1, (22, -5): 1, (23, -5): 1, (24, -4): 1, (26, -4): 1, (27, -5): 1, (28, -5): 1, (29, -4): 1, (29, -5): 1, (31, -4): 1, (31, -5): 1, (36, -5): 1, (36, -4): 1, (37, -5): 1, (38, -5): 1, (39, -5): 1}

for key in painted_locs:
    if painted_locs[key] == 0:
        painted_locs[key] = "⬛️ "
    else:
        painted_locs[key] = "⬜️ "

xs = [key[0] for key in painted_locs]
ys = [key[1] for key in painted_locs]

#need all positive numbers
x_offset = abs(min(xs)) 
y_offset = abs(min(ys))

# +1 to account for arrays being indexed by 0. else you get an Index Out of Bounds err
num_xs = x_offset + max(xs) + 1
num_ys = y_offset + max(ys) + 1
# generate canvas with size x*y and fill with black squares
canvas = []
for i in range(num_ys):
    row = []
    for j in range(num_xs):
        row.append('⬛️ ')
    canvas.append(row)

for x, y in painted_locs:
    # print(y+y_offset, x+x_offset, painted_locs[(x,y)])
    new_x = x+x_offset
    new_y = abs(y+y_offset - 5) # flip image vertically
    canvas[new_y][new_x] = painted_locs[(x,y)]
    # for i in canvas:
    #     print(''.join(i))

for i in canvas:
    print(''.join(i))

# for i in sorted(painted_locs):
#     print(i)