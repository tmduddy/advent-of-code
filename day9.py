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