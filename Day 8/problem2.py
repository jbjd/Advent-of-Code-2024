"""Given a map where alphanumeric values represent antennas, find the number
of unique locations that have antinodes placed. An antinodes can be placed on
any spot where they are perfectly inline with antennas of the same frequency
including spots that already have antenna and themselves."""

EMPTY_SPOT_ICON: str = "."

antenna_to_coords: dict[str, list[tuple[int, int]]] = {}
y_size: int = 0
x_size: int = 0

with open("Day 8/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        for x_size, char in enumerate(line):
            if char != EMPTY_SPOT_ICON:
                if char not in antenna_to_coords:
                    antenna_to_coords[char] = [(x_size, y_size)]
                else:
                    antenna_to_coords[char].append((x_size, y_size))

        y_size += 1
        x_size = len(line)

already_occupied_coords: set[tuple[int, int]] = set()
for coords_iter in antenna_to_coords.values():
    for coords in coords_iter:
        already_occupied_coords.add(coords)


def coords_in_bounds(coords: tuple[int, int]) -> bool:
    x, y = coords

    return x >= 0 and y >= 0 and x < x_size and y < y_size


antinode_coords: set[tuple[int, int]] = set()

for antenna, coords_iter in antenna_to_coords.items():
    if len(coords_iter) < 2:
        continue

    for i in range(len(coords_iter)):
        for j in range(i + 1, len(coords_iter)):
            root_coords = coords_iter[i]
            other_antenna_coords = coords_iter[j]

            x_diff, y_diff = (
                root_coords[0] - other_antenna_coords[0],
                root_coords[1] - other_antenna_coords[1],
            )

            for direction in (1, -1):
                possible_coords = (
                    root_coords[0] + x_diff * direction,
                    root_coords[1] + y_diff * direction,
                )
                while coords_in_bounds(possible_coords):
                    antinode_coords.add(possible_coords)
                    possible_coords = (
                        possible_coords[0] + x_diff * direction,
                        possible_coords[1] + y_diff * direction,
                    )

# Special case: add antenna's own coords if at least 2 are present
for coords_iter in antenna_to_coords.values():
    if len(coords_iter) > 1:
        for coords in coords_iter:
            antinode_coords.add(coords)


# Correct: 1259
print(len(antinode_coords))
