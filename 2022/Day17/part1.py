from collections import defaultdict
import itertools


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class Shape:
    def __init__(self, shape, left, bottom) -> None:
        self.fixed = False
        self.shape = shape
        self.left = left
        self.bottom = bottom
        self.height = {
            "dash": 1,
            "plus": 3,
            "l": 3,
            "i": 4,
            "square": 2
        }[self.shape]
        self.rows = {
            "dash": [
                [1, 1, 1, 1],
            ],
            "plus": [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            "l": [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1]
            ],
            "i": [
                [1],
                [1],
                [1],
                [1]
            ],
            "square": [
                [1, 1],
                [1, 1]
            ]
        }[self.shape]
    
    def can_go(self, dir, rows):
        return getattr(self, f"goes_{dir}_{self.shape}")(rows)
    
    def goes_down_dash(self, rows):
        bottom = rows[1]
        return all([x == 0 for x in [
            bottom[self.left],
            bottom[self.left + 1],
            bottom[self.left + 2],
            bottom[self.left + 3],
        ]])

    def goes_down_plus(self, rows):
        current = rows[2]
        bottom = rows[3]
        return all([x == 0 for x in [
            current[self.left],
            current[self.left + 2],
            bottom[self.left + 1]
        ]])
    
    def goes_down_l(self, rows):
        bottom = rows[3]
        return all([x == 0 for x in [
            bottom[self.left],
            bottom[self.left + 1],
            bottom[self.left + 2]
        ]])
    
    def goes_down_i(self, rows):
        bottom = rows[4]
        return all([x == 0 for x in [
            bottom[self.left]
        ]])
    
    def goes_down_square(self, rows):
        bottom = rows[2]
        return all([x == 0 for x in [
            bottom[self.left],
            bottom[self.left + 1]
        ]])
    
    def goes_left_dash(self, rows):
        return all([x == 0 for x in [
            rows[0][self.left - 1] if self.left > 0 else 1
        ]])

    def goes_left_plus(self, rows):
        return all([x == 0 for x in [
            rows[0][self.left],
            rows[1][self.left - 1] if self.left > 0 else 1,
            rows[2][self.left]
        ]])
    
    def goes_left_l(self, rows):
        return all([x == 0 for x in [
            rows[0][self.left],
            rows[0][self.left + 1],
            rows[1][self.left],
            rows[1][self.left + 1],
            rows[2][self.left - 1] if self.left > 0 else 1
        ]])
    
    def goes_left_i(self, rows):
        return all([x == 0 for x in [
            rows[i][self.left - 1] if self.left > 0 else 1
            for i in range(4)
        ]])

    def goes_left_square(self, rows):
        return all([x == 0 for x in [
            rows[i][self.left - 1] if self.left > 0 else 1
            for i in range(2)
        ]])

    def goes_right_dash(self, rows):
        return all([x == 0 for x in [
            rows[0][self.left + 4] if self.left + 4 < 7 else 1
        ]])

    def goes_right_plus(self, rows):
        return all([x == 0 for x in [
            rows[0][self.left + 2],
            rows[1][self.left + 3] if self.left + 3 < 7 else 1,
            rows[2][self.left + 2]
        ]])
    
    def goes_right_l(self, rows):
        return all([x == 0 for x in [
            rows[i][self.left + 3] if self.left + 3 < 7 else 1
            for i in range(3)
        ]])
    
    def goes_right_i(self, rows):
        return all([x == 0 for x in [
            rows[i][self.left + 1] if self.left + 1 < 7 else 1
            for i in range(4)
        ]])
    
    def goes_right_square(self, rows):
        return all([x == 0 for x in [
            rows[i][self.left + 2] if self.left + 2 < 7 else 1
            for i in range(2)
        ]])


def create_rows(low, high, shapes):
    rows = [[0 for _ in range(7)] for __ in range(5)]

    for row in range(low, high + 1):
        if row <= 0:
            rows[high - row] = [1 for _ in range(7)]

    for shape in shapes:
        bottom = shape.bottom
        top = shape.bottom + shape.height - 1

        for shape_row in range(bottom, top + 1):
            if shape_row < low or shape_row > high:
                continue
            desired_shape_row = shape.height - (shape_row - bottom) - 1
            for i in range(len(shape.rows[desired_shape_row])):
                rows[high - shape_row][shape.left + i] |= shape.rows[desired_shape_row][i]
    return rows
        

for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    def next_move_wrapper():
        moves = lines[0].strip()
        total = len(moves)
        turn = -1
        def next_move():
            nonlocal turn
            turn = (turn + 1) % total
            return moves[turn]
        return next_move
    
    def next_shape_wrapper():
        shapes = ["dash", "plus", "l", "i", "square"]
        total = 5
        turn = -1
        def next_shape():
            nonlocal turn
            turn = (turn + 1) % total
            return shapes[turn]
        return next_shape

    next_move = next_move_wrapper()
    next_shape = next_shape_wrapper()
    shapes = []
    floor = 0

    for shape_i in range(2022):
        shape = Shape(next_shape(), 2, floor + 4)

        while not shape.fixed:
            move = next_move()
            rows = create_rows(shape.bottom + shape.height - 5, shape.bottom + shape.height - 1, shapes)
            if shape.can_go("right" if move == '>' else "left", rows):
                if move == '<':
                    shape.left -= 1
                else:
                    shape.left += 1
            if shape.can_go("down", rows):
                shape.bottom -= 1
            else:
                shape.fixed = 1

        if shape.bottom + shape.height - 1 > floor:
            floor = shape.bottom + shape.height - 1
        shapes.append(shape)
        
    
    p1_ans = floor

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)