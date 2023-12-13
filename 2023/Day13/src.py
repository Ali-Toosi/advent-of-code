def try_c_mirror(grid, index):
    length = min(index + 1, len(grid[0]) - index - 1)
    errors = 0
    for line in grid:
        left = line[index - length + 1:index + 1]
        right = "".join(reversed(line[index + 1:index + 1 + length]))
        errors += len([x for x in range(length) if left[x] != right[x]])
    return errors


def try_r_mirror(grid, index):
    length = min(index + 1, len(grid) - index - 1)
    errors = 0
    for i in range(length):
        top = grid[index - i]
        bottom = grid[index + 1 + i]
        errors += len([x for x in range(len(top)) if top[x] != bottom[x]])
    return errors


def solve_pattern(grid):
    p1 = p2 = 0
    for i in range(len(grid[0]) - 1):
        errors = try_c_mirror(grid, i)
        if errors == 0:
            p1 += i + 1
        elif errors == 1:
            p2 += i + 1
    for i in range(len(grid) - 1):
        errors = try_r_mirror(grid, i)
        if errors == 0:
            p1 += (i + 1) * 100
        elif errors == 1:
            p2 += (i + 1) * 100
    return p1, p2


def solve(lines):
    p1 = p2 = 0

    while len(lines) > 0:
        try:
            end = lines.index("")
        except ValueError:
            end = len(lines)
        a, b = solve_pattern(lines[:end])
        p1 += a
        p2 += b
        lines = lines[end + 1:]

    return p1, p2


def take_out_sequence(line, *args):
    res = []
    rest = line
    for arg in args:
        cur, rest = rest.split(arg, 1)
        res.append(cur)
    return res + [rest]


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            lines = list(map(lambda x: x.strip(), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))

