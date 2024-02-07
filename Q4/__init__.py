def generate_triangle_pattern(n: int) -> list[str]:
    """Generate a list of strings which adhere to
    a specific sort of triangular number pattern

    Args:
        `n` (`int`):
            Number of lines to generate

    Returns:
        `list[str]`:

    """
    
    # Initialize a list to store lines
    lines: list[str] = []

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
            line.append(str(2 * i * j))  # type: ignore[reportGeneralTypeIssues]
        # Append generated line to list
        lines.append(" ".join(line))  # type: ignore[reportGeneralTypeIssues]

    # Return list of lines
    return lines


if __name__ == "__main__":
    for n in (1, 3, 5, 9):
        print(f"{n=}")
        print(*generate_triangle_pattern(n), "\n", sep="\n")
