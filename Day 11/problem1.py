"""Given numbers seperated by a space that represent stones with numbers on them,
apply the first applicable rule of a given set of rules to each stone. Only one rule is
applied to a given stone at a time. The rules apply each time you blink, and you will
blink 25 times. Perserve the order of the stones"""

BLINK_COUNT: int = 25
stones: list[int]

with open("Day 11/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        stones = [int(num) for num in line.split(" ")]


def can_apply_rule1(stone: int) -> bool:
    return stone == 0


def can_apply_rule2(stone: int) -> bool:
    return len(str(stone)) % 2 == 0


for _ in range(BLINK_COUNT):
    new_stones: list[int] = []

    for stone in stones:
        if can_apply_rule1(stone):
            new_stones.append(1)
        elif can_apply_rule2(stone):
            stone_repr = str(stone)
            digits = len(stone_repr)
            left_stone = int(stone_repr[: digits // 2])
            right_stone = int(stone_repr[digits // 2 :])

            new_stones.append(left_stone)
            new_stones.append(right_stone)

        else:
            new_stones.append(stone * 2024)

    stones = new_stones

# Correct: 199946
print(len(stones))
