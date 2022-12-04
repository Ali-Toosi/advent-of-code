def read_input():
    with open("input.txt", "r") as f:
        input_lines = f.readlines()
    
    with open("sample_input.txt", "r") as f:
        sample_input_lines = f.readlines()
    
    # return sample_input_lines
    return input_lines


lines = read_input()

answer = 0

for line in lines:
    p1, p2 = map(int, line.split(',')[0].split('-'))
    q1, q2 = map(int, line.split(',')[1].split('-'))

    # Part 1
    # if (p1 >= q1 and p2 <= q2) or (q1 >= p1 and q2 <= p2):
    # Part 2
    if (p1 >= q1 and p1 <= q2) or (q1 >= p1 and q1 <= p2):
        answer += 1

print(answer)