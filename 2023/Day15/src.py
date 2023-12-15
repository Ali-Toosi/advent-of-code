def mhash(x):
    res = 0
    for c in x:
        res += ord(c)
        res *= 17
        res %= 256
    return res


def add(boxes, box, lens, num):
    for l in boxes[box]:
        if l[0] == lens:
            l[1] = num
            return

    boxes[box].append([lens, num])


def rem(boxes, box, lens):
    for i, l in enumerate(boxes[box]):
        if l[0] == lens:
            boxes[box].pop(i)
            return


def act(boxes, label):
    if "=" in label:
        b, n = list(label.split("="))
        lens = b
        box = mhash(lens)
        num = int(n)
        add(boxes, box, lens, num)
    else:
        lens = label[:-1]
        box = mhash(lens)
        rem(boxes, box, lens)


def solve(lines):
    labels = lines[0].split(",")
    p1 = sum([mhash(part) for part in labels])

    boxes = [[] for _ in range(256)]
    for label in labels:
        act(boxes, label)

    p2 = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            p2 += (i + 1) * (j + 1) * lens[1]

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

