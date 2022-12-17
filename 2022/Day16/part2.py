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


def get_duo_edges(nodes, edges):
    pass


def combination_flow(combination, flows):
    return sum([flows[node] for node in combination])


def solve_p2(nodes, edges, combinations, flows):
    dp = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0))))
    ans = 0
    lnodes = list(nodes)
    print(len(nodes))
    print(len(combinations))
    for time in range(27):
        print("Time", time)
        if time > 2:
            del dp[time - 2]
        for comb in combinations:
            for i in range(len(nodes)):
                for j in range(i, len(nodes)):
                    me = lnodes[i]
                    elephant = lnodes[j]
                    
                    if time == 0:
                        if me == 'AA' and elephant == 'AA' and not comb:
                            dp[time][comb][me][elephant] = dp[time][comb][elephant][me] = 0
                        else:
                            dp[time][comb][me][elephant] = dp[time][comb][elephant][me] = None
                        continue
                
                    local_max = -1
                    
                    # We both open
                    if me in comb and elephant in comb:
                        new_comb = tuple([c for c in comb if c not in [me, elephant]])
                        if dp[time - 1][new_comb][me][elephant] is not None:
                            local_max = dp[time - 1][new_comb][me][elephant] + combination_flow(new_comb, flows)
                    
                    # Only I open
                    if me in comb:
                        new_comb = tuple([c for c in comb if c not in [me]])
                        local_dp = dp[time - 1][new_comb][me]
                        for neighbour in edges[elephant]:
                            if local_dp[neighbour] is not None:
                                local_max = max(local_max, 
                                   local_dp[neighbour] + combination_flow(new_comb, flows)
                                )
                    
                    # Only elephant opens
                    if elephant in comb:
                        new_comb = tuple([c for c in comb if c not in [elephant]])
                        local_dp = dp[time - 1][new_comb]
                        for neighbour in edges[me]:
                            if local_dp[neighbour][elephant] is not None:
                                local_max = max(local_max, 
                                    local_dp[neighbour][elephant] + combination_flow(new_comb, flows)
                                )
                    
                    # Neither opens
                    local_dp = dp[time - 1][comb]
                    for my_neighbour in edges[me]:
                        for elephant_neighbour in edges[elephant]:
                            if local_dp[my_neighbour][elephant_neighbour] is not None:
                                local_max = max(local_max,
                                    local_dp[my_neighbour][elephant_neighbour] + combination_flow(comb, flows)
                                )

                    if local_max == -1:
                        dp[time][comb][me][elephant] = dp[time][comb][elephant][me] = None
                    else:
                        dp[time][comb][me][elephant] = dp[time][comb][elephant][me] = local_max

                    if time == 26:
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
    # p1_ans = solve_p1(nodes, edges, combinations, flows)
    p2_ans = solve_p2(nodes, edges, combinations, flows)


    print("=================")
    print("-> Input", file_name)
    print("Part 2:")
    print(p2_ans)