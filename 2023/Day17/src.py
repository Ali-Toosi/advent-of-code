RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


class N:
    def __init__(self, r, c, d, s, parent):
        self.r = r
        self.c = c
        self.d = d
        self.s = s
        self.parent = parent

    def apply_d(self, d):
        nr, nc = self.r + d[0], self.c + d[1]
        return N(nr, nc, d, self.s + 1 if self.d == d else 1, self)

    def in_grid(self, grid):
        return len(grid) > self.r >= 0 and len(grid[0]) > self.c >= 0

    def __hash__(self):
        return hash((self.r, self.c, self.d[0], self.d[1], self.s))

    def __eq__(self, other):
        return (self.r, self.c, self.d, self.s) == (other.r, other.c, other.d, other.s)

    def __str__(self):
        return f"{self.r}, {self.c} - {str(self.d)} at {self.s}"

    def __repr__(self):
        return str(self)


def rev(d):
    return {
        RIGHT: LEFT,
        LEFT: RIGHT,
        UP: DOWN,
        DOWN: UP
    }[d]


def best_neighbour(neis):
    return min(neis.items(), key=lambda n: n[1])[0]


def shortest_paths(grid, min_straight, max_straight):
    dstr, dstc = len(grid) - 1, len(grid[0]) - 1
    root = N(0, 0, UP, 0, None)
    lens = {root: 0}
    neis = {N(0, 1, RIGHT, 1, root): grid[0][0], N(1, 0, DOWN, 1, root): grid[0][0]}

    while True:
        best_nei = best_neighbour(neis)
        del neis[best_nei]
        distance = lens[best_nei.parent] + grid[best_nei.parent.r][best_nei.parent.c]
        if best_nei.r == dstr and best_nei.c == dstc and best_nei.s >= min_straight:
            return distance + grid[dstr][dstc] - grid[0][0]

        lens[best_nei] = distance
        for d in [RIGHT, LEFT, UP, DOWN]:
            if d == rev(best_nei.d) or (d == best_nei.d and best_nei.s == max_straight):
                continue
            if d != best_nei.d and best_nei.s < min_straight:
                continue
            new_n = best_nei.apply_d(d)
            if new_n.in_grid(grid) and new_n not in lens and new_n not in neis:
                neis[new_n] = distance + grid[best_nei.r][best_nei.c]


def solve(grid):
    p1 = shortest_paths(grid, 1, 3)
    p2 = shortest_paths(grid, 4, 10)

    return p1, p2


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            lines = list(map(lambda x: list(map(int, list(x.strip()))), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))

