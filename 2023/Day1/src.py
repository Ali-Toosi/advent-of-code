def find_goals(line: str, only_digits):
    goals = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if not only_digits:
        goals += ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    min_goal = None
    max_goal = None
    for goal in goals:
        try:
            l_index = line.index(goal)
            r_index = line.rindex(goal)
        except ValueError:
            continue

        if min_goal is None or line.index(min_goal) > l_index:
            min_goal = goal
        if max_goal is None or line.rindex(max_goal) < r_index:
            max_goal = goal

    if min_goal and max_goal:
        return (goals.index(min_goal) % 9) + 1, (goals.index(max_goal) % 9) + 1
    return 0, 0


def solve(lines):
    p1 = p2 = 0
    for i, line in enumerate(lines):
        p1_first, p1_last = find_goals(line, True)
        p2_first, p2_last = find_goals(line, False)
        p1 += p1_first * 10 + p1_last
        p2 += p2_first * 10 + p2_last

    return p1, p2


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

