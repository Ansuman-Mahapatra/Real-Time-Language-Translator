rows = 4

for i in range(rows):
    # Print leading spaces (each space is actually two to align nicely)
    for j in range(rows - i - 1):
        print(" ", end="")

    # Print ascending characters
    for j in range(i + 1):
        print(chr(65 + j), end="")

    # Print descending characters
    for j in range(i - 1, -1, -1):
        print(chr(65 + j), end="")

    # Move to the next line
    print()
