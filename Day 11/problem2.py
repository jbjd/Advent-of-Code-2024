"""Given numbers seperated by a space that represent stones with numbers on them,
apply the first applicable rule of a given set of rules to each stone. Only one rule is
applied to a given stone at a time. The rules apply each time you blink, and you will
blink 75 times. Perserve the order of the stones"""

import functools

BLINK_COUNT: int = 35
stones: list[int]

with open("Day 11/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        stones = [int(num) for num in line.split(" ")]


@functools.cache
def visit_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    stone_repr = str(stone)
    digit_count = len(stone_repr)
    if digit_count % 2 == 0:
        return [
            int(stone_repr[: digit_count // 2]),
            int(stone_repr[digit_count // 2 :]),
        ]

    return [stone * 2024]


import time

a = time.perf_counter()
new_stones = []

for stone in stones:
    local_stones = [stone]
    for _ in range(BLINK_COUNT):
        new_local_stones = []
        for local_stone in local_stones:
            new_local_stones += visit_stone(local_stone)

        local_stones = new_local_stones

    new_stones += local_stones
print(time.perf_counter() - a)

# Correct:
print(len(new_stones))
