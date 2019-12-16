with open('input-files/day6.csv', 'r') as map_file:
    map_data = [row for row in map_file]

map_list = [tuple(row.strip().split(')')) for row in map_data]
items_set = set()
orbit_dict = {}
for pair in map_list:
    orbit_dict[pair[0]] = pair[1]
    items_set.add(pair[0])
    items_set.add(pair[1])

total_orbits = 0

for k,v in orbit_dict.items():
    if orbit_dict.get(v, False):
        orbit_dict[k] += f',{orbit_dict[v]}'


print(orbit_dict)
print(total_orbits)
