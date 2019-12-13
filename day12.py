def gen_moon_data():
    with open('input-files/day12.csv', 'r') as f:
        moon_data = []
        for row in f:
            row_list = []
            row_data = row.strip().split(',')
            for coord in row_data:
                row_list.append(int(coord.split('=')[1].replace('>', '')))
            moon_data.append(row_list)
    return moon_data

def apply_accel(moon_data, moon_vel):
    compare_pos = moon_data.copy()
    new_moon_vel = moon_vel.copy()
    for i in range(len(moon_data)):
        pos = moon_data[i]
        compare_pos.remove(pos)
        for moon in compare_pos:
            for j in range(3):
                if pos[j] < moon[j]:
                    new_moon_vel[i][j] += 1
                elif pos[j] > moon[j]:
                    new_moon_vel[i][j] -= 1
        compare_pos = moon_data.copy()
    return new_moon_vel

def apply_vel(moon_data, moon_vel):
    new_moon_data = moon_data.copy()
    for i in range(len(new_moon_data)):
        moon = new_moon_data[i]
        vel = moon_vel[i]
        for j in range(len(moon)):
            moon[j] += vel[j]
    return new_moon_data
        
def run_cycles(num_cycles, init_moon_data, init_moon_vel):
    moon_data = init_moon_data.copy()
    moon_vel = init_moon_vel.copy()
    for _ in range(num_cycles):
        moon_vel = apply_accel(moon_data, moon_vel)
        moon_data = apply_vel(moon_data, moon_vel)
    return (moon_data, moon_vel)

def repeat_history(init_moon_data, init_moon_vel):
    moon_data = init_moon_data.copy()
    moon_vel = init_moon_vel.copy()
    counter = 0
    visited_pos = []
    while True:
        moon_vel = apply_accel(moon_data, moon_vel)
        moon_data = apply_vel(moon_data, moon_vel)
        if moon_data in visited_pos:
            break
        visited_pos.append(moon_data)
        counter += 1


def calc_energy(moon_data, moon_vel):
    pot_en = []
    kin_en = []
    for moon in moon_data:
        pot_en.append(sum(list(map(abs, moon))))
    for moon in moon_vel:
        kin_en.append(sum(list(map(abs, moon))))
    
    result = sum([i*j for i, j in zip(pot_en, kin_en)])
    return result

moon_data = gen_moon_data()
moon_vel = [[0, 0, 0] for moon in moon_data]

### part A ###
# final_moons, final_vels = run_cycles(1000, moon_data, moon_vel)
# print(calc_energy(final_moons, final_vels))
### end part A ###


### part B ###
repeat_history(moon_data, moon_vel)
### end part B ###