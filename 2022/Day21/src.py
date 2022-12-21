def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines

nodes = {}

class Node:
    def __init__(self, line) -> None:
        line = line.strip()
        self.name = line.split(': ')[0]
        rest = line.split(': ')[1]
        self.val = None
        self.children = ()
        rest_split = rest.split()
        if len(rest_split) == 1:
            self.val = int(rest)
        else:
            self.children = (rest_split[0], rest_split[2])
            self.op = rest_split[1]

    def eval(self):
        if self.val is None:
            left, right = nodes[self.children[0]].eval(), nodes[self.children[1]].eval()
            self.val = eval(f"{str(left)} {self.op} {str(right)}")
        return self.val


def verdict(lines, guess):
    for line in lines:
        name = line.split(':')[0]
        nodes[name] = Node(line)

    nodes["humn"].val = guess
    left = nodes[nodes["root"].children[0]].eval()
    right = nodes[nodes["root"].children[1]].eval()
    if left < right:
        return -1
    if right < left:
        return 1
    return 0


def bs(variation, lines):
    l = -10000000000000000000000000000
    r = 100000000000000000000000000000
    while r - l > 1:
        mid = (r + l) // 2
        res = verdict(lines, mid)

        if res == 0:
            return mid
        elif (res > 0 and variation == 0) or (res < 0 and variation == 1):
            l = mid
        else:
            r = mid


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    for line in lines:
        name = line.split(':')[0]
        nodes[name] = Node(line)
    
    p1_ans = nodes["root"].eval()

    p2_ans = bs(0, lines)
    if p2_ans is None:
        p2_ans = bs(1, lines)

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)