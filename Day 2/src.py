with open("input.txt", "r") as f:
    lines = f.readlines()

score = 0

move_scores = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

win_scores = {
    "X": {"A": 3, "B": 0, "C": 6},
    "Y": {"A": 6, "B": 3, "C": 0},
    "Z": {"A": 0, "B": 6, "C": 3},
}

alter_move = {
    "X": {"A": "Z", "B": "X", "C": "Y"},
    "Y": {"A": "X", "B": "Y", "C": "Z"},
    "Z": {"A": "Y", "B": "Z", "C": "X"},
}

for line in lines:
    them, me = line.split()
    # Part two
    # me = alter_move[me][them]
    score += move_scores[me]
    score += win_scores[me][them]

print(score)
