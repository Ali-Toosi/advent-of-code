def next_level(line):
    res = []
    for i in range(1, len(line)):
        res.append(line[i] - line[i - 1])

    return res


def full_history_ends(line, end):
    hist = [line]
    while not all([x == 0 for x in hist[-1]]):
        hist.append(next_level(hist[-1]))

    res = []
    for h in hist:
        res.append(h[end])

    return res


def predict(line):
    ends = full_history_ends(line, -1)
    return sum(ends)


def predict_2(line):
    ends = full_history_ends(line, 0)
    below = 0
    for end in reversed(ends):
        below = end - below

    return below


def solve(lines):
    p1 = p2 = 0

    for line in lines:
        x = list(map(int, line.split()))
        p1 += predict(x)
        p2 += predict_2(x)

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

