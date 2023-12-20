from math import gcd


def lcm(l):
    ans = 1
    for i in l:
        ans = (ans * i) // gcd(ans, i)
    return ans


class Module:
    def __init__(self, line):
        self.type = line[0]
        name, dst = line[1:].split(" -> ", 1)
        self.name = name
        self.dst = dst.split(", ")

        self.recv = {}
        self.flip = False

    def send_pulse(self, modules: dict):
        if self.type == "%":
            val = self.flip
        else:
            all_vals = list(self.recv.values())
            if False in all_vals:
                val = True
            else:
                val = False

        res = []
        for dst in self.dst:
            if dst in modules:
                modules[dst].receive_pulse(self.name, val)
            res.append(dst)
        return res, val

    def receive_pulse(self, src, val):
        if self.type == "%":
            if not val:
                self.flip = not self.flip
        else:
            self.recv[src] = val


def propagate(start, modules, look_for=tuple()):
    on_cnt = off_cnt = 0
    for s in start:
        modules[s].receive_pulse("broadcaster", False)
        off_cnt += 1

    gave_high = {x: 0 for x in look_for}
    q = [x for x in start]
    while len(q) > 0:
        top: Module = modules[q.pop(0)]
        new_dsts, val = top.send_pulse(modules)
        for new_dst in new_dsts:
            # print(top.name, f"-{val}->", new_dst)
            on_cnt += 1 if val else 0
            off_cnt += 0 if val else 1
            if (new_dst not in modules) or (modules[new_dst].type == "%" and val):
                continue
            q.append(new_dst)
        if val and top.name in look_for:
            gave_high[top.name] += 1

    return on_cnt, off_cnt, gave_high


def _setup(lines):
    modules = {}
    start = []
    for line in lines:
        if line.startswith("broad"):
            start = line.split(" -> ")[1].split(", ")
        else:
            m = Module(line)
            modules[m.name] = m

    for m in modules:
        for d in modules[m].dst:
            if d in modules and modules[d].type == "&":
                modules[d].recv[m] = False

    return modules, start


def solve(lines, file):
    modules, start = _setup(lines)
    on_cnt = off_cnt = 0
    for btn in range(1000):
        off_cnt += 1
        a, b, _ = propagate(start, modules)
        on_cnt += a
        off_cnt += b
    p1 = on_cnt * off_cnt

    modules, start = _setup(lines)
    if file != "input.txt":
        p2 = 0
    else:
        rx_root = list(filter(lambda x: "rx" in x, lines))[0].split(" -> ")[0][1:]
        look_for = {x: [] for x in modules[rx_root].recv.keys()}
        for btn in range(10000):
            _, _, gave_high = propagate(start, modules, tuple(look_for.keys()))
            for l in look_for:
                if gave_high[l] == 1:
                    look_for[l].append(btn + 1)
                elif gave_high[l] > 1:
                    raise Exception("What now")

        print(look_for)
        p2 = lcm([lf[0] for lf in look_for.values()])

    return p1, p2


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["sample1.txt", "sample2.txt", "input.txt"]:
        try:
            _lines = list(map(lambda x: x.strip(), read_input(file_name)))
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(_lines, file_name))

