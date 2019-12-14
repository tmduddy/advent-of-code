import numpy as np

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
    for i in range(num_cycles):
        moon_vel = apply_accel(moon_data, moon_vel)
        moon_data = apply_vel(moon_data, moon_vel)
        if i % 1000000 == 0:
            print(int(i/1000000))
    return (moon_data, moon_vel)

def calc_energy(moon_data, moon_vel):
    pot_en = []
    kin_en = []
    for moon in moon_data:
        pot_en.append(sum(list(map(abs, moon))))
    for moon in moon_vel:
        kin_en.append(sum(list(map(abs, moon))))
    
    result = sum([i*j for i, j in zip(pot_en, kin_en)])
    return result

def apply_accel_one_dim(moon_data, moon_vel):
    compare_pos = moon_data.copy()
    new_moon_vel = moon_vel.copy()
    for i in range(len(moon_data)):
        pos = moon_data[i]
        compare_pos.remove(pos)
        for moon in compare_pos:
            if pos < moon:
                new_moon_vel[i] += 1
            elif pos > moon:
                new_moon_vel[i] -= 1
        compare_pos = moon_data.copy()
    return new_moon_vel

def apply_vel_one_dim(moon_data, moon_vel):
    new_moon_data = moon_data.copy()
    for i in range(len(new_moon_data)):
        new_moon_data[i] += moon_vel[i]
    return new_moon_data

def repeat_history(init_moon_data, init_moon_vel):
    moon_data = init_moon_data.copy()
    moon_vel = init_moon_vel.copy()
    p_xs = [moon[0] for moon in moon_data]
    p_ys = [moon[1] for moon in moon_data]
    p_zs = [moon[2] for moon in moon_data]

    v_xs = [vel[0] for vel in moon_vel]
    v_ys = [vel[1] for vel in moon_vel]
    v_zs = [vel[2] for vel in moon_vel]

    x_counter, y_counter, z_counter = (0,0,0)

    while True:
        v_xs = apply_accel_one_dim(p_xs, v_xs)
        p_xs = apply_vel_one_dim(p_xs, v_xs)
        if x_counter == 0 or v_xs != [0, 0, 0, 0]:
            x_counter += 1
            continue
        if p_xs == [moon[0] for moon in init_moon_data]:
            print(f'x: {x_counter}')
            break
    
    while True:
        v_ys = apply_accel_one_dim(p_ys, v_ys)
        p_ys = apply_vel_one_dim(p_ys, v_ys)
        if y_counter == 1 or v_ys != [0, 0, 0, 0]:
            y_counter += 1
            continue
        if p_ys == [moon[1] for moon in init_moon_data]:
            print(f'y: {y_counter}')
            break
        
    while True:
        v_zs = apply_accel_one_dim(p_zs, v_zs)
        p_zs = apply_vel_one_dim(p_zs, v_zs)
        if z_counter == 0 or v_zs != [0, 0, 0, 0]:
            z_counter += 1
            continue
        if p_zs == [moon[2] for moon in init_moon_data]:
            print(f'z: {z_counter}')
            break
    
    print(np.lcm.reduce([x_counter+2, y_counter+2, z_counter+2])) # unclear why +2 works
        

moon_data = gen_moon_data()
moon_vel = [[0, 0, 0] for moon in moon_data]

### part A ###
# final_moons, final_vels = run_cycles(1000, moon_data, moon_vel)
# print(calc_energy(final_moons, final_vels))
# print(final_moons)
### end part A ###


### part B ###
repeat_history(moon_data, moon_vel)
### end part B ###