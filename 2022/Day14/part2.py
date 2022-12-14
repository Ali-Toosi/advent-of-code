def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def send_sand(grid, low):
    x, y = 0, 500
    if grid[x][y] == 'o':
        return True
    while True:
        if grid[x + 1][y] == '.':
            x += 1
            continue
        if y > 0 and grid[x+1][y-1] == '.':
            x += 1
            y -= 1
            continue
        if grid[x+1][y+1] == '.':
            x += 1
            y += 1
            continue
        grid[x][y] = 'o'
        return False


def draw_line(grid, p):
    lowest_x = -1
    for i in range(1, len(p)):
        fix_x = p[i-1][0] == p[i][0]
        fix_y = p[i-1][1] == p[i][1]

        src_x = min(p[i-1][0], p[i][0])
        dst_x = max(p[i-1][0], p[i][0])

        src_y = min(p[i-1][1], p[i][1])
        dst_y = max(p[i-1][1], p[i][1])

        for x in range(src_x, dst_x + 1):
            for y in range(src_y, dst_y + 1):
                if (fix_x and x == p[i-1][0]) or (fix_y and y == p[i-1][1]):
                    grid[x][y] = '#'
                    
                    if x > lowest_x:
                        lowest_x = x
    return lowest_x


def print_grid(grid, rb, re, cb, ce):
    for r in range(rb, re + 1):
        for c in range(cb, ce + 1):
            print(grid[r][c], end="")
        print()


MAX_COL = 5000

for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p2_ans = 0

    grid = [['.' for _ in range(MAX_COL)] for __ in range(5000)]

    lowest_x = -1

    for line in lines:
        points = line.split('->')
        p = []
        for point in points:
            p.append((int(point.split(',')[1].strip()), int(point.split(',')[0].strip())))

        low_x = draw_line(grid, p)
        if low_x > lowest_x:
            lowest_x = low_x

    draw_line(grid, [(lowest_x + 2, 0), (lowest_x + 2, MAX_COL - 1)])

    cnt = 0
    while True:
        res = send_sand(grid, lowest_x)
        if res:
            p2_ans = cnt
            break
        cnt += 1

    print("=================")
    print("-> Input", file_name)
    print("Part 2:")
    print(p2_ans)