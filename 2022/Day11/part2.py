def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


class Number:
    def __init__(self, x):
        self.divs = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        self.div = {d: x % d for d in self.divs}
    
    def add(self, val):
        for d in self.divs:
            self.div[d] += val
            self.div[d] %= d

    def multiply(self, val):
        for d in self.divs:
            self.div[d] *= val
            self.div[d] %= d

    def power(self):
        for d in self.divs:
            self.div[d] *= self.div[d]
            self.div[d] %= d

    def test(self, val):
        return self.div[val] == 0



class Monkey:
    def __init__(self, text):
        self.items = list(map(lambda x: Number(x), map(int, text[1].strip().split(':')[-1].strip().split(', '))))

        try:
            val = int(text[2].strip().split()[-1])
            op = text[2].strip().split()[-2]
            self.op = (lambda x: x.multiply(val)) if op == '*' else (lambda x: x.add(val))
        except ValueError:
            self.op = lambda x: x.power()
        

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
            self.op(item)

            dest = self.dests[item.test(self.test)]
            transfers.append((dest, item))
        
        self.items = []
        return transfers



for file_name in ["input.txt", "sample1.txt"]:
    lines = read_input(file_name)
    p2_ans = 0

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
    
    for rnd in range(10000):
        for i, monkey in enumerate(monkeys):
            transfers = monkey.inspect()
            
            for transfer in transfers:
                monkeys[transfer[0]].items.append(transfer[1])
    
    sorted_monkeys = sorted(monkeys, key=lambda x: -1 * x.inspections)
    p2_ans = sorted_monkeys[0].inspections * sorted_monkeys[1].inspections


    print("=================")
    print("-> Input", file_name)
    print("Part 2:")
    print(p2_ans)
