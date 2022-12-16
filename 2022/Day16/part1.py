from collections import defaultdict
import itertools


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


def get_src_from_line(line):
    return line.split()[1]


def get_flow_from_line(line):
    return int(line.split()[4].split('=')[-1][:-1])


def get_dst_from_line(line):
    all = line.split()[9:]
    res = []
    for valve in all:
        if valve[-1] == ',':
            valve = valve[:-1]
        res.append(valve)
    return res


def get_all_combinations(non_zero_nodes):
    res = []
    for L in range(len(non_zero_nodes) + 1):
        for subset in itertools.combinations(non_zero_nodes, L):
            res.append(subset)
    return res


def combination_flow(combination, flows):
    return sum([flows[node] for node in combination])


def solve_p1(nodes, edges, combinations, flows):
    dp = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    ans = 0

    for time in range(31):
        for comb in combinations:
            for node in nodes:
                if time == 0:
                    if node == 'AA' and not comb:
                        dp[time][comb][node] = 0
                    else:
                        dp[time][comb][node] = None
                    continue
                
                local_max = -1
                # Either open the current node
                if node in comb:
                    new_comb = tuple([c for c in comb if c != node])
                    if dp[time - 1][new_comb][node] is not None:
                        local_max = dp[time - 1][new_comb][node] + combination_flow(new_comb, flows)
                
                # Or just get here from a neighbour without opening
                for neighbour in edges[node]:
                    if dp[time - 1][comb][neighbour] is not None:
                        local_max = max(local_max, 
                            dp[time - 1][comb][neighbour] + combination_flow(comb, flows)
                        )
                
                if local_max == -1:
                    dp[time][comb][node] = None
                else:
                    dp[time][comb][node] = local_max

                if time == 30:
                    ans = max(ans, local_max)
    
    return ans


for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    # dict to set
    edges = defaultdict(set)
    nodes = set()
    non_zero_nodes = set()
    flows = dict()
    
    for line in lines:
        line = line.strip()
        
        src = get_src_from_line(line)
        nodes.add(src)

        flow = get_flow_from_line(line)
        flows[src] = flow
        if flow != 0:
            non_zero_nodes.add(src)

        dests = get_dst_from_line(line)
        for dest in dests:
            edges[src].add(dest)
        
    combinations = get_all_combinations(non_zero_nodes)
    p1_ans = solve_p1(nodes, edges, combinations, flows)

    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)