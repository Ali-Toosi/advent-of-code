def bfs(grid, r, c, goal):
    if goal < 0:
        return 0
    reachable = {0: 1}
    q = [(0, r, c)]
    seen = [[False for _ in range(len(grid[0]))] for __ in range(len(grid))]
    seen[r][c] = True
    while len(q) > 0:
        l, r, c = q.pop(0)
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + d[0], c + d[1]
            if not (len(grid) > nr >= 0 and len(grid[0]) > nc >= 0):
                continue
            if grid[nr][nc] == "#" or seen[nr][nc]:
                continue
            try:
                reachable[l + 1] += 1
            except KeyError:
                reachable[l + 1] = 1
            q.append((l + 1, nr, nc))
            seen[nr][nc] = True

    res = 0
    for i in range(0, goal + 1, 2):
        res += reachable.get(goal - i, 0)
    return res


def difs(seq):
    res = []
    for i in range(1, len(seq)):
        res.append(seq[i] - seq[i - 1])
    return res


def expand_grid(grid, cnt):
    res = []
    for i in range(cnt * len(grid)):
        res.append([])
        for j in range(cnt * len(grid)):
            res[-1].append(grid[i % len(grid)][j % len(grid)])

    return res


def find_s(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return i, j


def solve(grid, file_name):
    sr, sc = find_s(grid)

    assert file_name != "input.txt" or all(grid[sr][i] != "#" and grid[i][sc] != "#" for i in range(len(grid)))

    p1 = bfs(grid, sr, sc, 64)

    max_dist = 26501365
    og_len = len(grid)
    grid = expand_grid(grid, 9)
    sr, sc = len(grid) // 2, len(grid) // 2

    p2s = []
    if file_name == "input.txt":
        for _max_dist in range(og_len // 2, max_dist, og_len):
            if len(p2s) > 3:
                break
            p2s.append(bfs(grid, sr, sc, _max_dist))

        dif_levels = [p2s]
        while 0 not in dif_levels[-1]:
            dif_levels.append(difs(dif_levels[-1]))
            print(dif_levels[-1])

        needed = (max_dist - og_len // 2) // og_len
        x = dif_levels[0][0]
        y = dif_levels[1][0]
        z = dif_levels[2][0]

        p2 = x + needed * y + z * (needed * (needed-1)) // 2
    else:
        p2 = 0

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
            _lines = list(map(lambda x: list(x.strip()), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(_lines, file_name))

