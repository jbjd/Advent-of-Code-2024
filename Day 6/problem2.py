"""Given an input where "^" represent a guard, "#" represents an obstacle and
"." represent where the guard can walk: determine the nunber of unique spaces the guard
can walk on. Assume the guard starts walking upward. Assume guard turns 90 degress
to the right if anything is infront of them, otherwise they will walk forward."""

from enum import Enum

GUARD_ICON: str = "^"
OBSTACLE_ICON: str = "#"
WALKED_ON_ICON: str = "X"
EMPTY_ICON: str = "."


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class GuardMoveState:
    CAN_MOVE = 0
    IN_LOOP = 1
    OUT_OF_BOUNDS = 2


class Guard:
    """Stores information on guard and their patrol area.
    Assumes 0,0 is top left of patrol_area matrix"""

    def __init__(
        self, patrol_area: list[str], x: int, y: int, label_path: bool = False
    ) -> None:
        self.direction = Direction.UP
        self.patrol_area = patrol_area
        self.x = x
        self.y = y
        self.label_path = label_path

        if label_path:
            self.patrol_area[y][x] = WALKED_ON_ICON
        self.unique_coords: set[tuple[int, int]] = {(x, y)}
        self.history: set[tuple[int, int, Direction]] = set()

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        return (
            y < 0
            or x < 0
            or y >= len(self.patrol_area)
            or x >= len(self.patrol_area[0])
        )

    def is_in_loop(self) -> bool:
        coords_and_dir = (self.x, self.y, self.direction)

        return coords_and_dir in self.history

    def move_and_see_if_terminal(self) -> GuardMoveState:
        next_x, next_y = self._next_coords()

        while (
            not self.is_out_of_bounds(next_x, next_y)
            and self.patrol_area[next_y][next_x] == OBSTACLE_ICON
        ):
            self._rotate_90_degrees()
            next_x, next_y = self._next_coords()

        self.x, self.y = next_x, next_y
        in_loop: bool = self.is_in_loop()
        out_of_bounds: bool = self.is_out_of_bounds(self.x, self.y)

        if not out_of_bounds:
            if self.label_path:
                self.patrol_area[self.y][self.x] = WALKED_ON_ICON
            coords = (self.x, self.y)
            self.unique_coords.add(coords)
            self.history.add((self.x, self.y, self.direction))

        if in_loop:
            return GuardMoveState.IN_LOOP
        elif out_of_bounds:
            return GuardMoveState.OUT_OF_BOUNDS
        else:
            return GuardMoveState.CAN_MOVE

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


patrol_area: list[list[str]] = []

with open("Day 6/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        patrol_area.append([char for char in line])


def find_guard_start_coords(patrol_area: list[str]) -> tuple[int, int]:
    for y, row in enumerate(patrol_area):
        for x, item in enumerate(row):
            if item == GUARD_ICON:
                return x, y

    raise IndexError("Guard not found")


guard_x, guard_y = find_guard_start_coords(patrol_area)

# Solve once and label path so we only check those
guard = Guard(patrol_area, guard_x, guard_y, label_path=True)

state: GuardMoveState = guard.move_and_see_if_terminal()
while state == GuardMoveState.CAN_MOVE:
    state = guard.move_and_see_if_terminal()

# Generate all variations of adding an obstacle to the patrol area
# and see if they generate loops
loop_count: int = 0
previous_coords: tuple[int, int] | None = None
for x in range(len(patrol_area)):
    for y in range(len(patrol_area[0])):
        current_icon = patrol_area[y][x]
        if current_icon != WALKED_ON_ICON:
            continue

        if previous_coords is not None:
            patrol_area[previous_coords[1]][previous_coords[0]] = EMPTY_ICON

        previous_coords = (x, y)

        patrol_area[y][x] = OBSTACLE_ICON

        guard = Guard(patrol_area, guard_x, guard_y)

        state: GuardMoveState = guard.move_and_see_if_terminal()
        while state == GuardMoveState.CAN_MOVE:
            state = guard.move_and_see_if_terminal()

        if state == GuardMoveState.IN_LOOP:
            loop_count += 1

# Correct: 1957
# There is a more optimal solution here, this one is O(n) but still ran slow.
# Every spot on the path does not need to be checked, only ones where we turn
# and are then on the path we originally walked on. Infact, solving the whole
# path again was unnecessary as I should only need to check for if placing
# the obstacle would cause a right turn such that we are now in a position
# that the original path took (same direction / coords). Implementing that should
# save a lot of time, but this worked for now.
print(loop_count)
