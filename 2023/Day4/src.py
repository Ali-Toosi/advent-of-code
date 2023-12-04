def p1(lines):
    part1 = 0

    for card in lines:
        while "  " in card:
            card = card.replace("  ", " ")
        numbers = card.split(":")[1].strip()
        winning, have = list(map(lambda x: x.strip(), numbers.split("|")))
        winning = list(map(int, winning.split()))
        have = list(map(int, have.split()))
        points = 0
        for num in have:
            if num in winning:
                if points == 0:
                    points = 1
                else:
                    points *= 2
        part1 += points

    return part1


def p2(lines):
    cards = [(i, lines[i].strip()) for i in range(len(lines))]

    i = 0
    while i < len(cards):
        card_no, card = cards[i]
        i += 1
        while "  " in card:
            card = card.replace("  ", " ")
        numbers = card.split(":")[1].strip()
        winning, have = list(map(lambda x: x.strip(), numbers.split("|")))
        winning = list(map(int, winning.split()))
        have = list(map(int, have.split()))
        cnt = 0
        for num in have:
            if num in winning:
                cnt += 1
        for j in range(card_no + 1, card_no + cnt + 1):
            cards.append((j, lines[j].strip()))

    return len(cards)


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
        print(p1(lines), p2(lines))

