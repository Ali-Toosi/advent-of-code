# Part 1
print(sum([{"X": 1,"Y": 2,"Z": 3}[line.split()[1]] + {"X": {"A": 3, "B": 0, "C": 6},"Y": {"A": 6, "B": 3, "C": 0},"Z": {"A": 0, "B": 6, "C": 3},}[line.split()[1]][line.split()[0]] for line in open("input.txt").readlines()]))

# Part 2
print(sum([{"X": 1,"Y": 2,"Z": 3}[{"X": {"A": "Z", "B": "X", "C": "Y"},"Y": {"A": "X", "B": "Y", "C": "Z"},"Z": {"A": "Y", "B": "Z", "C": "X"}}[line.split()[1]][line.split()[0]]] + {"X": {"A": 3, "B": 0, "C": 6},"Y": {"A": 6, "B": 3, "C": 0},"Z": {"A": 0, "B": 6, "C": 3},}[{"X": {"A": "Z", "B": "X", "C": "Y"},"Y": {"A": "X", "B": "Y", "C": "Z"},"Z": {"A": "Y", "B": "Z", "C": "X"}}[line.split()[1]][line.split()[0]]][line.split()[0]] for line in open("input.txt").readlines()]))
