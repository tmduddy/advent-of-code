import csv

goal = 19690720

with open('input-files/day5.csv', 'r') as input_csv:
    reader = csv.reader(input_csv, delimiter=',')
    test_intcode = [instruction for instruction in reader][0]

def parse_intcode(intcode, init_input=1):
    pos = 0
    loop = True
    counter = 0
    value = init_input

    while loop:
        pointer = intcode[pos]
        instruction = int(pointer) if len(pointer) < 2 or pointer == 99 else int(pointer[-2:])
        
        if instruction == 99 or counter > 100000:
            loop = False
            halt_string = '99: halted' if instruction == 99 else 'counter_overload: halted'
            print(halt_string)
            break

        param_1_mode = 0 if len(pointer) < 3 else pointer[-3]
        param_2_mode = 0 if len(pointer) < 4 else pointer[-4]

        if instruction in [1, 2]:
            index_1 = int(intcode[pos+1]) if int(param_1_mode) == 0 else pos+1
            index_2 = int(intcode[pos+2]) if int(param_2_mode) == 0 else pos+2
            
            param_1 = intcode[index_1]
            param_2 = intcode[index_2]

            result =  (int(param_1) + int(param_2)) if instruction == 1 else (int(param_1) * int(param_2))

            op = '+' if instruction == 1 else '*'
            print(f'\t{param_1} {op} {param_2} = {result}')
            print(f'\t\t{index_1}, {index_2} to index {intcode[pos+3]}')
            print(f'\t\t{param_1_mode}, {param_2_mode} to index {intcode[pos+3]}')

            intcode[int(intcode[pos+3])] = str(result)
            pos += 4
        elif instruction == 3:
            index = int(intcode[pos+1])
            intcode[index] = str(value)
            print(f'storing value: {value} in position: {index}')
            pos += 2
        elif instruction == 4:
            param_1 = intcode[int(intcode[pos+1])] if param_1_mode == 0 else intcode[pos+1]
            print(f'{param_1} = output')
            value = param_1
            pos += 2
        else:
            print(counter, pos, pointer, instruction, param_1_mode, param_2_mode)
            print('bad instruction: ' + str(instruction))
            loop = False
            break
        #print(pos, pointer, instruction, param_1_mode, param_2_mode)
        counter += 1

parse_intcode(test_intcode)
