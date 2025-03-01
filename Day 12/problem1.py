"""Given an input of letters, find all regions formed by the letters where
adjacent, identical letters form a region. If there are no matching bordering letters,
the region is jsut the letter itself. Mulitple each region's area by its perimeter
to get the cost to fence it. Find the total cost to fence everything.
"""

map: list[list[str]] = []

with open("Day 12/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        map.append([letter for letter in line])

map_width: int = len(map[0])
map_height: int = len(map)

visited_coords: set[tuple[int, int]] = set()
regions: list[set[tuple[int, int]]] = []


def find_region(
    x: int, y: int, expected_letter: str, visited_coords: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    coords = (x, y)
    visited_coords.add(coords)

    if x < 0 or y < 0 or x >= map_width or y >= map_height:
        return set()

    letter: str = map[y][x]
    if letter != expected_letter:
        return set()

    region: set[tuple[int, int]] = {coords}

    if (x - 1, y) not in visited_coords:
        region = region.union(find_region(x - 1, y, expected_letter, visited_coords))
    if (x + 1, y) not in visited_coords:
        region = region.union(find_region(x + 1, y, expected_letter, visited_coords))
    if (x, y - 1) not in visited_coords:
        region = region.union(find_region(x, y - 1, expected_letter, visited_coords))
    if (x, y + 1) not in visited_coords:
        region = region.union(find_region(x, y + 1, expected_letter, visited_coords))

    return region


def find_perimeter(region: set[tuple[int, int]]) -> int:
    perimeter: int = 0

    for x, y in region:
        sides: int = 4

        if (x - 1, y) in region and x >= 0:
            sides -= 1
        if (x + 1, y) in region and x + 1 < map_width:
            sides -= 1
        if (x, y - 1) in region and y >= 0:
            sides -= 1
        if (x, y + 1) in region and y < map_height:
            sides -= 1

        perimeter += sides

    return perimeter


total_fence_cost: int = 0

for x in range(map_width):
    for y in range(map_height):
        if (x, y) in visited_coords:
            continue

        letter: str = map[y][x]
        region: set[tuple[int, int]] = find_region(x, y, letter, set())
        visited_coords = visited_coords.union(region)

        area: int = len(region)
        perimeter: int = find_perimeter(region)
        total_fence_cost += area * perimeter

# Correct: 1371306
print(total_fence_cost)
