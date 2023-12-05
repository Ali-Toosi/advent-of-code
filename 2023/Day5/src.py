def transform(endpoints, group):
    res = []
    for endpoint in endpoints:
        found = False
        for g_line in group:
            dst, src, rng = list(map(int, g_line.split()))
            if src <= endpoint <= src + rng:
                res.append(endpoint - src + dst)
                found = True
                break

        if not found:
            res.append(endpoint)

    return res


def find_matching_seed(target, groups):
    targets = [target]
    for group in groups:
        new_targets = []
        for target in targets:
            found = False
            for line in group:
                dst, src = line
                if dst[0] <= target <= dst[1]:
                    new_targets.append(src[0] + target - dst[0])
                    found = True
            if not found:
                new_targets.append(target)
        targets = new_targets
    return targets


def seed_available(seed, endpoints):
    for a, b in endpoints:
        if a <= seed <= b:
            return True
    return False


def p2(lines):
    endpoints_gen = list(map(int, lines[0].split(": ")[1].split()))
    endpoints = []
    for i in range(0, len(endpoints_gen), 2):
        endpoints.append((endpoints_gen[i], endpoints_gen[i] + endpoints_gen[i + 1]))

    groups = []
    i = 3
    while i < len(lines):
        groups.append([])
        while lines[i].strip() != "":
            dst, src, rng = list(map(int, lines[i].split()))
            groups[-1].append(((dst, dst + rng), (src, src + rng)))
            i += 1

        i += 2
        groups[-1] = list(sorted(groups[-1]))

    groups = list(reversed(groups))

    for target in range(1000000000):
        if target % 1000000 == 0:
            print(target)
        seeds = find_matching_seed(target, groups)
        for seed in seeds:
            if seed_available(seed, endpoints):
                return target

    return "Fuck"


def p1(lines):
    endpoints = list(map(int, lines[0].split(": ")[1].split()))

    groups = []
    i = 3
    while i < len(lines):
        groups.append([])
        while lines[i].strip() != "":
            groups[-1].append(lines[i])
            i += 1

        i += 2

    for group in groups:
        endpoints = transform(endpoints, group)

    return min(endpoints)


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

