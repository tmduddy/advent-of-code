import csv
from pprint import pprint

def get_picture_data():
    with open('input-files/day8.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            return [i for i in row[0]]

def min_max_from_dict(dct, return_min=True):
    min_max_key = min(dct, key=dct.get) if return_min else max(dct, key=dct.get)
    return (min_max_key, dct[min_max_key])

def list_to_chunks(lst, num_chunks):
    chunk_size = int(len(lst) / num_chunks)
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def picture_data_to_lists(picture_data, num_layers, width, height):
    picture_layers = list(list_to_chunks(picture_data, num_layers))

    all_data = []
    for layer in picture_layers:
        all_data.append(list(list_to_chunks(layer, height)))
    return all_data

def count_digit(picture_data_lists, digit):
    digits = {}
    for i in range(len(picture_data_lists)):
        layer = picture_data_lists[i]
        sum = 0
        for row in layer:
            sum += row.count(digit)
        digits[i] = sum
    return digits

def stack_images(picture_data_lists, num_layers, width, height):
    canvas = [[0 for x in range(width)] for y in range(height)] 
    for layer in picture_data_lists[::-1]:
        for i in range(len(layer)):
            row = layer[i]
            for j in range(len(row)):
                pixel = row[j]
                if pixel == '2':
                    continue
                elif pixel == '1':
                    pixel_value = "◼️ "
                else:
                    pixel_value = "◻️ "
                canvas[i][j] = pixel_value
    return canvas


def get_part_a(picture_data_lists):
    zeros_result = count_digit(picture_data_lists, '0')
    # layer_index is the index of the layer with the min number of zeros
    layer_index = min_max_from_dict(zeros_result, return_min=True)[0]
    num_ones = count_digit(picture_data_lists, '1')[layer_index]
    num_twos = count_digit(picture_data_lists, '2')[layer_index]

    print(layer_index)
    print(num_ones, num_twos)
    print(num_ones * num_twos)

picture_data = get_picture_data()

width = 25
height = 6
num_layers = int(len(picture_data) / (width*height))

picture_data_lists = picture_data_to_lists(picture_data, num_layers, width, height)

for i in stack_images(picture_data_lists, num_layers, width, height):
    print(''.join(i))