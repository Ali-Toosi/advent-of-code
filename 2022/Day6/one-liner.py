print(*[[
    min([i for i in range(len(line) - u_len + 1) if len(set(list(line[i:i+u_len]))) == u_len]) + u_len
    for u_len in [4, 14]] for line in open("input.txt").readlines()
])