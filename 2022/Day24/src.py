from collections import defaultdict
from math import lcm


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def read_map(lines):
    grid = []
    for i, line in enumerate(lines):
        if i in [0, len(lines) - 1]:
            continue
        line = line.strip()[1:-1]
        grid.append(list(line))
    
    return grid


def row_col_state_factory():
    return defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))


map_free_mem = row_col_state_factory()
def map_free(grid, row, col, state):
    if map_free_mem[row][col][state] is None:
        rows = len(grid)
        cols = len(grid[0])
        map_free_mem[row][col][state] = (
            grid[(row + state) % rows][col] != '^' and
            grid[(row - state) % rows][col] != 'v' and
            grid[row][(col + state) % cols] != '<' and
            grid[row][(col - state) % cols] != '>'
        )
    return map_free_mem[row][col][state]


def bfs(grid, rows, cols, states, src, dst, initial_state):
    res = row_col_state_factory()

    queue = []
    for wait in range(states):
        if map_free(grid, src[0], src[1], initial_state + wait + 1):
            res[src[0]][src[1]][initial_state + wait + 1] = wait + 1
            queue.append((src[0], src[1], initial_state + wait + 1))
    
    while len(queue) > 0:
        row, col, state = queue[0]
        del queue[0]

        dr = [0, 1, 0, -1, 0]
        dc = [1, 0, -1, 0, 0]

        for i in range(5):
            nr, nc, ns = row + dr[i], col + dc[i], (state + 1) % states
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if not map_free(grid, nr, nc, ns) or res[nr][nc][ns] is not None:
                continue
            res[nr][nc][ns] = res[row][col][state] + 1
            queue.append((nr, nc, ns))
    
    min_dist = 1e10
    min_state = None
    for state in range(states):
        if res[dst[0]][dst[1]][state] is not None and res[dst[0]][dst[1]][state] < min_dist:
            min_dist = res[dst[0]][dst[1]][state]
            min_state = state

    return min_dist + 1, (min_state + 1) % states


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    grid = read_map(lines)
    map_free_mem.clear()
    rows = len(grid)
    cols = len(grid[0])
    states = lcm(rows, cols)

    p1_ans, state_1 = bfs(grid, rows, cols, states, (0, 0), (rows - 1, cols - 1), 0)
    
    round_2, state_2 = bfs(grid, rows, cols, states, (rows - 1, cols - 1), (0, 0), state_1)
    round_3, _ = bfs(grid, rows, cols, states, (0, 0), (rows - 1, cols - 1), state_2)
    p2_ans = p1_ans + round_2 + round_3

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)