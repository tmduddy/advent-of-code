import csv

def get_picture_data():
    with open('input-files/day8.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            return [i for i in row[0]]

print(get_picture_data())