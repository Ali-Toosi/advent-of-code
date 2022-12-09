def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def touches(self, point):
        return abs(self.x - point.x) <= 1 and abs(self.y - point.y) <= 1
        
    def update_pos(self, d):
        self.x += d[0]
        self.y += d[1]
    
    def pos(self):
        return self.x, self.y


def tail_move(head, tail):
    if head.touches(tail):
        return 0, 0
    
    dx = (head.x - tail.x) // abs(head.x - tail.x) if head.x != tail.x else 0
    dy = (head.y - tail.y) // abs(head.y - tail.y) if head.y != tail.y else 0
    
    return dx, dy

movement_map = {
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "U": (0, -1)
}

for file_name in ["input.txt", "sample1.txt", "sample2.txt"]:
    lines = read_input(file_name)

    parts = []
    for knots_cnt in [1, 9]:
        knots = [Point(0, 0) for _ in range(knots_cnt)]

        head = Point(0, 0)
        tail = knots[-1]

        seen = {tail.pos()}

        for line in lines:
            d, l = line.strip().split()

            for step in range(int(l)):
                head.update_pos(movement_map[d])
                for i in range(len(knots)):
                    prev = head if i == 0 else knots[i - 1]
                    knots[i].update_pos(tail_move(prev, knots[i]))
                
                seen.add(tail.pos())
        
        parts.append(len(seen))

    print("Input", file_name)
    print("Part 1:", parts[0])
    print("Part 2:", parts[1])
    print("=================")
