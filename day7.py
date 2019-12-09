import csv

with open('input-files/day7.csv', 'r') as input_csv:
    reader = csv.reader(input_csv, delimiter=',')
    master_intcode = [instruction for instruction in reader][0]

def parse_intcode(intcode, init_input, amp_input, init=False, init_pos=0, halt_on_output=False, debug=False):
    pos = init_pos # initialize pointer position
    loop = True
    counter = 0 # counter to prevent infinite looping
    max_count = 1000

    input_counter = 0 # each cycle needs two inputs, this flag decides which to use

    value = init_input if init else amp_input
    
    while loop:
        # aim the compiler at the current position and read the input as an instruction
        pointer = intcode[pos]
        instruction = int(pointer) if len(pointer) < 2 or pointer == 99 else int(pointer[-2:])
        

        if instruction == 99 or counter > max_count:
            loop = False
            halt_string = 'HLT: 99' if instruction == 99 else 'HLT: counter_overload'
            halt_code = 99 if instruction == 99 else 0
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
            intcode[index] = value
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
            if halt_on_output:
                halt_code = 4
                return (value, halt_code, pos)
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

    return (value, halt_code, pos)

def run_thrusters(input_list, init_value, halt_code=99, ic=master_intcode):
    e_halt = False
    counter = 0
    pos_a, pos_b, pos_c, pos_d, pos_e = (0, 0, 0, 0, 0)
    init = True
    while not e_halt:
        a = parse_intcode(ic, input_list[0], init_value, init=init, init_pos=pos_a, halt_on_output=True, debug=True)
        output_a = a[0]
        pos_a = a[2]
        b = parse_intcode(ic, input_list[1], output_a, init=init, init_pos=pos_b, halt_on_output=True, debug=True)
        output_b = b[0]
        pos_b = b[2]
        c = parse_intcode(ic, input_list[2], output_b, init=init, init_pos=pos_c, halt_on_output=True, debug=True)
        output_c = c[0]
        pos_c = c[2]
        d = parse_intcode(ic, input_list[3], output_c, init=init, init_pos=pos_d, halt_on_output=True, debug=True)
        output_d = c[0]
        pos_d = d[2]
        e = parse_intcode(ic, input_list[4], output_d, init=init, init_pos=pos_e, halt_on_output=True, debug=True)
        output_e = e[0]
        pos_e = e[2]
        halt_e = e[1]
        init_value = output_e[0]
        counter += 1
        init = False
        # if counter % 100 == 0:
        #     print(counter, e[1])
        if halt_e == halt_code or counter == 10000:
            e_halt = True
    return (output_e[0], ic)

def generate_combinations(num_digits, min_individual_digit, max_individual_digit):
    low = int(str(min_individual_digit) * (num_digits-1))
    high = int(str(max_individual_digit) * num_digits)
    return_list = []
    if min_individual_digit == 0:
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
    else:
        for num in range(low, high):
            if int(max(list(str(num)))) <= max_individual_digit \
                and int(min(list(str(num)))) >= min_individual_digit \
                and len(set(str(num))) == num_digits:
                return_list.append(str(num))
        return return_list

# all_inputs = generate_combinations(5, 5, 9)

results = {}
# for input in all_inputs:
#     print(input)
#     results[''.join(input)] = run_thrusters(input, init_value=0, halt_code=4)[0]

# max_key = max(results, key=results.get)
# print(f'{max_key}: {results[max_key]}')

input = [str(i) for i in range(9, 4, -1)]
results[''.join(input)] = run_thrusters(input, init_value=0, halt_code=99)[0]

max_key = max(results, key=results.get)
print(f'{max_key}: {results[max_key]}')