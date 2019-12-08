import csv

with open('input-files/day6.csv', 'r') as map_file:
    reader = csv.reader(map_file, delimiter=',')
    map_list = [row[0] for row in reader]

map_list_unnested = [i.split(')') for i in map_list]
map_dict = {}
for pair in map_list_unnested:
    