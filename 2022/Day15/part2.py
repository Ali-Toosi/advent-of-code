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


def segment_hole(segments, row, beacs, sens):
    max_col = 4_000_000
    potential_hole = []

    p1 = 0

    while p1 < len(segments):
        current_end = segments[p1][1]
        p2 = p1 + 1
        while p2 < len(segments) and segments[p2][0] <= current_end:
            current_end = max(current_end, segments[p2][1])
            p2 += 1

        if current_end > max_col:
            break

        if p2 < len(segments):
            potential_hole.append((current_end + 1, min(max_col, segments[p2][0] - 1)))
        
        p1 = p2
    
    for l, r in potential_hole:
        for col in range(l, r + 1):
            if (row, col) not in beacs and (row, col) not in sens:
                return row, col


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p2_ans = 0

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
    
    for row in range(4_000_001):
        captured_segments = []
        for i, rec in enumerate(recs):
            if rec.bottom >= row >= rec.top:
                captured_segments.append(rec.row_segment(row))
        
        captured_segments.sort()

        res = segment_hole(captured_segments, row, beacs, sens)
        if res:
            p2_ans = res[1] * 4000000 + res[0]
            break


    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p2_ans)