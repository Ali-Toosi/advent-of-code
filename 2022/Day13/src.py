import json
from functools import cmp_to_key


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def cmp(l, r):
    
    if isinstance(l, int) and isinstance(r, int):
        return l <= r
    
    if isinstance(l, int):
        return cmp([l], r)
    
    if isinstance(r, int):
        return cmp(l, [r])
    
    for i in range(min(len(l), len(r))):
        if l[i] == r[i]:
            continue
        
        return cmp(l[i], r[i])
    
    return len(l) <= len(r)



for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    packets = []

    for i in range(0, len(lines), 3):
        l = json.loads(lines[i].strip())
        r = json.loads(lines[i + 1].strip())
        p1_ans += (i // 3) + 1 if cmp(l, r) else 0

        packets.extend([l, r])
    
    packets.extend([[[2]], [[6]]])
    packets = sorted(packets, key=cmp_to_key(lambda x, y: -1 if cmp(x, y) else 1))
    indices = packets.index([[2]]), packets.index([[6]])
    p2_ans = (indices[0] + 1) * (indices[1] + 1)

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)