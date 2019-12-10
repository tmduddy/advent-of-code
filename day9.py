import csv

def get_fresh_intcode():
    with open('input-files/day9.csv', 'r') as input_csv:
        reader = csv.reader(input_csv, delimiter=',')
        return [instruction for instruction in reader][0]

def parse_intcode(ic, init_input, amp_input, init=False, init_pos=0, halt_on_output=False, debug=False):
    intcode = ic
    pos = init_pos # initialize pointer position
    loop = True
    counter = 0 # counter to prevent infinite looping
    max_count = 100000
    
    while loop:
        # aim the compiler at the current position and read the input as an instruction
        pointer = intcode[pos]
        instruction = int(pointer) if len(pointer) < 2 or pointer == 99 else int(pointer[-2:])
        
        # set the INP value based on cycle count (init T/F)
        value = init_input if init else amp_input

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
                print(f'\tAOM: {param_1} {op} {param_2} = {result} to index {intcode[pos+3]}')
                #print(f'\t -> AOM: index: {index_1}, {index_2} to index {intcode[pos+3]}')

            intcode[int(intcode[pos+3])] = str(result)
            pos += 4
        elif instruction == 3:
            index = int(intcode[pos+1])
            intcode[index] = value
            init = False
            if debug:
                print(f'\tINP: storing input {value} at index: {index}')
            pos += 2
        elif instruction == 4:
            param_1 = intcode[int(intcode[pos+1])] if param_1_mode == 0 else intcode[pos+1]
            if debug:
                print(f'\tOUT = {param_1}')
            value = param_1
            pos += 2
            if halt_on_output:
                halt_code = 4
                if debug:
                    print(f'HLT: halt on out enabled')
                break
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
            print('\t***bad instruction: ' + str(instruction))
            loop = False
            break
        counter += 1

    return (value, halt_code, pos, intcode)

def run_thrusters(input_list, init_value, halt_code=99, num_amps=5, debug=False):
    a_ic, b_ic, c_ic, d_ic, e_ic = (get_fresh_intcode(), get_fresh_intcode(), get_fresh_intcode(), get_fresh_intcode(), get_fresh_intcode())
    a_pos, b_pos, c_pos, d_pos, e_pos = (0, 0, 0, 0, 0)
    a_init, b_init, c_init, d_init, e_init = (i for i in input_list)
    # initial conditions so that loop 1 is different
    e_out = init_value
    e_halt = False
    init = True
    counter = 0
    while not e_halt:
        a = parse_intcode(a_ic, a_init, e_out, init, a_pos, halt_on_output=True, debug=debug)
        a_out = a[0]
        a_pos = a[2]
        a_ic = a[3]
        b = parse_intcode(b_ic, b_init, a_out, init, b_pos, halt_on_output=True, debug=debug)
        b_out = b[0]
        b_pos = b[2]
        b_ic = b[3]
        c = parse_intcode(c_ic, c_init, b_out, init, c_pos, halt_on_output=True, debug=debug)
        c_out = c[0]
        c_pos = c[2]
        c_ic = c[3]
        d = parse_intcode(d_ic, d_init, c_out, init, d_pos, halt_on_output=True, debug=debug)
        d_out = d[0]
        d_pos = d[2]
        d_ic = d[3]
        e = parse_intcode(e_ic, e_init, d_out, init, e_pos, halt_on_output=True, debug=debug)
        e_out = e[0]
        e_code = e[1]
        e_pos = e[2]
        e_ic = e[3]
        
        init = False
        counter += 1
        if e_code == 99:
            break
    # end while
    #print(counter)
    return int(e_out)

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

all_inputs = generate_combinations(5, 5, 9)
results = {}
for input in all_inputs:
    results[''.join(input)] = run_thrusters(input, init_value=0, halt_code=99, debug=False)

max_key = max(results, key=results.get)
print(f'{max_key}: {results[max_key]}')

# print(results)