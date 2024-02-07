def generate_triangle_pattern(n: int):
    # Loop `n` times
    #
    # The counters are offset by +1
    # so that zero multiplication doesn't happen
    for i in range(1, n + 1):
        # Initialize variable to store list of numbers
        # which are to be printed to the line
        line: list[int] = []
        # There are `line_number` times of numbers per line,
        # so loop that many times
        for j in range(1, i + 1):
            # The numbers apparently adhere to the formula
            # `2*i*j`, where `i` is the line, and `j` is
            # the `j`th number being appended per line
            line.append(2 * i * j)
        # Print the list as a line
        print(" ".join(line))  # type: ignore

if __name__ == "__main__":
    generate_triangle_pattern(2)
    generate_triangle_pattern(5)