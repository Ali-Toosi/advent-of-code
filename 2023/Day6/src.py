def p2(lines):
    times_line = lines[0].split(":")[1].strip()
    times_line = times_line.replace(" ", "")
    times = list(map(int, times_line.split()))

    targets_line = lines[1].split(":")[1].strip()
    targets_line = targets_line.replace(" ", "")
    targets = list(map(int, targets_line.split()))

    races = []
    ans = []
    for i in range(len(times)):
        races.append(Race(times[i], targets[i]))
        ans.append(solve(races[-1]))

    if len(ans) == 0:
        return 0

    p2 = 1
    for a in ans:
        p2 *= a

    return p2


class Race:
    def __init__(self, time, target):
        self.time = time
        self.target = target


def solve(race: Race):
    ans = 0
    for duration in range(race.time + 1):
        speed = duration
        if speed * (race.time - duration) > race.target:
            ans += 1
    return ans


def p1(lines):
    times_line = lines[0].split(":")[1].strip()
    while "  " in times_line:
        times_line = times_line.replace("  ", " ")
    times = list(map(int, times_line.split()))

    targets_line = lines[1].split(":")[1].strip()
    while "  " in targets_line:
        targets_line = targets_line.replace("  ", " ")
    targets = list(map(int, targets_line.split()))

    races = []
    ans = []
    for i in range(len(times)):
        races.append(Race(times[i], targets[i]))
        ans.append(solve(races[-1]))

    if len(ans) == 0:
        return 0

    p1 = 1
    for a in ans:
        p1 *= a


    return p1


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            lines = list(map(lambda x: x.strip(), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(p1(lines), p2(lines))

