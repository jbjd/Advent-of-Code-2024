"""Given a string of numbers of even length where the following pattern is represented:
the first number is the blocks of the file and the second is the blocks of free space.
909090 would be three files in a row without space inbetween. files have ids that
correspond to their initial ordering. Reorder the files by moving the rightmost file
to the leftmost space that can accomodate and recalculate the checksum. The checksum is
defined as thesum of all indexes multiplied by the id of the file occupying that block
"""

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


class FileBlock:
    def __init__(self, id: int | None, start_index: int, length: int):
        self.id = id
        self.start_index = start_index
        self.length = length


none_blocks: list[FileBlock] = []
id_blocks: list[FileBlock] = []
last_id: int | None = None
for index, file_id in enumerate(file_layout):
    if file_id is None:
        if not none_blocks or last_id is not None:
            none_blocks.append(FileBlock(None, index, 1))
        else:
            none_blocks[-1].length += 1
    else:
        if not id_blocks or file_id != last_id:
            id_blocks.append(FileBlock(file_id, index, 1))
        else:
            id_blocks[-1].length += 1

    last_id = file_id

id_blocks.reverse()

for id_block in id_blocks:
    none_block_target = next(
        (
            none_block
            for none_block in none_blocks
            if none_block.length >= id_block.length
            and none_block.start_index < id_block.start_index
        ),
        None,
    )
    if none_block_target is None:
        continue

    none_index = none_block_target.start_index
    id_index = id_block.start_index
    for _ in range(id_block.length):
        file_layout[none_index], file_layout[id_index] = (
            file_layout[id_index],
            file_layout[none_index],
        )
        none_index += 1
        id_index += 1

    none_block_target.length -= id_block.length
    none_block_target.start_index += id_block.length


checksum: int = 0

for index, file_id in enumerate(file_layout):
    if file_id is None:
        continue

    checksum += index * file_id

# Correct: 6287317016845
print(checksum)
