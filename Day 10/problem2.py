"""Given a square topographic map with numbers ranging from 0-9 representing the height,
find the score of all trailheads. A trailhead is a path from 0 to 9 increasing by 1 each
step where steps are orthogonal, never diagonal. A trailhead is scored by the number of
unique paths to a 9 it reachs. Find the total sum of the trailheads"""

topographic_map: list[list[int]] = []


with open("Day 10/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        topographic_map.append([int(c) if c.isnumeric() else -1 for c in line])

max_y: int = len(topographic_map)
max_x: int = len(topographic_map[0])


def find_score_of_trailhead(x: int, y: int, expected_elevation: int) -> int:
    if expected_elevation < 0 or expected_elevation > 9:
        raise ValueError("Invalid Elevation Expected")

    if x < 0 or y < 0 or x >= max_x or y >= max_y:
        return 0

    elevation: int = topographic_map[y][x]
    if elevation != expected_elevation:
        return 0

    if elevation == 9:
        return 1

    expected_elevation += 1
    total_score: int = 0

    total_score += find_score_of_trailhead(x, y - 1, expected_elevation)
    total_score += find_score_of_trailhead(x, y + 1, expected_elevation)
    total_score += find_score_of_trailhead(x + 1, y, expected_elevation)
    total_score += find_score_of_trailhead(x - 1, y, expected_elevation)

    return total_score


total_score: int = 0

for y, row in enumerate(topographic_map):
    for x, elevation in enumerate(row):
        if elevation == 0:
            score: int = find_score_of_trailhead(x, y, 0)
            total_score += score

# Correct:
print(total_score)
