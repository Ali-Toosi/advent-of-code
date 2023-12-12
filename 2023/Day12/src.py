def expand(line, pattern, cnt):
    rline = []
    rp = []
    for i in range(cnt):
        rline.extend(line)
        if i != cnt - 1:
            rline.append("?")
        rp.extend(pattern)
    return rline, rp


def solve_line(line, pattern, expansion):
    line, pattern = expand(line, pattern, expansion)
    dp = []
    for i, num in enumerate(pattern):
        dp.append([])
        for loc in range(len(line)):
            dp[-1].append(0)
            seq_start = loc - num + 1
            if line[loc] == "." or seq_start < 0:
                continue
            else:
                if any([x == "." for x in line[seq_start:loc + 1]]):
                    continue
                elif loc + 1 < len(line) and line[loc + 1] == "#":
                    continue
                else:
                    if i == 0:
                        dp[i][loc] = 1 if all([x != "#" for x in line[:seq_start]]) else 0
                    else:
                        res = 0
                        for prev_end in range(seq_start - 1):
                            if all([x != '#' for x in line[prev_end + 1:seq_start]]):
                                res += dp[i - 1][prev_end]
                        dp[i][loc] = res

    res = 0
    start = len(line) - 1

    while start >= 0:
        if line[start] == "#":
            res += dp[len(pattern) - 1][start]
            break
        elif line[start] == "?":
            res += dp[len(pattern) - 1][start]
        start -= 1

    return res


def solve(lines):
    p1 = p2 = 0
    for line in lines:
        l, nums = line.split()
        nums = list(map(int, nums.split(",")))
        p1 += solve_line(list(l), nums, 1)
        p2 += solve_line(list(l), nums, 5)

    return p1, p2


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

