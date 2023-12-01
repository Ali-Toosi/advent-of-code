def solve(lines):
    pass


def read_input(file_name):
    with open(file_name, "r") as f:
        input_lines = f.readlines()

    return input_lines


if __name__ == "__main__":
    for file_name in ["input.txt", "sample1.txt", "sample2.txt"]:
        try:
            lines = read_input(file_name)
        except FileNotFoundError:
            continue
        print("-> " + file_name)
        print(solve(lines))
