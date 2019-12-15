def get_index(intcode, param_mode, pos, rel_base):
    param_mode = int(param_mode)
    if param_mode == 0:
        index = int(intcode[pos]) 
    elif param_mode == 1:
        index = int(pos)
    elif param_mode == 2:
        index = int(intcode[pos]) + rel_base
    return index

def write_value_to_index(intcode, index, value):
    if len(intcode) <= index:
        length_needed = (index - len(intcode))+1
        intcode = intcode + [0] * length_needed
    intcode[index] = value
    return intcode

def read_value_from_index(intcode, index, ret_int=True):
    if len(intcode) <= index:
        length_needed = (index - len(intcode))+1
        intcode = intcode + [0] * length_needed
    return (int(intcode[index]) if ret_int else intcode[index], intcode)

def parse_intcode(ic, init_input=None, later_input=None, init=True, init_pos=0, init_rel_base=0, halt_on_output=False, print_out=True, debug=False):
    intcode = ic
    pos = init_pos
    rel_base = init_rel_base
    counter = 0 # counter to prevent infinite looping
    max_count = 1000000
    
    while True:
        # aim the compiler at the current position and read the input as an instruction
        pointer = str(read_value_from_index(intcode, pos)[0])
        # valid instruction strings are /(\d)/, /\d*(\d\d)/, /99/
        instruction = int(pointer) if len(pointer) < 2 or pointer == 99 else int(pointer[-2:])
        # set the INP value based on cycle count (init T/F)
        value = init_input if init else later_input

        if instruction == 99 or counter > max_count:
            halt_code = 99 if instruction == 99 else 0
            if debug:
                halt_string = 'HLT: 99' if instruction == 99 else 'HLT: counter_overload'
                print(halt_string)
            break

        # account for varying number of digits in instruction
        # 11002 = mode-mode-mode-instruction = immediate-immediate-position-instruction
        param_1_mode = 0 if len(pointer) < 3 else int(pointer[-3])
        param_2_mode = 0 if len(pointer) < 4 else int(pointer[-4])
        param_3_mode = 0 if len(pointer) < 5 else int(pointer[-5])

        ### INS: 1, 2 ###
        if instruction in [1, 2]:
            # add or multiply two params, output to third
            index_1 = get_index(intcode, param_1_mode, pos+1, rel_base)
            index_2 = get_index(intcode, param_2_mode, pos+2, rel_base)
            index_3 = get_index(intcode, param_3_mode, pos+3, rel_base)
            
            param_1, intcode = read_value_from_index(intcode, index_1)
            param_2, intcode = read_value_from_index(intcode, index_2)

            result =  (param_1 + param_2) if instruction == 1 else (param_1 * param_2)

            intcode = write_value_to_index(intcode, index_3, str(result))
            pos += 4

            if debug:
                op = '+' if instruction == 1 else '*'
                print(f'\tAOM: {param_1} {op} {param_2} = {result} to index {index_3}')
                print(f'\t\tMODES: {param_1_mode}, {param_2_mode}, {param_3_mode}')

        ### INS: 3 ###
        elif instruction == 3:
            # read input from value
            index = get_index(intcode, param_1_mode, pos+1, rel_base)

            intcode = write_value_to_index(intcode, index, value)

            #init = False
            if debug:
                print(f'\tINP: storing input {value} at index: {index}')
            pos += 2

        ### INS: 4 ###
        elif instruction == 4:
            # output value, potentially HALT based on settings
            index = get_index(intcode, param_1_mode, pos+1, rel_base)
            param_1, intcode = read_value_from_index(intcode, index)

            value = param_1
            pos += 2
            
            if print_out:
                print(f'\tOUT = {param_1}')

            if halt_on_output:
                halt_code = 4
                if debug:
                    print(f'HLT: halt on out enabled')
                break
        ### INS: 5, 6 ###    
        elif instruction in [5, 6]:
            # JUMP if True/False
            index_1 = get_index(intcode, param_1_mode, pos+1, rel_base)
            index_2 = get_index(intcode, param_2_mode, pos+2, rel_base)
            
            param_1, intcode = read_value_from_index(intcode, index_1)
            param_2, intcode = read_value_from_index(intcode, index_2)

            if instruction == 5:
                pos = param_2 if param_1 != 0 else (pos+3)
                
                if debug and param_1 != 0:
                    print(f'\tJIT: {param_1} != 0; pos JUMP to {param_2}')
                elif debug:
                    print(f'\tJIT: {param_1} == 0; pos += 3 ({pos})')
            elif instruction == 6:
                pos = param_2 if param_1 == 0 else (pos+3)

                if debug and param_1 == 0:
                    print(f'\tJIF: {param_1} == 0; pos JUMP to {param_2}')
                elif debug:
                    print(f'\tJIF: {param_1} != 0; pos += 3 ({pos})')
        ### INS: 7, 8 ###
        elif instruction in [7, 8]:
            # write 1/0 for T/F eval of A > B or A == B
            index_1 = get_index(intcode, param_1_mode, pos+1, rel_base)
            index_2 = get_index(intcode, param_2_mode, pos+2, rel_base)
            index_result = get_index(intcode, param_3_mode, pos+3, rel_base)
            
            param_1, intcode = read_value_from_index(intcode, index_1)
            param_2, intcode = read_value_from_index(intcode, index_2)

            if instruction == 7:
                result = 1 if (param_1 < param_2) else 0
                intcode = write_value_to_index(intcode, index_result, result)
                intcode[index_result] = result
                
                if debug:
                    op = "<" if (param_1 < param_2) else "!<"
                    print(f'\t1G2: {param_1} {op} {param_2}; storing {result} in {index_result}')
                    print(f'\t\tMODES: {param_1_mode}, {param_2_mode}, {param_3_mode}')
            else:
                result = 1 if (param_1 == param_2) else 0
                intcode = write_value_to_index(intcode, index_result, result)
                
                if debug:
                    op = '==' if (param_1 == param_2) else '!='
                    print(f'\t1E2: {param_1} {op} {param_2}; storing {result} in {index_result}')
                    print(f'\t\tMODES: {param_1_mode}, {param_2_mode}, {param_3_mode}')
            pos += 4
        ### INS: 9 ###
        elif instruction == 9:
            # update rel_base
            index_1 = get_index(intcode, param_1_mode, pos+1, rel_base)
            param_1, intcode = read_value_from_index(intcode, index_1)
            
            if debug:
                print(f'\tRLP: r_b = (r_b + p_1); ({rel_base} + intcode[{index_1}]) = {rel_base+param_1}')

            rel_base += param_1
            pos += 2
        ### INS: something went wrong ###
        else:
            halt_code = 'err'
            print(counter, pos, pointer, instruction, param_1_mode, param_2_mode)
            print('\t***bad instruction: ' + str(instruction))
            break
        ### END INSTRUCTIONS ###
        if debug:
            print(f'\t\tPOS: {pos}; REL: {rel_base}')
        counter += 1
    # end while #
    return (value, halt_code, pos, rel_base, intcode)