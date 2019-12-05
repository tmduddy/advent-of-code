import csv

def rocket_equation(mass):
    fuel = (mass // 3) - 2
    return fuel if fuel > 0 else 0

with open('input-files/day2.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    input_data = [int(row[0]) for row in reader]

final_mass = []

for mass in input_data:
    new_mass = rocket_equation(mass)
    fuel_mass = new_mass
    while new_mass > 0:
        new_mass = rocket_equation(new_mass)
        fuel_mass += new_mass
    final_mass.append(fuel_mass)

print(sum(final_mass))
