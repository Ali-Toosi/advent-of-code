d_map = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0)
}


def extract_points(instructions):
    points = [(0, 0)]
    real_points_cnt = 0
    for i in instructions:
        new_r, new_c = points[-1][0] + d_map[i[0]][0] * i[1], points[-1][1] + d_map[i[0]][1] * i[1]
        real_points_cnt += i[1]
        points.append((new_r, new_c))

    return points, real_points_cnt


def find_area(points):
    res = 0
    for i in range(len(points)):
        res += (points[i][1] - points[(i + 1) % len(points)][1]) * (points[i][0] + points[(i + 1) % len(points)][0])
    return abs(res) // 2


def solve_instructions(instructions):
    points, cnt = extract_points(instructions)
    area = find_area(points)
    return area + (cnt - 4) // 2 + 3


def solve(lines):
    p1_instructions = [
        take_out_sequence(line, " ", " (#")
        for line in lines
    ]
    p2_instructions = []
    for i in p1_instructions:
        i[1] = int(i[1])
        i[2] = i[2][:-1]
        p2_instructions.append([
            ["R", "D", "L", "U"][int(i[2][-1])],
            int(i[2][:-1], 16)
        ])

    p1 = solve_instructions(p1_instructions)
    p2 = solve_instructions(p2_instructions)

    return p1, p2


def take_out_sequence(line, *args):
    res = []
    rest = line
    for arg in args:
        cur, rest = rest.split(arg, 1)
        res.append(cur)
    return res + [rest]


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            _lines = list(map(lambda x: x.strip(), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(_lines))

