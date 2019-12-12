def gen_moon_data():
    with open('input-files/day12.csv', 'r') as f:
        moon_data = []
        for row in f:
            row_list = []
            row_data = row.strip().split(',')
            for coord in row_data:
                row_list.append(coord.split('=')[1])
            moon_data.append(row_list)
    return moon_data

def apply_accel(moon_data, moon_vel):
    for vel in moon_vel:
        pass        
        


moon_data = gen_moon_data()

