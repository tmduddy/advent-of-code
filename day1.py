import csv

with open('input-files/day1.csv', 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',')
    input_data = [int(row[0]) for row in reader]

output_fuel = (list(map(lambda x: (x//3) - 2, input_data)))

print(sum(output_fuel))
