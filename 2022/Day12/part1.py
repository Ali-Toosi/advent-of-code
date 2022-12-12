def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    height = []
    src_r = src_c = dst_r = dst_c = 0

    row = 0
    col = 0

    for line in lines:
        line = line.strip()
        col = 0
        height.append([])
        for cell in line:
            if cell == 'S':
                src_r = row
                src_c = col
                cell = 'a'
            elif cell == 'E':
                dst_r = row
                dst_c = col
                cell = 'z'

            height[-1].append(ord(cell) - ord('a'))
            col += 1        
        row += 1
    
    marked = []
    queue = [(src_r, src_c, 0)]
    while len(queue) > 0:
        x, y, l = queue[0]
        del queue[0]

        if x == dst_r and y == dst_c:
            p1_ans = l
            break

        marked.append((x, y))

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for i in range(4):
            new_x = x + dx[i]
            new_y = y + dy[i]
            if new_x < 0 or new_y < 0 or new_x >= len(height) or new_y >= len(height[0]):
                continue

            if height[new_x][new_y] - height[x][y] <= 1 and (new_x, new_y) not in marked:
                marked.append((new_x, new_y))
                queue.append((new_x, new_y, l + 1))

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)