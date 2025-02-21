"""Given a square topographic map with numbers ranging from 0-9 representing the height,
find the score of all trailheads. A trailhead is a path from 0 to 9 increasing by 1 each
step where steps are orthogonal, never diagonal. A trailhead is scored by the number of
9s it reachs. Find the total sum of the trailheads"""

topographic_map: list[list[int]] = []


with open("Day 10/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        topographic_map.append([int(c) if c.isnumeric() else -1 for c in line])

max_y: int = len(topographic_map)
max_x: int = len(topographic_map[0])


def find_unique_mountain_heads(
    x: int, y: int, expected_elevation: int
) -> set[tuple[int, int]]:
    if expected_elevation < 0 or expected_elevation > 9:
        raise ValueError("Invalid Elevation Expected")

    mountain_heads: set[tuple[int, int]] = set()

    if x < 0 or y < 0 or x >= max_x or y >= max_y:
        return mountain_heads

    elevation: int = topographic_map[y][x]
    if elevation != expected_elevation:
        return mountain_heads

    if elevation == 9:
        coords: tuple[int, int] = (x, y)
        mountain_heads.add(coords)
        return mountain_heads

    expected_elevation += 1

    above_result = find_unique_mountain_heads(x, y - 1, expected_elevation)
    below_result = find_unique_mountain_heads(x, y + 1, expected_elevation)
    right_result = find_unique_mountain_heads(x + 1, y, expected_elevation)
    left_result = find_unique_mountain_heads(x - 1, y, expected_elevation)

    mountain_heads = mountain_heads.union(above_result)
    mountain_heads = mountain_heads.union(below_result)
    mountain_heads = mountain_heads.union(right_result)
    mountain_heads = mountain_heads.union(left_result)

    return mountain_heads


total_score: int = 0

for y, row in enumerate(topographic_map):
    for x, elevation in enumerate(row):
        if elevation == 0:
            score: int = len(find_unique_mountain_heads(x, y, 0))
            total_score += score

# Correct: 746
print(total_score)
