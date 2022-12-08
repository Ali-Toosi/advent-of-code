def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines

for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)

    grid = []
    for line in lines:
        grid.append(list(map(int, line.strip())))

    ans_p1 = 0
    ans_p2 = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):

            dx = [1, 0, -1, 0]
            dy = [0, 1, 0, -1]

            tree_score = 1
            tree_counted = False

            for di in range(4):
                visible = True
                height = grid[row][col]
                nr = row + dx[di]
                nc = col + dy[di]
                local_score = 0
                
                while nr < len(grid) and nc < len(grid[0]) and nr >= 0 and nc >= 0:
                    local_score += 1
                    if grid[nr][nc] >= height:
                        visible = False
                        break
                    nr += dx[di]
                    nc += dy[di]
                
                tree_score *= local_score
            
                if visible and not tree_counted:
                    ans_p1 += 1
                    tree_counted = True

            if tree_score > ans_p2:
                ans_p2 = tree_score


    print(ans_p1, ans_p2)




