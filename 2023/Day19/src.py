class Part:
    def __init__(self, line):
        line = line[1:-1].split(",")
        self.x = int(line[0][2:])
        self.m = int(line[1][2:])
        self.a = int(line[2][2:])
        self.s = int(line[3][2:])


class Workflow:
    def __init__(self, line):
        self.name = line.split("{", 1)[0]
        self.next = set()
        self.prev = set()
        self.rules = []

        _rules = line[len(self.name) + 1:-1].split(",")
        for rule in _rules:
            if ":" in rule:
                self.rules.append(rule.split(":"))
                dst = rule.split(":")[1]
                if dst not in "RA":
                    self.next.add(dst)
            else:
                self.rules.append(("x!=None", rule))
                if rule not in "RA":
                    self.next.add(rule)

        self.unprocessed_nexts = len(self.next)
        self.success_conditions = []


class Condition:
    def __init__(self, x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000)):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def length(self):
        xlen = (self.x[1] - self.x[0] + 1)
        mlen = (self.m[1] - self.m[0] + 1)
        alen = (self.a[1] - self.a[0] + 1)
        slen = (self.s[1] - self.s[0] + 1)
        if any([lens < 0 for lens in [xlen, mlen, alen, slen]]):
            return 0
        return xlen * mlen * alen * slen

    def apply_rule(self, rule: str, reverse=False):
        _copy = Condition(self.x, self.m, self.a, self.s)
        c = rule[0]
        o = rule[1]
        val = int(rule[2:])
        changed = [getattr(_copy, c)[0], getattr(_copy, c)[1]]
        if o == "<":
            if not reverse:
                changed[1] = min(val - 1, getattr(_copy, c)[1])
            else:
                changed[0] = max(val, getattr(_copy, c)[0])
        elif o == ">":
            if not reverse:
                changed[0] = max(val + 1, getattr(_copy, c)[0])
            else:
                changed[1] = min(val, getattr(_copy, c)[1])
        else:
            raise Exception("Didn't expect this!")

        setattr(_copy, c, tuple(changed))
        return _copy

    def apply_condition(self, other):
        x = [max(self.x[0], other.x[0]), min(self.x[1], other.x[1])]
        m = [max(self.m[0], other.m[0]), min(self.m[1], other.m[1])]
        a = [max(self.a[0], other.a[0]), min(self.a[1], other.a[1])]
        s = [max(self.s[0], other.s[0]), min(self.s[1], other.s[1])]
        return Condition(x, m, a, s)

    def print(self):
        print(f"{self.x[0]} <= X <= {self.x[1]}")
        print(f"{self.m[0]} <= M <= {self.m[1]}")
        print(f"{self.a[0]} <= A <= {self.a[1]}")
        print(f"{self.s[0]} <= S <= {self.s[1]}")


def process_part_in_workflow(part: Part, workflow):
    for rule in workflow.rules:
        if eval("part." + rule[0]):
            return rule[1]


def process_part(part, workflows):
    current = "in"
    while current not in ["R", "A"]:
        current = process_part_in_workflow(part, workflows[current])

    return current == "A"


def figure_workflow_conditions(workflows, w):
    workflow = workflows[w]
    carry_condition = Condition()
    for rule in workflow.rules:
        if "None" in rule[0]:
            if rule[1] == "A":
                workflow.success_conditions.append(carry_condition)
            elif rule[1] != "R":
                for condition in workflows[rule[1]].success_conditions:
                    workflow.success_conditions.append(condition.apply_condition(carry_condition))
            break

        dst = rule[1]
        if dst == "A":
            workflow.success_conditions.append(carry_condition.apply_rule(rule[0]))
        elif dst != "R":
            for condition in workflows[dst].success_conditions:
                workflow.success_conditions.append(condition.apply_condition(carry_condition).apply_rule(rule[0]))

        carry_condition = carry_condition.apply_rule(rule[0], True)


def backtrack_workflows(workflows: dict[str, Workflow]):
    while True:
        found_any = False
        for w in workflows:
            if workflows[w].unprocessed_nexts == 0:
                workflows[w].unprocessed_nexts = -1
                found_any = True
                figure_workflow_conditions(workflows, w)
                for p in workflows[w].prev:
                    workflows[p].unprocessed_nexts -= 1
        if not found_any:
            break


def solve(lines):
    p1 = p2 = 0

    workflows = {}
    i = 0
    for line in lines:
        if line == "":
            break
        i += 1
        w = Workflow(line)
        workflows[w.name] = w

    for w in workflows:
        for n in workflows[w].next:
            workflows[n].prev.add(w)

    backtrack_workflows(workflows)
    for cond in workflows["in"].success_conditions:
        p2 += cond.length()

    for line in lines[i + 1:]:
        part = Part(line)
        if process_part(part, workflows):
            p1 += part.x + part.m + part.a + part.s

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
        print(solve(_lines))

