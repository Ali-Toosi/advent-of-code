def calc_load(grid, col, count_dots=False):
    dots = 0
    res = 0
    for r in range(len(grid)):
        if grid[r][col] == "O":
            res += len(grid) - r
            if count_dots:
                res += dots
        elif grid[r][col] == ".":
            dots += 1
        else:
            dots = 0
    return res


def add(r, c, d):
    return r + d[0], c + d[1]


def at(grid, loc):
    return grid[loc[0]][loc[1]]


def isin(grid, loc):
    return 0 <= loc[0] < len(grid) and 0 <= loc[1] < len(grid[0])


def next(grid, r, c, d):
    new_loc = add(r, c, d)
    if isin(grid, new_loc):
        return True, False, new_loc
    nr, nc = r, c
    if d[0] == 1:
        nc += 1
        nr = 0
    elif d[0] == -1:
        nr = len(grid) - 1
        nc += 1
    elif d[1] == 1:
        nc = 0
        nr += 1
    else:
        nc = len(grid[0]) - 1
        nr += 1
    if isin(grid, (nr, nc)):
        return True, True, (nr, nc)
    return False, False, False


def swap(grid, loc1, loc2):
    grid[loc1[0]][loc1[1]], grid[loc2[0]][loc2[1]] = grid[loc2[0]][loc2[1]], grid[loc1[0]][loc1[1]]


def tilt(grid, d):
    rc_map = {
        (0, 1): (0, 0),
        (0, -1): (0, len(grid[0]) - 1),
        (1, 0): (0, 0),
        (-1, 0): (len(grid) - 1, 0)
    }
    grid = [[grid[r][c] for c in range(len(grid[0]))] for r in range(len(grid))]
    had_movement = True
    while had_movement:
        had_movement = False
        r, c = rc_map[d]
        while True:
            success, reset, loc = next(grid, r, c, d)
            if not success:
                break
            if not reset:
                if at(grid, (r, c)) == "." and at(grid, loc) == "O":
                    swap(grid, (r, c), loc)
                    had_movement = True
            r, c = loc
    return grid


def extract_id(grid):
    id = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            id.append(grid[r][c] == "O")
    return id


def solve_2(grid):
    history = [extract_id(grid)]
    max_count = 1000000000

    i = 1
    while i <= max_count:
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            grid = tilt(grid, d)
        new_id = extract_id(grid)
        try:
            last = history.index(new_id)
            length = i - last
            rep_cap = (max_count - i) // length
            i += rep_cap * length
        except ValueError:
            pass
        history.append(new_id)
        i += 1

    p2 = 0
    for c in range(len(grid[0])):
        p2 += calc_load(grid, c)
    return p2


def solve(grid):
    p1 = 0
    for c in range(len(grid[0])):
        p1 += calc_load(grid, c, True)

    p2 = solve_2(grid)

    return p1, p2


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            lines = list(map(lambda x: list(x.strip()), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))

