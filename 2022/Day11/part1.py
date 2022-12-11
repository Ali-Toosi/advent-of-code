def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class Monkey:
    def __init__(self, text):
        self.items = list(map(int, text[1].strip().split(':')[-1].strip().split(', ')))

        try:
            val = int(text[2].strip().split()[-1])
            op = text[2].strip().split()[-2]
            self.op = (lambda x: x * val) if op == '*' else (lambda x: x + val)
        except ValueError:
            self.op = lambda x: x * x
        

        self.test = int(text[3].strip().split()[-1])

        self.dests = {
            True: int(text[4].strip().split()[-1]),
            False: int(text[5].strip().split()[-1]),
        }

        self.inspections = 0

    def inspect(self):
        self.inspections += len(self.items)
        transfers = []
        for item in self.items:
            item = self.op(item)
            item //= 3

            dest = self.dests[item % self.test == 0]
            transfers.append((dest, item))
        
        self.items = []
        return transfers



for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p1_ans = 0

    monkeys = []
    current_monkey = []
    for line in lines:
        line = line.strip()
        if line == "":
            monkeys.append(Monkey(current_monkey))
            current_monkey = []
        else:
            current_monkey.append(line)
    
    monkeys.append(Monkey(current_monkey))
    
    for rnd in range(20):
        for i, monkey in enumerate(monkeys):
            transfers = monkey.inspect()
            
            for transfer in transfers:
                monkeys[transfer[0]].items.append(transfer[1])
    
    sorted_monkeys = sorted(monkeys, key=lambda x: -1 * x.inspections)
    p1_ans = sorted_monkeys[0].inspections * sorted_monkeys[1].inspections


    print("=================")
    print("-> Input", file_name)
    print("Part 1:")
    print(p1_ans)