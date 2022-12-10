def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    parts = []

    signals = []
    x = 1

    for line in lines:
        line = line.strip()
        if line == "noop":
            signals.append(x)
        else:
            val = int(line.split()[1])
            signals.extend([x, x])
            x += val
    
    while len(signals) < 240:
        signals.append(x)
    
    p1_ans = 0
    for i in [20, 60, 100, 140, 180, 220]:
        p1_ans += signals[i - 1] * i

    crt = ""
    for i in range(240):
        loc = signals[i] + (i // 40) * 40
        if loc - 1 <= i <= loc + 1:
            crt += '#'
        else:
            crt += '.'
    
    p2_ans = ""
    for i, char in enumerate(crt):
        if i % 40 == 0 and i != 0:
            p2_ans += '\n'
        p2_ans += char


    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)
