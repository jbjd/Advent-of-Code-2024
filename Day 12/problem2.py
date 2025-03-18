"""Given an input of letters, find all regions formed by the letters where
adjacent, identical letters form a region. If there are no matching bordering letters,
the region is jsut the letter itself. Mulitple each region's area by its sides
to get the cost to fence it. Find the total cost to fence everything.
"""

from enum import Enum


class Direction(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"


map: list[list[str]] = []

with open("Day 12/input_small.txt", "r", encoding="utf-8") as fp:
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


def get_coord_on_right(coord, direction):
    x, y = coord

    if direction == Direction.RIGHT:
        y += 1
    elif direction == Direction.DOWN:
        x -= 1
    elif direction == Direction.LEFT:
        y -= 1
    elif direction == Direction.UP:
        x += 1
    else:
        assert False

    return (x, y)


def get_next_coord(coord, direction):
    x, y = coord

    if direction == Direction.RIGHT:
        x += 1
    elif direction == Direction.DOWN:
        y += 1
    elif direction == Direction.LEFT:
        x -= 1
    elif direction == Direction.UP:
        y -= 1
    else:
        assert False

    return (x, y)


def turn_right(direction: Direction) -> Direction:
    if direction == Direction.RIGHT:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.LEFT
    elif direction == Direction.LEFT:
        return Direction.UP
    elif direction == Direction.UP:
        return Direction.RIGHT
    else:
        assert False


def turn_left(direction: Direction) -> Direction:
    if direction == Direction.RIGHT:
        return Direction.UP
    elif direction == Direction.DOWN:
        return Direction.RIGHT
    elif direction == Direction.LEFT:
        return Direction.DOWN
    elif direction == Direction.UP:
        return Direction.LEFT
    else:
        assert False


def recurse_around_sides(
    coord,
    direction,
    starting_coord,
    starting_direction,
    region,
    running_total: int = 0,
    start: bool = False,
) -> int:
    if not start and coord == starting_coord and direction == starting_direction:
        return running_total

    next_coord = get_next_coord(coord, direction)
    if next_coord in region:
        direction = turn_left(direction)
        return recurse_around_sides(
            coord,
            direction,
            starting_coord,
            starting_direction,
            region,
            running_total + 1,
        )
    elif get_coord_on_right(next_coord, direction) not in region:
        direction = turn_right(direction)
        return recurse_around_sides(
            next_coord,
            direction,
            starting_coord,
            starting_direction,
            region,
            running_total + 1,
        )
    else:
        return recurse_around_sides(
            next_coord,
            direction,
            starting_coord,
            starting_direction,
            region,
            running_total,
        )


def find_side_count(region: set[tuple[int, int]]) -> int:
    # Find top left corner
    lowest_y = float("inf")

    for _, y in region:
        if y < lowest_y:
            lowest_y = y

    possible_lowest_coords = {coords for coords in region if coords[1] == lowest_y}

    lowest_coord = (float("inf"), lowest_y)
    for coord in possible_lowest_coords:
        if coord[0] < lowest_coord[0]:
            lowest_coord = coord

    top_left = (lowest_coord[0] - 1, lowest_coord[1] - 1)

    return recurse_around_sides(
        top_left, Direction.RIGHT, top_left, Direction.RIGHT, region, start=True
    )


total_fence_cost: int = 0

for x in range(map_width):
    for y in range(map_height):
        if (x, y) in visited_coords:
            continue

        letter: str = map[y][x]
        region: set[tuple[int, int]] = find_region(x, y, letter, set())
        visited_coords = visited_coords.union(region)

        area: int = len(region)
        side_count: int = find_side_count(region)
        total_fence_cost += area * side_count
        print(letter, f"{area:2} * {side_count:2} = {area * side_count:4}")

print(total_fence_cost)
