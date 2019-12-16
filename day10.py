with open('input-files/day10.csv', 'r') as f:
    grid = [list(row.strip()) for row in f]

for row in range(len(grid)):
    for col in range(len(grid[row])):
        point = grid[row][col]
        if point == '.':
            continue
        

