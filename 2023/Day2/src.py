def solve(lines):
    maxes = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    part1 = part2 = 0
    for i, line in enumerate(lines):
        needed = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        data = line.split(": ")[1]
        sets = data.split(";")
        possible = True
        for s in sets:
            s = s.strip()
            cubes = s.split(", ")
            for cube in cubes:
                cnt, col = cube.split()
                cnt = int(cnt)
                if cnt > maxes[col]:
                    possible = False
                needed[col] = max(needed[col], cnt)
        if possible:
            part1 += i + 1
        part2 += needed["red"] * needed["blue"] * needed["green"]

    return part1, part2


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["input.txt", "sample1.txt", "sample2.txt"]:
        try:
            lines = read_input(file_name)
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))

