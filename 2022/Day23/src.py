from collections import defaultdict


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class World:
    def __init__(self) -> None:
        self.turns = [0, 2, 3, 1]
        self.dr = [-1, 0, 1, 0]
        self.dc = [0, 1, 0, -1]
        self.d2r = [
            (0, 0, 0),
            (-1, 0, 1),
            (0, 0, 0),
            (-1, 0, 1)
        ]
        self.d2c = [
            (-1, 0, 1),
            (0, 0, 0),
            (-1, 0, 1),
            (0, 0, 0)
        ]
        self.grid = defaultdict(lambda: defaultdict(lambda: None))
        self.elves = []
        self.fixed = False
    
    def rotate_turns(self):
        self.turns = self.turns[1:] + [self.turns[0]]
    
    def get_edges(self):
        min_row = min([elf.row for elf in self.elves])
        max_row = max([elf.row for elf in self.elves])
        min_col = min([elf.col for elf in self.elves])
        max_col = max([elf.col for elf in self.elves])

        return min_row, max_row, min_col, max_col


class Elf:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.pr_row = None
        self.pr_col = None
        self.dirty = False
    
    def propose(self, world):
        found = False
        cnt = 0
        for turn in world.turns:
            center_r, center_c = self.row + world.dr[turn], self.col + world.dc[turn]
            empty = True
            for i in range(3):
                empty &= not world.grid[center_r + world.d2r[turn][i]][center_c + world.d2c[turn][i]]
            
            if empty:
                cnt += 1
                if not found:
                    found = True
                    self.pr_row = center_r
                    self.pr_col = center_c
        
        if not found or cnt == 4:
            self.pr_col = self.pr_row = None
    
    def clean(self):
        if self.dirty:
            self.row = self.pr_row
            self.col = self.pr_col
            self.pr_row = self.pr_col = None
            self.dirty = False
        

def create_world(lines):
    world = World()

    for i, line in enumerate(lines):
        line = line.strip()
        for j, char in enumerate(line):
            if char == '#':
                elf = Elf(i, j)
                world.elves.append(elf)
                world.grid[i][j] = elf
    
    return world

        
def play_round(world):
    one_elf_moved = False
    spots = defaultdict(lambda: 0)
    for elf in world.elves:
        elf.propose(world)
        if elf.pr_row is not None:
            spots[(elf.pr_row, elf.pr_col)] += 1
    
    new_grid = defaultdict(lambda: defaultdict(lambda: None))
    for elf in world.elves:
        if elf.pr_row is not None and spots[(elf.pr_row, elf.pr_col)] == 1:
            one_elf_moved = True
            new_grid[elf.pr_row][elf.pr_col] = elf
            elf.dirty = True
        else:
            new_grid[elf.row][elf.col] = elf
            elf.pr_row = elf.pr_col = None
    
    for elf in world.elves:
        elf.clean()
    world.rotate_turns()
    world.fixed = not one_elf_moved
    world.grid = new_grid
    

def print_world(world):
    min_row, max_row, min_col, max_col = world.get_edges()

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if world.grid[row][col]:
                print('#', end='')
            else:
                print('.', end='')
        print()


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    world = create_world(lines)
    # print_world(world)
    round = 0
    while True:
        play_round(world)
        round += 1
        if round == 10:
            min_row, max_row, min_col, max_col = world.get_edges()
            p1_ans = (max_row - min_row + 1) * (max_col - min_col + 1) - len(world.elves)
        if world.fixed:
            p2_ans = round
            break

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)