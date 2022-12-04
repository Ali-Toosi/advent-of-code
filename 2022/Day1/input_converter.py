with open("clean_input.txt", "w") as output:
    with open("input.txt", "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                output.write("-1\n")
            else:
                output.write(line)
