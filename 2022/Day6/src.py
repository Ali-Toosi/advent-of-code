def read_input():
    with open("input.txt", "r") as f:
        input_lines = f.readlines()
    
    with open("sample_input.txt", "r") as f:
        sample_input_lines = f.readlines()
    
    # return sample_input_lines
    return input_lines


lines = read_input()

answer = 0

line = lines[0].strip()

unique_length = 4
# Part 2
# unique_length = 14
for i in range(len(line) - unique_length + 1):
    if len(set(list(line[i:i+unique_length]))) == unique_length:
        print(i + unique_length)
        break


