"""Given a string of numbers of even length where the following pattern is represented:
the first number is the blocks of the file and the second is the blocks of free space.
909090 would be three files in a row without space inbetween. files have ids that
correspond to their initial ordering. Reorder the files by moving the rightmost blocks
to the leftmost position and recalculate the checksum. The checksum is defined as the
sum of all indexes multiplied by the id of the file occupying that block"""

file_layout: list[int | None] = []
id: int = 0

with open("Day 9/input.txt", "r", encoding="utf-8") as fp:
    line: str = fp.readline().strip()

# Turn the input into a representation of the files where None is an empty space
is_file_blocks: bool = True
for char in line:
    blocks: int = int(char)

    if is_file_blocks:
        if blocks > 0:
            for _ in range(blocks):
                file_layout.append(id)
            id += 1
    else:
        for _ in range(blocks):
            file_layout.append(None)

    is_file_blocks = not is_file_blocks


def indexes_are_still_valid(
    leftmost_none_index: int, rightmost_file_index: int
) -> bool:
    return (
        leftmost_none_index >= 0
        and rightmost_file_index >= 0
        and rightmost_file_index > leftmost_none_index
    )


# Shift rightmost file blocks to leftmost position
leftmost_none_index: int = file_layout.index(None)
rightmost_file_index: int = len(file_layout) - 1
while rightmost_file_index >= 0 and file_layout[rightmost_file_index] is None:
    rightmost_file_index -= 1

while indexes_are_still_valid(leftmost_none_index, rightmost_file_index):
    file_layout[leftmost_none_index], file_layout[rightmost_file_index] = (
        file_layout[rightmost_file_index],
        file_layout[leftmost_none_index],
    )

    while (
        leftmost_none_index < len(file_layout)
        and file_layout[leftmost_none_index] is not None
    ):
        leftmost_none_index += 1

    while rightmost_file_index >= 0 and file_layout[rightmost_file_index] is None:
        rightmost_file_index -= 1

checksum: int = 0

for index, file_id in enumerate(file_layout):
    if file_id is None:
        break

    checksum += index * file_id

# Correct: 6262891638328
print(checksum)
