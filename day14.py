from math import ceil
with open('input-files/day14.csv', 'r') as f:
    data = [row.strip().split(' => ') for row in f]

all_recipes = [(i[0].split(', '), i[1]) for i in data]
rec_dict = {recipe[1].split(' ')[1]: [int(recipe[1].split(' ')[0]), recipe[0]] for recipe in all_recipes}

fuel_recipe = rec_dict['FUEL']

def get_ore_requirements(recipe):
    pass

for item in fuel_recipe[1]:
    quantity_needed = item.split(' ')[0]
    quantity_made, item_recipe = tuple(rec_dict[item.split(' ')[1]])
    print(quantity_needed, quantity_made, item_recipe)
    new_recipe_dict = {}