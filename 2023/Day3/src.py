class Number:
    def __init__(self, starting_val=0):
        self.num = starting_val
        self.part = False

    def add_digit(self, digit):
        self.num = self.num * 10 + digit

def solve(lines):
    part1 = part2 = 0
    grid = []
    for line in lines:
        grid.append([])
        for i, c in enumerate(line):
            c = str(c)
            if c.isnumeric():
                if i == 0 or not isinstance(grid[-1][i - 1], Number):
                    grid[-1].append(Number(int(c)))
                else:
                    grid[-1][i - 1].add_digit(int(c))
                    grid[-1].append(grid[-1][i - 1])
            else:
                grid[-1].append(c)

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != '.' and not lines[i][j].isnumeric():
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        try:
                            if isinstance(grid[i + dx][j + dy], Number):
                                grid[i + dx][j + dy].part = True
                        except IndexError:
                            pass

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == '*':
                parts = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        try:
                            if isinstance(grid[i + dx][j + dy], Number) and grid[i + dx][j + dy].part:
                                parts.append(grid[i + dx][j + dy])
                        except IndexError:
                            pass
                parts = list(set(parts))
                if len(parts) == 2:
                    part2 += parts[0].num * parts[1].num

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if isinstance(grid[i][j], Number) and grid[i][j].part:
                part1 += grid[i][j].num
                grid[i][j].part = False

    return part1, part2


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

