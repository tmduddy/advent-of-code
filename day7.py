import csv

with open('input-files/day7.csv', 'r') as input_csv:
    reader = csv.reader(input_csv, delimiter=',')
    master_intcode = [instruction for instruction in reader][0]

def parse_intcode(intcode, init_input, amp_input, debug=False):
    pos = 0 # initialize pointer position
    loop = True
    counter = 0 # counter to prevent infinite looping
    max_count = 1000

    input_counter = 0 # each cycle needs two inputs, this flag decides which to use

    value = init_input
    
    while loop:
        # aim the compiler at the current position and read the input as an instruction
        pointer = intcode[pos]
        instruction = int(pointer) if len(pointer) < 2 or pointer == 99 else int(pointer[-2:])
        

        if instruction == 99 or counter > max_count:
            loop = False
            halt_string = 'HLT: 99' if instruction == 99 else 'HLT: counter_overload'
            if debug:
                print(halt_string)
            break

        # account for varying number of digits in instruction
        param_1_mode = 0 if len(pointer) < 3 else pointer[-3]
        param_2_mode = 0 if len(pointer) < 4 else pointer[-4]

        if instruction in [1, 2]:
            index_1 = int(intcode[pos+1]) if int(param_1_mode) == 0 else pos+1
            index_2 = int(intcode[pos+2]) if int(param_2_mode) == 0 else pos+2
            
            param_1 = intcode[index_1]
            param_2 = intcode[index_2]

            result =  (int(param_1) + int(param_2)) if instruction == 1 else (int(param_1) * int(param_2))

            op = '+' if instruction == 1 else '*'
            if debug:
                print(f'\tAOM: {param_1} {op} {param_2} = {result}')
                #print(f'\t -> AOM: index: {index_1}, {index_2} to index {intcode[pos+3]}')

            intcode[int(intcode[pos+3])] = str(result)
            pos += 4
        elif instruction == 3:
            index = int(intcode[pos+1])
            intcode[index] = str(init_input) if input_counter == 0 else str(amp_input)
            input_counter += 1
            if debug:
                print(f'INP: storing input {value} at index: {index}')
            pos += 2
        elif instruction == 4:
            param_1 = intcode[int(intcode[pos+1])] if param_1_mode == 0 else intcode[pos+1]
            if debug:
                print(f'OUT = {param_1}')
            value = param_1
            pos += 2
        elif instruction in [5, 6]:
            index_1 = int(intcode[pos+1]) if int(param_1_mode) == 0 else pos+1
            index_2 = int(intcode[pos+2]) if int(param_2_mode) == 0 else pos+2
            
            param_1 = int(intcode[index_1])
            param_2 = int(intcode[index_2])

            if instruction == 5:
                if param_1 != 0:
                    pos = param_2
                    if debug:
                        print(f'\tJIT: {param_1} != 0; pos JUMP to {param_2}')
                else:
                    pos += 3
                    if debug:
                        print(f'\tJIT: {param_1} == 0; pos += 3 ({pos})')
            elif instruction == 6:
                if param_1 == 0:
                    pos = param_2
                    if debug:
                        print(f'\tJIF: {param_1} == 0; pos JUMP to {param_2}')
                else:
                    pos += 3
                    if debug:
                        print(f'\tJIF: {param_1} != 0; pos += 3 ({pos})')
        elif instruction in [7, 8]:
            index_1 = int(intcode[pos+1]) if int(param_1_mode) == 0 else pos+1
            index_2 = int(intcode[pos+2]) if int(param_2_mode) == 0 else pos+2
            index_result = int(intcode[pos+3])

            param_1 = int(intcode[index_1])
            param_2 = int(intcode[index_2])

            if instruction == 7:
                result = 1 if (param_1 < param_2) else 0
                op = "<" if (param_1 < param_2) else "!<"
                intcode[index_result] = result
                if debug:
                    print(f'\t1G2: {param_1} {op} {param_2}; storing {result} in {index_result}')
            else:
                result = 1 if (param_1 == param_2) else 0
                op = '==' if (param_1 == param_2) else '!='
                intcode[index_result] = result
                if debug:
                    print(f'\t1E2: {param_1} {op} {param_2}; storing {result} in {index_result}')
            pos += 4

        else:
            print(counter, pos, pointer, instruction, param_1_mode, param_2_mode)
            print('bad instruction: ' + str(instruction))
            loop = False
            break
        counter += 1

    return value

def run_thrusters(input_list, intcode=master_intcode):
    output_a = parse_intcode(intcode, input_list[0], 0)
    output_b = parse_intcode(intcode, input_list[1], output_a)
    output_c = parse_intcode(intcode, input_list[2], output_b)
    output_d = parse_intcode(intcode, input_list[3], output_c)
    output_e = parse_intcode(intcode, input_list[4], output_d)

    return output_e

def generate_combinations(num_digits, min_individual_digit, max_individual_digit):
    low = int(str(min_individual_digit) * (num_digits-1))
    high = int(str(max_individual_digit) * num_digits)
    return_list = []
    for num in range(low, high):
        '''
            if:
                the max digit <= max_ind_digit
                AND (
                    number of unique digits == num_digits
                    OR (
                        number of unique digits in '0'+number == num digits
                        AND len('0'+number) == num_digits
                    )
                ): return_list.append(num or '0'+num as appropriate)
        '''
        if int(max(list(str(num)))) <= max_individual_digit \
            and ( \
                (len(set('0' + str(num))) == num_digits \
                    and len(str(num)) == (num_digits - 1))
                or len(set(str(num))) == num_digits
            ):
            str_num = '0'*(num_digits - len(str(num))) + str(num)
            return_list.append(str_num)
    return return_list

all_inputs = generate_combinations(5, 0, 4)

results = {}
for input in all_inputs:
    results[''.join(input)] = run_thrusters(input)

max_key = max(results, key=results.get)
print(f'{max_key}: {results[max_key]}')