from functools import partial, cmp_to_key


def get_type(hand):
    hand = "".join(sorted(hand))
    cnts = [1]
    for i in range(1, 5):
        if hand[i] == hand[i-1]:
            cnts[-1] += 1
        else:
            cnts.append(1)

    cmps = [[5], [1, 4], [2, 3], [1, 1, 3], [1, 2, 2], [1, 1, 1, 2], [1, 1, 1, 1, 1]]
    return cmps.index(sorted(cnts))

types_cache = dict()


def get_type_2(hand):
    letters = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if hand in types_cache:
        return types_cache[hand]

    if "J" not in hand:
        types_cache[hand] = get_type(hand)
        return types_cache[hand]

    possibilities = [hand]
    for i in range(5):
        if hand[i] != "J":
            continue
        new_poss = []
        for poss in possibilities:
            for l in letters:
                new_poss.append(poss[:i] + l + poss[i + 1:])
        possibilities = new_poss

    lowest = 10
    for poss in possibilities:
        if get_type(poss) < lowest:
            lowest = get_type(poss)
    types_cache[hand] = lowest
    return lowest


def cmp(get_type_func, a, b):
    if get_type_func == get_type_2:
        STRENGTHS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    else:
        STRENGTHS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    a = a[0]
    b = b[0]
    t_a, t_b = get_type_func(a), get_type_func(b)
    if t_a == t_b:
        for i in range(5):
            if a[i] != b[i]:
                return -1 if STRENGTHS.index(a[i]) < STRENGTHS.index(b[i]) else 1
        return 0
    return -1 if t_a < t_b else 1


def solve(lines):
    p1 = p2 = 0

    hands = [line.strip().split() for line in lines]
    hands = list(reversed(sorted(hands, key=cmp_to_key(partial(cmp, get_type)))))
    for i, hand in enumerate(hands):
        p1 += int(hand[1]) * (i + 1)

    hands = list(reversed(sorted(hands, key=cmp_to_key(partial(cmp, get_type_2)))))
    for i, hand in enumerate(hands):
        p2 += int(hand[1]) * (i + 1)

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

