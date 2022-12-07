def read_input():
    with open("input.txt", "r") as f:
        input_lines = f.readlines()
    
    with open("sample.txt", "r") as f:
        sample_input_lines = f.readlines()
    
    # return sample_input_lines
    return input_lines


lines = read_input()

class Dir:
    def __init__(self, name="", parent=None):
        self.name = name
        self.parent = parent
        self.size = 0
        self.children = {}
        self.files = []

    def child(self, name):
        if name not in self.children.keys():
            self.children[name] = Dir(name, self)
        return self.children[name]
    
    def add_file(self, name, size):
        self.files.append(name)
        temp = self
        while temp is not None:
            temp.size += size
            temp = temp.parent


root = Dir()


def cd(current, dst):
    if dst == '..':
        if current == root:
            return current
        return current.parent
    else:
        if dst == '/':
            return root
        return current.child(dst)
        

current = root

for line in lines:
    line = line.strip()
    if line[0] == '$':
        if line[2:4] == "cd":
            current = cd(current, line.split()[2])
    else:
        args = line.split()
        if args[0] == "dir":
            current.child(args[1])
        else:
            current.add_file(args[1], int(args[0]))


answer = 0

def dfs(node, max_size):
    global answer
    if node.size <= max_size:
        answer += node.size
    for child in node.children.values():
        dfs(child, max_size)

# Part 1
dfs(root, 100000)
print("-> Part 1")
print(answer)


# Part 2
used = root.size
needed = 30000000 - (70000000 - used)

answer = ("None", 1e12)
def find_smallest(node, needed):
    global answer
    if node.size >= needed and node.size < answer[1]:
        answer = (node.name, node.size)
    for child in node.children.values():
        find_smallest(child, needed)


find_smallest(root, needed)
print("\n-> Part 2")
print(answer)

    
