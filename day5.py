import csv

goal = 19690720

with open('input-files/day5.csv', 'r') as input_csv:
    reader = csv.reader(input_csv, delimiter=',')
    test_intcode = [instruction for instruction in reader][0]

def parse_intcode(intcode):
    pos = 0
    pointer = intcode[pos]
    loop = True
    while loop:
        if pointer == 99:
            loop = False
            break

    while pointer != 99:
        index_1 = intcode[pos+1]
        index_2 = intcode[pos+2]
        index_result = intcode[pos+3]
        if pointer == 1:
            intcode[index_result] = intcode[index_1] + intcode[index_2]
            pos += 4
        elif pointer == 2:
            intcode[index_result] = intcode[index_1] * intcode[index_2]
            pos += 4
        elif pointer == 3:
            param_three_input = 1
            intcode[index_1] = param_three_input
            pos += 2
        elif pointer == 4:
            param_four_output = intcode[index_1]
            print(param_four_output)
            pos += 2
        else:
            print('invalid pointer')
        pointer = intcode[pos]
    return intcode

#print(parse_intcode(test_intcode))
