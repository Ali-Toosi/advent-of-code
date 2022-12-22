def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def read_map(lines):
    grid = []
    max_len = 0
    for line in lines:
        line = line.replace('\n', '')
        if not line.strip():
            break
        grid.append(list(line))
        max_len = max(max_len, len(grid[-1]))
    
    for row in grid:
        while len(row) < max_len:
            row.append(' ')

    return grid


def read_instructions(lines):
    raw = lines[-1].strip()
    res = []

    current = ""
    for char in raw:
        if char in ['L', 'R']:
            if current:
                res.append(int(current))
                current = ""
            res.append(char)
            continue
        
        current += char
    
    if current:
        res.append(int(current))
    
    return res


def create_offsets(grid):
    row_offset = []
    col_offset = []
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        lcnt = 0
        while grid[row][lcnt] == ' ':
            lcnt += 1
        rcnt = 0
        while grid[row][cols - 1 - rcnt] == ' ':
            rcnt += 1
        
        row_offset.append((lcnt, rcnt))
    
    for col in range(cols):
        tcnt = 0
        while grid[tcnt][col] == ' ':
            tcnt += 1
        bcnt = 0
        while grid[rows - 1 - bcnt][col] == ' ':
            bcnt += 1
        
        col_offset.append((tcnt, bcnt))
    
    return row_offset, col_offset


def move(grid, row_offset, col_offset, row, col, d, inst):
    if inst == "L":
        return row, col, (d + 3) % 4
    if inst == "R":
        return row, col, (d + 1) % 4
    
    rows = len(grid)
    cols = len(grid[0])

    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]

    for i in range(inst):
        nr, nc = (row + dr[d] + rows) % rows, (col + dc[d] + cols) % cols
        if grid[nr][nc] == ' ':
            if d == 0:
                nc = row_offset[nr][0]
            if d == 2:
                nc = cols - 1 - row_offset[nr][1]
            if d == 1:
                nr = col_offset[nc][0]
            if d == 3:
                nr = rows - 1 - col_offset[nc][1]
            
        assert grid[nr][nc] != ' '

        if grid[nr][nc] == '#':
            break
        
        row, col = nr, nc
    
    return row, col, d


for file_name in ["input_p1.txt", "sample_p1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    grid = read_map(lines)
    instructions = read_instructions(lines)
    row_offset, col_offset = create_offsets(grid)

    r, c, d = 0, row_offset[0][0], 0
    for instruction in instructions:
        r, c, d = move(grid, row_offset, col_offset, r, c, d, instruction)
    
    p1_ans = (r + 1) * 1000 + (c + 1) * 4 + d

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)