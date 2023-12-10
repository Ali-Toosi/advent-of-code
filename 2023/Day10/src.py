def follow(grid, r, c):
    dmap = {
        "L": [(-1, 0), (0, 1)],
        "7": [(0, -1), (1, 0)],
        "F": [(1, 0), (0, 1)],
        "J": [(0, -1), (-1, 0)],
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
    }
    dr, dc = r, c
    steps = 0
    prev = None
    cells = [(r, c)]
    while True:
        ds = dmap[grid[r][c]]
        for d in ds:
            nr, nc = r + d[0], c + d[1]
            if prev == (nr, nc):
                continue
            if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]) or grid[nr][nc] == ".":
                return False, steps, []
            if nr == dr and nc == dc:
                return True, steps, cells
            prev = (r, c)
            steps += 1
            r, c = nr, nc
            cells.append((r, c))
            break


def count_line(line: str):
    cnt = 0
    b = False
    for i in range(len(line)):
        if line[i] == "." and b:
            cnt += 1
            # print("I", end="")
        # else:
            # print(line[i], end="")
        if line[i] == "&":
            b = not b

    # print()
    return cnt


def solve(grid):
    r, c = None, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                r, c = i, j
                break

    p1 = cells = None
    for candidate in ["F", "J", "L", "|", "-", "7"]:
        grid[r] = grid[r][:c] + candidate + grid[r][c + 1:]
        a, x, y = follow(grid, r, c)
        if a:
            p1 = (x // 2) + 1
            cells = y
            break

    print("S is", grid[r][c])

    for r, c in cells:
        if grid[r][c] in ["|", "F", "7"]:
            grid[r] = grid[r][:c] + "&" + grid[r][c + 1:]
        # elif grid[r][c] == "-":
        #     grid[r] = grid[r][:c] + "$" + grid[r][c + 1:]
        else:
            grid[r] = grid[r][:c] + "*" + grid[r][c + 1:]

    new_grid = []
    for line in grid:
        for pipe in ["F", "J", "L", "|", "-", "7"]:
            line = line.replace(pipe, ".")
        new_grid.append(line)
        # print(line)

    # print("-----------------------")
    p2 = sum([count_line(line) for line in new_grid])
    return p1, p2


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "sample3.txt", "sample4.txt", "sample5.txt", "input.txt"]:
        try:
            lines = list(map(lambda x: x.strip(), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))

