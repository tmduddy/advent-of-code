intcode = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,9,19,23,2,13,23,27,2,27,13,31,2,31,10,35,1,6,35,39,1,5,39,43,1,10,43,47,1,5,47,51,1,13,51,55,2,55,9,59,1,6,59,63,1,13,63,67,1,6,67,71,1,71,10,75,2,13,75,79,1,5,79,83,2,83,6,87,1,6,87,91,1,91,13,95,1,95,13,99,2,99,13,103,1,103,5,107,2,107,10,111,1,5,111,115,1,2,115,119,1,119,6,0,99,2,0,14,0]

#intcode = [2,3,0,3,99]

pos = 0
pointer = intcode[pos]
while pointer != 99:
    if pointer == 1:
        sum_index_1  = intcode[pos+1]
        sum_index_2  = intcode[pos+2]
        sum_location = intcode[pos+3]
        intcode[sum_location] = intcode[sum_index_1] + intcode[sum_index_2]
    elif pointer == 2:
        prod_index_1  = intcode[pos+1]
        prod_index_2  = intcode[pos+2]
        prod_location = intcode[pos+3]
        intcode[prod_location] = intcode[prod_index_1] * intcode[prod_index_2]
    else:
        print('invalid pointer')
    pos += 4
    pointer = intcode[pos]
print(intcode)
