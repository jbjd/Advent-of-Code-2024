"""Given an input where "^" represent a guard, "#" represents an obstacle and
"." represent where the guard can walk: determine the nunber of unique spaces the guard
can walk on. Assume the guard starts walking upward. Assume guard turns 90 degress
to the right if anything is infront of them, otherwise they will walk forward."""

from enum import Enum

GUARD_ICON: str = "^"
OBSTACLE_ICON: str = "#"


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Guard:
    """Stores information on guard and their patrol area.
    Assumes 0,0 is top left of patrol_area matrix"""

    def __init__(self, patrol_area: list[str], x: int, y: int) -> None:
        self.direction = Direction.UP
        self.patrol_area = patrol_area
        self.x = x
        self.y = y

        self.unique_coords: set[tuple[int, int]] = {(x, y)}

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        return (
            y < 0
            or x < 0
            or y >= len(self.patrol_area)
            or x >= len(self.patrol_area[0])
        )

    def move(self) -> None:
        next_x, next_y = self._next_coords()

        while (
            not self.is_out_of_bounds(next_x, next_y)
            and self.patrol_area[next_y][next_x] == OBSTACLE_ICON
        ):
            self._rotate_90_degrees()
            next_x, next_y = self._next_coords()

        self.x, self.y = next_x, next_y

        if not self.is_out_of_bounds(self.x, self.y):
            coords = (self.x, self.y)
            self.unique_coords.add(coords)

    def _next_coords(self) -> tuple[int, int]:
        match self.direction:
            case Direction.UP:
                return self.x, self.y - 1
            case Direction.RIGHT:
                return self.x + 1, self.y
            case Direction.DOWN:
                return self.x, self.y + 1
            case Direction.LEFT:
                return self.x - 1, self.y
            case _:
                raise Exception("Unreachable")

    def _rotate_90_degrees(self) -> None:
        match self.direction:
            case Direction.UP:
                self.direction = Direction.RIGHT
            case Direction.RIGHT:
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case Direction.LEFT:
                self.direction = Direction.UP
            case _:
                raise Exception("Unreachable")


patrol_area: list[str] = []

with open("Day 6/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        patrol_area.append(line)


def find_guard_start_coords(patrol_area: list[str]) -> tuple[int, int]:
    for y, row in enumerate(patrol_area):
        for x, item in enumerate(row):
            if item == GUARD_ICON:
                return x, y

    raise IndexError("Guard not found")


guard_x, guard_y = find_guard_start_coords(patrol_area)
guard = Guard(patrol_area, guard_x, guard_y)

while not guard.is_out_of_bounds(guard.x, guard.y):
    guard.move()

# Correct: 5269
print(len(guard.unique_coords))
