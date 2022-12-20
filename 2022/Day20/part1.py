def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class Number:
    def __init__(self, x, pos):
        self.num = x
        self.pos = pos


def swap(x, num, moves):
    if moves < 0:
        target = x[num.pos - 1]
    else:
        target = x[num.pos + 1]
    
    aux_num_pos = num.pos

    x[target.pos] = num
    num.pos = target.pos
    
    x[aux_num_pos] = target
    target.pos = aux_num_pos


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    x = []
    cc = []
    zero_ref = None
    enc_key = 1
    for i, line in enumerate(lines):
        num_object = Number(enc_key * int(line.strip()), i)
        if num_object.num == 0:
            zero_ref = num_object
        x.append(num_object)
        cc.append(num_object)
    
    for _ in range(1):
        for num in cc:
            moves = abs(num.num) % (len(x) - 1)
            if num.num < 0:
                moves = -1 * moves
            if moves + num.pos <= 0 or moves + num.pos >= len(x):
                if moves > 0:
                    moves = -1 * (len(x) - 1 - moves)
                else:
                    moves = len(x) - 1 + moves
            for i in range(abs(moves)):
                swap(x, num, moves)

    
    for dst in [1000, 2000, 3000]:
        dst += zero_ref.pos
        p1_ans += x[dst % len(x)].num


    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)