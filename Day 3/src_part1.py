import string

with open("input.txt", "r") as f:
    lines = f.readlines()

commons = []

for line in lines:
    a, b = line[:len(line)//2], line[len(line)//2:]
    common = set()
    for ac in a:
        if ac in b:
            common.add(ac)
    commons.append(list(common))

def priority(character):
    all_chars = string.ascii_lowercase + string.ascii_uppercase
    return all_chars.index(character) + 1

ans = 0
for common in commons:
    for common_char in common:
        ans += priority(common_char)

print(ans)