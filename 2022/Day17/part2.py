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
    rows = [[0 for _ in range(7)] for __ in range(high - low + 1)]

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


def move_shape(shape, move, shapes):
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


def height_with_given_shapes(shapes_cnt, next_move, next_shape):
    shapes = []
    floor = 0
    for _ in range(shapes_cnt):
        shape = Shape(next_shape(), 2, floor + 4)

        while not shape.fixed:
            move_shape(shape, next_move(), shapes)

        if shape.bottom + shape.height - 1 > floor:
            floor = shape.bottom + shape.height - 1
        shapes.append(shape)
    return floor


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    total_moves = len(lines[0].strip())

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
    move_count = 0
    
    goal = 1000000000000

    shape_i_repeats = []
    floor_repeats = []
    shape_interval = None
    floor_interval = None

    for shape_i in range(goal):
        shape = Shape(next_shape(), 2, floor + 4)

        while not shape.fixed:
            move_shape(shape, next_move(), shapes)
            move_count += 1
            
            if move_count % total_moves == 0:
                shape_i_repeats.append(shape_i)
                floor_repeats.append(floor)

        if shape.bottom + shape.height - 1 > floor:
            floor = shape.bottom + shape.height - 1
        shapes.append(shape)

        if len(shape_i_repeats) > 1:
            shape_interval = shape_i_repeats[1] - shape_i_repeats[0]
            floor_interval = floor_repeats[1] - floor_repeats[0]
            break
    
    rest = goal % shape_interval
    rest_height = height_with_given_shapes(rest + shape_interval, next_move_wrapper(), next_shape_wrapper())
    p2_ans = (goal // shape_interval - 1) * floor_interval + rest_height

    print("=================")
    print("-> Input", file_name)
    print("Part 2:")
    print(p2_ans)