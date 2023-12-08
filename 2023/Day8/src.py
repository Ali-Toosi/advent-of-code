from math import gcd


def lcm(l):
    ans = 1
    for i in l:
        ans = (ans * i) // gcd(ans, i)
    return ans


def needed_steps(start, cmds, grid, condition):
    steps = 0
    current = start
    while not condition(current):
        cmd = 0 if cmds[steps % len(cmds)] == "L" else 1
        current = grid[current][cmd]
        steps += 1
    return steps


def solve(lines):
    grid = {}
    cmds = lines[0].strip()
    all_starts = []

    for line in lines[2:]:
        src, rest = line.split(" = ")
        left, rest = rest.split(",")
        left = left[1:]
        right = rest.strip()[:-1]
        grid[src] = (left, right)
        if src[-1] == "A":
            all_starts.append(src)

    return (
        needed_steps("AAA", cmds, grid, lambda x: x == "ZZZ"),  # Part 1
        lcm([
            needed_steps(start, cmds, grid, lambda x: x[-1] == "Z")
            for start in all_starts
        ])                                                           # Part 2
    )


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

