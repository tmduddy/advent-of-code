from intcode import parse_intcode

def get_fresh_intcode():
    with open('input-files/day13.csv', 'r') as f:
        for row in f:
            return list(map(int, row.strip().split(',')))

intcode = get_fresh_intcode()

def list_to_thruples(lst, n=3):
    # stolen shamelessly from stack overflow #
    # https://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n #
    return list(zip(*(iter(lst),) * n))

def draw_to_canvas(canvas, pos, value):
    x = pos[0]
    y = pos[1]
    print(x, y, value)
    print(f'starting canvas: {canvas}')
    existing_rows = len(canvas)
    if existing_rows <= y:
        canvas = canvas.copy().append([''] * (x - existing_rows + 1))
    existing_cols = len(canvas[0])
    if existing_cols <= x:
        for row in canvas:
            row.append(row.copy().append([''] * (y - existing_cols + 1)))
    canvas[y][x] = value
    return canvas

def run_game(intcode):
    game_inputs = []
    pos = 0
    rel = 0
    while True:
        # run intcode
        value, halt_code, pos, rel, intcode = parse_intcode(
            intcode, 
            init_pos=pos, 
            init_rel_base=rel, 
            halt_on_output=True,
            print_out=False
        )
        if halt_code == 99:
            break
        game_inputs.append(value)
    
    num_cols = max([x for x,y,z in list_to_thruples(game_inputs)])
    num_rows = max([y for x,y,z in list_to_thruples(game_inputs)])
    game_inputs_formatted = [((x,y), z) for x,y,z in list_to_thruples(game_inputs)]

    canvas = [['' for _ in range(num_cols+1)] for __ in range(num_rows+1)] # 2D canvas of proper size

    val_dict = {
        0: "◼️ ",
        1: "◻️ ",
        2: "♋️",
        3: "❇️ ",
        4: "🎾",
    }

    for pos, val in game_inputs_formatted:
        if pos = (-1, 0):
            score = val
            continue
        row = pos[1]
        col = pos[0]
        canvas[row][col] = val_dict[val]
    return score, canvas
        
score, canvas = run_game(intcode)

for row in canvas:
    print(''.join(row))
    sum += row.count("♋️")
