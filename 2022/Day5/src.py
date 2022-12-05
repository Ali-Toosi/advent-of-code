def read_input():
    with open("input.txt", "r") as f:
        input_lines = f.readlines()
    
    with open("sample_input.txt", "r") as f:
        sample_input_lines = f.readlines()
    
    lines = input_lines
    # lines = sample_input_lines
    
    good_lines = []
    stack_rows = []
    stack_nums = None
    for line in lines:
        if line[0] == '[':
            stack_rows.append(line)
        elif line[0:2] == ' 1':
            stack_nums = line.strip()
        else:
            good_lines.append(line.strip())
    
    stack_nums = max(list(map(int, stack_nums.split())))
    stack_rows = list(reversed(stack_rows))
    stack_lines = []
    for stack_num in range(stack_nums):
        line = ''
        for stack_row in stack_rows:
            offset = 4 * stack_num + 1
            line += stack_row[offset]
        stack_lines.append(line.strip())
    
    good_lines = stack_lines + good_lines
    return good_lines


lines = read_input()

stacks = []

cnt = 0
for line in lines:
    cnt += 1
    if not line.strip():
        break

    stacks.append(list(line.strip()))

for line in lines[cnt:]:
    q, src, dst = int(line.split()[1]), int(line.split()[3]) - 1, int(line.split()[5]) - 1
    removed = stacks[src][-1*q:]
    stacks[src] = stacks[src][:-1*q]
    # Part 1
    # stacks[dst].extend(list(reversed(removed)))
    # Part 2
    stacks[dst].extend(removed)

answer = ''.join([stack[-1] for stack in stacks])

print(answer)