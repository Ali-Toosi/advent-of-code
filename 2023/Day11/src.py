def empty_cols(grid):
    res = []
    for col in range(len(grid[0])):
        empty = True
        for row in range(len(grid)):
            empty = empty and grid[row][col] == "."
        if empty:
            res.append(col)
    return res


def empty_rows(grid):
    res = []
    for i, line in enumerate(grid):
        if all([x == "." for x in line]):
            res.append(i)
    return res


def bfs(grid, x, y, expansion):
    big_rows = empty_rows(grid)
    big_cols = empty_cols(grid)

    q = [(0, x, y)]
    seen = [[False for _ in range(len(grid[0]))] for __ in range(len(grid))]
    seen[x][y] = True
    s = 0
    while len(q) > 0:
        l, r, c = q.pop(0)
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + d[0], c + d[1]
            if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]):
                continue
            if seen[nr][nc]:
                continue

            if r != nr:
                if r in big_rows:
                    step_size = expansion
                else:
                    step_size = 1
            elif c != nc:
                if c in big_cols:
                    step_size = expansion
                else:
                    step_size = 1

            q.append((l + step_size, nr, nc))
            seen[nr][nc] = True
            if grid[nr][nc] == "#":
                s += l + step_size

    return s


def solve(grid):
    p1 = p2 = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                p1 += bfs(grid, i, j, 2)
                p2 += bfs(grid, i, j, int(1e6))

    p1 //= 2
    p2 //= 2
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

