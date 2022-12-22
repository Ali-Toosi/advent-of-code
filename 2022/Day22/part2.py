def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines

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


def read_cube_lines(lines, side):
    size = 0
    while lines[size].strip() != "":
        size += 1
    size += 1
    return lines[side * size : (side + 1) * size - 1]


RIGHT = 0
BOTTOM = 1
LEFT = 2
TOP = 3


class CubeCell:
    def __init__(self, og_row, og_col, blocked, side):
        self.og_row = og_row
        self.og_col = og_col
        self.row = self.col = 0
        self.blocked = blocked
        self.top = self.bottom = self.left = self.right = None
        self.side = side


class CubeSide:
    def __init__(self, name, lines, row_offset, col_offset):
        self.grid = []
        for row, line in enumerate(lines):
            line = line.strip()
            current_row = []
            for col, char in enumerate(line):
                current_row.append(CubeCell(row + row_offset, col + col_offset, char == '#', name))
            self.grid.append(current_row)
    
    def rotate(self):
        size = len(self.grid)
        new_grid = [[None for _ in range(size)] for __ in range(size)]

        for i in range(size):
            for j in range(size):
                new_grid[j][size - 1 - i] = self.grid[i][j]
        
        self.grid = new_grid
    
    def mirror(self):
        size = len(self.grid)
        new_grid = [[None for _ in range(size)] for __ in range(size)]

        for i in range(size):
            for j in range(size):
                new_grid[i][size - 1 - j] = self.grid[i][j]
        
        self.grid = new_grid


def move(cell, inst, d, real_d):
    if inst == "L":
        return cell, (d + 3) % 4, (real_d + 3) % 4
    if inst == "R":
        return cell, (d + 1) % 4, (real_d + 1) % 4
    
    d_map = {
        TOP: "top",
        BOTTOM: "bottom",
        LEFT: "left",
        RIGHT: "right",
    }

    for _ in range(inst):
        new_cell, new_d = getattr(cell, d_map[d])
        if new_cell.blocked:
            break
        cell = new_cell
        d = new_d
    
    return cell, d, real_d


for file_name in ["input_p2.txt"]:
    lines = read_input(file_name)
    p2_ans = 0

    instructions = read_instructions(lines)
    
    offsets = {
        "input_p2.txt": [
            (0, 50),    # top
            (50, 50),   # face
            (0, 100),   # right
            (150, 0),   # back
            (100, 0),   # left
            (100, 50),  # bottom
        ],
        "sample_p2.txt": [
            (0, 8),
            (4, 8),
            (8, 12),
            (4, 0),
            (4, 4),
            (8, 4)
        ]
    }

    top = CubeSide("top", read_cube_lines(lines, 0), *offsets[file_name][0])
    face = CubeSide("face", read_cube_lines(lines, 1), *offsets[file_name][1])
    right = CubeSide("right", read_cube_lines(lines, 2), *offsets[file_name][2])
    back = CubeSide("back", read_cube_lines(lines, 3), *offsets[file_name][3])
    left = CubeSide("left", read_cube_lines(lines, 4), *offsets[file_name][4])
    bottom = CubeSide("bottom", read_cube_lines(lines, 5), *offsets[file_name][5])

    size = len(top.grid)

    for i in range(size):
        # ============== FACE ================
        face.grid[0][i].top = (top.grid[-1][i], TOP)
        top.grid[-1][i].bottom = (face.grid[0][i], BOTTOM)

        face.grid[i][0].left = (left.grid[0][i], BOTTOM)
        left.grid[0][i].top = (face.grid[i][0], RIGHT)

        face.grid[-1][i].bottom = (bottom.grid[0][i], BOTTOM)
        bottom.grid[0][i].top = (face.grid[-1][i], TOP)

        face.grid[i][-1].right = (right.grid[-1][i], TOP)
        right.grid[-1][i].bottom = (face.grid[i][-1], LEFT)

        # ============== BACK ================
        back.grid[-1][i].bottom = (right.grid[0][i], BOTTOM)
        right.grid[0][i].top = (back.grid[-1][i], TOP)

        back.grid[0][i].top = (left.grid[-1][i], TOP)
        left.grid[-1][i].bottom = (back.grid[0][i], BOTTOM)

        back.grid[i][0].left = (top.grid[0][i], BOTTOM)
        top.grid[0][i].top = (back.grid[i][0], RIGHT)

        back.grid[i][-1].right = (bottom.grid[-1][i], TOP)
        bottom.grid[-1][i].bottom = (back.grid[i][-1], LEFT)

        # ============== TOP ================
        top.grid[i][0].left = (left.grid[size - 1 - i][0], RIGHT)
        left.grid[size - 1 - i][0].left = (top.grid[i][0], RIGHT)

        top.grid[i][-1].right = (right.grid[i][0], RIGHT)
        right.grid[i][0].left = (top.grid[i][-1], LEFT)

        # ============== BOTTOM ================
        bottom.grid[i][0].left = (left.grid[i][-1], LEFT)
        left.grid[i][-1].right = (bottom.grid[i][0], RIGHT)

        bottom.grid[i][-1].right = (right.grid[size - 1 - i][-1], LEFT)
        right.grid[size - 1 - i][-1].right = (bottom.grid[i][-1], LEFT)

        for j in range(size):
            for x in [top, right, left, back, bottom, face]:
                x.grid[i][j].row = i
                x.grid[i][j].col = j

                if i > 0:
                    x.grid[i][j].top = (x.grid[i - 1][j], TOP)
                if i < size - 1:
                    x.grid[i][j].bottom = (x.grid[i + 1][j], BOTTOM)
                if j > 0:
                    x.grid[i][j].left = (x.grid[i][j - 1], LEFT)
                if j < size - 1:
                    x.grid[i][j].right = (x.grid[i][j + 1], RIGHT)
        
    cell = top.grid[0][0]
    d = real_d = RIGHT
    for ins in instructions:
        cell, d, real_d = move(cell, ins, d, real_d)

    p2_ans = (cell.og_row + 1) * 1000 + (cell.og_col + 1) * 4 + d

    print("=================")
    print("-> Input", file_name)
    print("Part 2:")
    print(p2_ans)