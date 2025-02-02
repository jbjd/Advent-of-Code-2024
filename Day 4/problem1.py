"""Given input of a word search puzzle, find how often XMAS appears
it can be in any direction including diagonals"""

character_matrix: list[str] = []

with open("Day 4/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        character_matrix.append(line)

row_count: int = len(character_matrix)
column_count: int = len(character_matrix[0])

xmas_occurrences: int = 0

# L to R or R to L occurrences
for row in character_matrix:
    xmas_occurrences += row.count("XMAS")
    xmas_occurrences += row.count("SAMX")


# Top to Botton or Bottom to Top occurrences
for column_index in range(column_count):
    column: str = "".join(row[column_index] for row in character_matrix)
    xmas_occurrences += column.count("XMAS")
    xmas_occurrences += column.count("SAMX")


# Top Left to Bottom Right Diagonal occurrences
# 0,0 being top left of matrix
diagonal_x_indexes: list[int] = [0] * (row_count - 1) + [i for i in range(column_count)]
diagonal_y_indexes: list[int] = [i for i in range(row_count - 1, 0, -1)] + [
    0
] * column_count

for x, y in zip(diagonal_x_indexes, diagonal_y_indexes):
    diagonal: str = ""

    while True:
        try:
            diagonal += character_matrix[y][x]
            y += 1
            x += 1
        except IndexError:
            break

    xmas_occurrences += diagonal.count("XMAS")
    xmas_occurrences += diagonal.count("SAMX")

# Bottom Left to Top Right Diagonal occurrences
# 0,0 being top left of matrix
diagonal_x_indexes = [0] * (row_count - 1) + [i for i in range(column_count)]
diagonal_y_indexes = [i for i in range(row_count)] + [row_count - 1] * column_count

for x, y in zip(diagonal_x_indexes, diagonal_y_indexes):
    diagonal: str = ""

    while True:
        try:
            diagonal += character_matrix[y][x]
            y -= 1
            x += 1
            if y < 0 or x < 0:
                raise IndexError
        except IndexError:
            break

    xmas_occurrences += diagonal.count("XMAS")
    xmas_occurrences += diagonal.count("SAMX")


# Correct: 2569
print(xmas_occurrences)
