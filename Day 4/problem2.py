"""Given input of a word search puzzle, find how often MAS appears
in an x shape

M.Sd
.A.
M.S

"""

character_matrix: list[str] = []

with open("Day 4/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        character_matrix.append(line)

row_count: int = len(character_matrix)
column_count: int = len(character_matrix[0])

xmas_occurrences: int = 0

# L to R or R to L occurrences
for row_index in range(1, row_count - 1):
    for col_index in range(1, column_count - 1):
        if character_matrix[row_index][col_index] == "A":  # Possible X-MAS here
            top_left: str = character_matrix[row_index - 1][col_index - 1]
            if top_left not in ("M", "S"):
                continue

            bottom_right: str = character_matrix[row_index + 1][col_index + 1]
            if bottom_right not in ("M", "S") or bottom_right == top_left:
                continue

            bottom_left: str = character_matrix[row_index - 1][col_index + 1]
            if bottom_left not in ("M", "S"):
                continue

            top_right: str = character_matrix[row_index + 1][col_index - 1]
            if top_right not in ("M", "S") or bottom_left == top_right:
                continue

            xmas_occurrences += 1

# Correct: 1998
print(xmas_occurrences)
