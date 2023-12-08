from math import gcd

def solve1(lines):
    p1 = p2 = 0

    grid = {}

    cmds = lines[0].strip()
    for line in lines[2:]:
        src, rest = line.split(" = ")
        left, rest = rest.split(",")
        left = left[1:]
        right = rest.strip()[:-1]
        grid[src] = (left, right)

    current = "AAA"
    while current != "ZZZ":
        cmd = 0 if cmds[p1 % len(cmds)] == "L" else 1
        current = grid[current][cmd]
        p1 += 1

    return p1


def lcm(l):
    ans = 1
    for i in l:
        ans = (ans * i) // gcd(ans, i)
    return ans


def solve2(lines):
    grid = {}

    cmds = lines[0].strip()
    starts = []
    for line in lines[2:]:
        src, rest = line.split(" = ")
        left, rest = rest.split(",")
        left = left[1:]
        right = rest.strip()[:-1]
        grid[src] = (left, right)
        if src[-1] == "A":
            starts.append(src)

    per_src = []
    for start in starts:
        steps = 0
        current = start
        while current[-1] != "Z":
            cmd = 0 if cmds[steps % len(cmds)] == "L" else 1
            current = grid[current][cmd]
            steps += 1
        per_src.append(steps)

    return lcm(per_src)


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
        print(solve1(lines))
        print(solve2(lines))

