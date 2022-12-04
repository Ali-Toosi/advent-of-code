import string

with open("input.txt", "r") as f:
    lines = f.readlines()

def priority(character):
    all_chars = string.ascii_lowercase + string.ascii_uppercase
    return all_chars.index(character) + 1


def find_common(a, b, c):
    return list(set(a.strip()).intersection(set(b.strip())).intersection(set(c.strip())))

answer = 0
for i in range(0, len(lines), 3):
    answer += priority(find_common(lines[i], lines[i + 1], lines[i + 2])[0])

print(answer)