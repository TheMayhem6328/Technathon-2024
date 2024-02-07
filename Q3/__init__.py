def calc_color() -> int:
    """Takes input from user and returns the number of boxes
    required to color it in a way that it makes a star

    Returns:
        `int`:
            Number of boxes to color
    """

    while True:
        # Take input
        values = input("Enter two integers in the form `n m`: ")
        # Integer conversion, unpacking, and type check
        try:
            n, m = tuple(map(int, values.split(" ")))
        except ValueError:
            continue

        # Range check
        if n not in range(1, 1_000_000_001):
            continue
        if m not in range(1, 1_000_000_001):
            continue

        # If all checks pass, break out of loop
        break

    # Return amount of boxes to color
    return min(n, m) * 4 - 3

if __name__ == "__main__":
    print("Boxes to color: ", calc_color())
