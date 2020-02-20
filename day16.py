from tqdm import tqdm

with open('input-files/day16.csv', 'r') as f:
    input_data = [list(row) for row in f][0]

input_data = [input_data for _ in range(10000)]
input_data = [int(item) for sublist in input_data for item in sublist]
input_data = [1,2] * 20
output_key = int(''.join(list(map(str, input_data[:8]))))
print(output_key)
num_phases = 100

for phase in range(num_phases):
    new_data = []
    if phase == 0:
        data = input_data
    for i in range(len(data)):
        pattern = [[j]*(i+1) for j in [0, 1, 0, -1]]
        flat_pattern = [int(item) for sublist in pattern for item in sublist]
        
        while len(flat_pattern) < len(data)+1:
            flat_pattern += flat_pattern
        
        stripped_flat_pattern = flat_pattern[1:len(data)+2]
        local_sum = 0
        local_data = data.copy()

        for k in range(len(data)):
            if i>0:
                local_data = local_data[i-1:]
                stripped_flat_pattern = stripped_flat_pattern[i-1:]
            if k >= len(local_data):
                continue
            local_sum += local_data[k] * stripped_flat_pattern[k]
        
        local_data = []
        new_digit = int(str(local_sum)[-1])
        new_data.append(new_digit)
    data = new_data.copy()
    #if phase % 5 == 0 or phase == max(range(num_phases)):
    print(f'phase {phase} result: {"".join(list(map(str, data)))[:50]}')
print(f'input_data[{output_key}] = {data[output_key:output_key+8]}')