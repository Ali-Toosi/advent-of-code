def add(r, c, d):
    return r + d[0], c + d[1]


def is_in(grid, r, c):
    return len(grid) > r >= 0 and len(grid[0]) > c >= 0


def move_beam(grid, r, c, d, energised, beam_seen):
    d_map = {
        ".": {
            (0, 1): ((0, 1),),
            (0, -1): ((0, -1),),
            (1, 0): ((1, 0),),
            (-1, 0): ((-1, 0),)
        },
        "|": {
            (0, 1): ((1, 0), (-1, 0)),
            (0, -1): ((1, 0), (-1, 0)),
            (1, 0): ((1, 0),),
            (-1, 0): ((-1, 0),)
        },
        "-": {
            (0, 1): ((0, 1),),
            (0, -1): ((0, -1),),
            (1, 0): ((0, 1), (0, -1)),
            (-1, 0): ((0, 1), (0, -1))
        },
        "/": {
            (0, 1): ((-1, 0),),
            (0, -1): ((1, 0),),
            (1, 0): ((0, -1),),
            (-1, 0): ((0, 1),)
        },
        "\\": {
            (0, 1): ((1, 0),),
            (0, -1): ((-1, 0),),
            (1, 0): ((0, 1),),
            (-1, 0): ((0, -1),)
        },
    }
    energised[r][c] = 1

    new_beams = []
    nds = d_map[grid[r][c]][d]
    for nd in nds:
        nr, nc = add(r, c, nd)
        if not is_in(grid, nr, nc):
            continue
        if beam_seen[nr][nc][nd]:
            continue
        beam_seen[nr][nc][nd] = True
        new_beams.append((nr, nc, nd))
    return new_beams


def process_beams(grid, initial_beam):
    energized = [[0 for _ in range(len(grid[0]))] for __ in range(len(grid))]
    beam_seen = [
        [
            {d: False for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]}
            for _ in range(len(grid[0]))
        ]
        for __ in range(len(grid))
    ]
    beam_seen[initial_beam[0]][initial_beam[1]][initial_beam[2]] = True
    beams = [initial_beam]
    for cycle in range(len(grid) * len(grid[0])):
        new_beams = []
        while len(beams) > 0:
            beam = beams.pop(0)
            new_beams.extend(move_beam(grid, *beam, energized, beam_seen))
        beams = new_beams

    return sum(sum(energized[r]) for r in range(len(energized)))


def solve(grid):
    p1 = process_beams(grid, (0, 0, (0, 1)))

    candidates = []
    for r in range(len(grid)):
        candidates.append(process_beams(grid, (r, 0, (0, 1))))
        candidates.append(process_beams(grid, (r, len(grid[0]) - 1, (0, -1))))
    for c in range(len(grid[0])):
        candidates.append(process_beams(grid, (0, c, (1, 0))))
        candidates.append(process_beams(grid, (len(grid) - 1, c, (-1, 0))))

    p2 = max(candidates)
    return p1, p2


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            lines = list(map(lambda x: list(x.strip()), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))

