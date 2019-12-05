import csv

def rocket_function(mass):
    return (mass // 3) - 2

with open('day1.csv', 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',')
    input_data = [int(row[0]) for row in reader]

output_fuel = (list(map(rocket_function, input_data)))

print(sum(output_fuel))
