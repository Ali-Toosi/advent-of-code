def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def base5(x):
    res = ""
    while x:
        res = str(x % 5) + res
        x //= 5
    return res


def snafu_add(a, b):
    signs = ["=", "-", "0", "1", "2"]
    res = ""
    carry = 0
    pos = -1
    while pos * -1 <= max(len(a), len(b)):
        local_res = carry
        if pos * -1 <= len(a):
            local_res += signs.index(a[pos]) - 2
        if pos * -1 <= len(b):
            local_res += signs.index(b[pos]) - 2
        carry = (abs(local_res) // 3) * (-1 if local_res < 0 else 1)
        res += signs[local_res - (5 * carry) + 2]
        pos -= 1
    res += signs[carry + 2]
    return "".join(reversed(res))

def snafu_sum(lines):
    res = "0"
    for line in lines:
        line = line.strip()
        temp_res = snafu_add(res, line)
        
        res = ""
        non_zero_seen = False
        for char in temp_res:
            if non_zero_seen or char != "0":
                non_zero_seen = True
                res += char
    return res


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    
    p1_ans = snafu_sum(lines)
    p2_ans = 0

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)
    print("Part 2:")
    print(p2_ans)