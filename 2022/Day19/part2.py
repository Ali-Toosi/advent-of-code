from parse import parse


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def add(v1, v2):
    return tuple([v1[i] + v2[i] for i in range(4)])


def neg(v1, v2):
    return tuple([v1[i] - v2[i] for i in range(4)])


def can_afford(move, costs, time, resources, bots):
    # If we actually can't afford
    if any([costs[move][i] > resources[i] for i in range(4)]):
        return False

    # If we already have enough bots
    if move != 3 and bots[move] >= max([
        costs[i][move] for i in range(4)
    ]):
        return False
    
    # If we already have enough resources
    if move != 3 and resources[move] >= max([
        costs[i][move] for i in range(4)
    ]) * (33 - time):
        return False
    
    return True
    

def dfs(costs, state):
    time, resources, bots = state
    ans = resources[3]

    if time == 32:
        return ans
    
    for move in range(4):
        local_resources = resources
        for when in range(time + 1, 33):
            if can_afford(move, costs, when, local_resources, bots):
                ans = max(ans, dfs(
                    costs,
                    (
                        when,
                        neg(add(local_resources, bots), costs[move]),
                        add(bots, tuple(0 if i != move else 1 for i in range(4)))
                    )
                ))
                break
            local_resources = add(local_resources, bots)
    
    return ans



def get_blueprint_quality(line):
    parts = list(map(int,
        parse("Blueprint {}: Each ore robot costs {} ore. Each clay robot costs {} ore. Each obsidian robot costs {} ore and {} clay. Each geode robot costs {} ore and {} obsidian.", line.strip())
    ))
    costs = (
        (parts[1], 0, 0, 0),            # 0 - Ore
        (parts[2], 0, 0, 0),            # 1 - Clay
        (parts[3], parts[4], 0, 0),     # 2 - Obs
        (parts[5], 0, parts[6], 0)      # 3 - Geo
    )

    starting_state = (
        0,              # Minutes passed
        (0, 0, 0, 0),   # Resources after this minute
        (1, 0, 0, 0)    # Bots after this minute
    )

    return dfs(costs, starting_state)


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p2_ans = 0

    qualities = []

    for i, line in enumerate(lines):
        print("Line", i)
        if i > 2:
            break
        qualities.append(get_blueprint_quality(line))

    # Sample input only has 2 blueprints
    if len(qualities) < 3:
        qualities.append(1)

    p2_ans = qualities[0] * qualities[1] * qualities[2]

    print("=================")
    print("-> Input", file_name)
    print("Part 2:")
    print(p2_ans)