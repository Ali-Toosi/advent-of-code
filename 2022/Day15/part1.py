def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class Rec:
    def __init__(self, sens_r, sens_c, be_r, be_c) -> None:
        dist = abs(sens_r - be_r) + abs(sens_c - be_c)
        self.top = sens_r - dist
        self.bottom = sens_r + dist
        self.left = sens_c - dist
        self.right = sens_c + dist

    def row_segment(self, row):
        mid = (self.top + self.bottom) // 2
        diff = abs(mid - row)
        return (self.left + diff, self.right - diff)


def beacons_at_row(beacs, row):
    cnt = 0
    for beac in beacs:
        if beac[0] == row:
            cnt += 1
    return cnt


def sens_at_row(sens, row):
    cnt = 0
    for sen in sens:
        if sen[0] == row:
            cnt += 1
    return cnt


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    recs = []
    beacs = set()
    sens = set()

    for line in lines:
        parts = line.strip().split()
        sens_c = int(parts[2][2:-1])
        sens_r = int(parts[3][2:-1])
        be_c = int(parts[8][2:-1])
        be_r = int(parts[9][2:])
        recs.append(Rec(sens_r, sens_c, be_r, be_c))
        beacs.add((be_r, be_c))
        sens.add((sens_r, sens_c))
    
    wanted_row = 2_000_000
    # wanted_row = 10
    captured_segments = []
    for i, rec in enumerate(recs):
        if rec.bottom >= wanted_row >= rec.top:
            captured_segments.append(rec.row_segment(wanted_row))
    
    captured_segments.sort()

    p1 = 0

    while p1 < len(captured_segments):
        current_end = captured_segments[p1][1]
        p2 = p1 + 1
        while p2 < len(captured_segments) and captured_segments[p2][0] <= current_end:
            current_end = max(current_end, captured_segments[p2][1])
            p2 += 1

        p1_ans += current_end - captured_segments[p1][0] + 1
        p1 = p2

    p1_ans -= beacons_at_row(beacs, wanted_row) + sens_at_row(sens, wanted_row)

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)