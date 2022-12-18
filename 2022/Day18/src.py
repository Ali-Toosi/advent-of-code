from collections import defaultdict


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines

MAX = 50

class Cube:
    def __init__(self, line):
        line = line.strip()
        self.row, self.col, self.level = map(int, line.split(','))
    
    def get_adjacents(self):
        res = []
        res.append((self.row, self.col + 1, self.level))
        res.append((self.row, self.col - 1, self.level))
        res.append((self.row + 1, self.col, self.level))
        res.append((self.row - 1, self.col, self.level))
        res.append((self.row, self.col, self.level - 1))
        res.append((self.row, self.col, self.level + 1))
        return res

    def equals(self, cords):
        return (self.row, self.col, self.level) == cords


def get_outer_surface(cubes):
    res = 0
    for cube in cubes:
        adjs = cube.get_adjacents()
        sides = 6
        for adj in adjs:
            for candidate in cubes:
                if candidate.equals(adj):
                    sides -= 1
                    break
        res += sides
    return res


def bfs(grid, checked, row, col, level):
    queue = [(row, col, level)]
    res = [(row, col, level)]
    checked[row][col][level] = True
    failed = False

    while len(queue) > 0:
        x, y, z = queue[0]
        del queue[0]

        dx = [-1, 1, 0, 0, 0, 0]
        dy = [0, 0, 1, -1, 0, 0]
        dz = [0, 0, 0, 0, 1, -1]

        for i in range(6):
            nx, ny, nz = x + dx[i], y + dy[i], z + dz[i]
            if any([cord < 0 or cord >= MAX for cord in [nx, ny, nz]]):
                failed = True
                continue
            if not checked[nx][ny][nz] and not grid[nx][ny][nz]:
                checked[nx][ny][nz] = True
                res.append((nx, ny, nz))
                queue.append((nx, ny, nz))
    
    return res if not failed else []


def get_trapped_surface(cubes):
    grid = [[[False for _ in range(MAX)] for __ in range(MAX)] for ___ in range(MAX)]

    for cube in cubes:
        grid[cube.row][cube.col][cube.level] = True
    
    trapped_surface = 0
    checked = [[[False for _ in range(MAX)] for __ in range(MAX)] for ___ in range(MAX)]
    for row in range(MAX):
        for col in range(MAX):
            for level in range(MAX):
                if not checked[row][col][level] and not grid[row][col][level]:
                    trapped_cubes = [Cube(f"{x[0]},{x[1]},{x[2]}") for x in bfs(grid, checked, row, col, level)]
                    trapped_surface += get_outer_surface(trapped_cubes)
    
    return trapped_surface


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    cubes = []
    for line in lines:
        cubes.append(Cube(line))
    
    p1_ans = get_outer_surface(cubes)
    p2_ans = p1_ans - get_trapped_surface(cubes)
    
    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)