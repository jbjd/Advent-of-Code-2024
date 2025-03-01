"""Given numbers seperated by a space that represent stones with numbers on them,
apply the first applicable rule of a given set of rules to each stone. Only one rule is
applied to a given stone at a time. The rules apply each time you blink, and you will
blink 75 times. Perserve the order of the stones"""

BLINK_COUNT: int = 75
stones: list[int]

with open("Day 11/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        stones = [int(num) for num in line.split(" ")]

stone_count_cache: dict[tuple[int, int], int] = {}


def get_stone_count_after_blinks(stone: int, remaining_blinks: int) -> int:
    cache_key: tuple[int, int] = (stone, remaining_blinks)
    if cache_key in stone_count_cache:
        return stone_count_cache[cache_key]

    if remaining_blinks == 0:
        return 1

    remaining_blinks -= 1
    total_stones: int = 0

    if stone == 0:
        total_stones = get_stone_count_after_blinks(1, remaining_blinks)
    else:
        stone_repr = str(stone)
        digit_count: int = len(stone_repr)

        if digit_count % 2 == 0:
            left_stone = int(stone_repr[: digit_count // 2])
            right_stone = int(stone_repr[digit_count // 2 :])
            total_stones = get_stone_count_after_blinks(
                left_stone, remaining_blinks
            ) + get_stone_count_after_blinks(right_stone, remaining_blinks)
        else:
            total_stones = get_stone_count_after_blinks(stone * 2024, remaining_blinks)

    stone_count_cache[cache_key] = total_stones
    return total_stones


total_stones = 0

for stone in stones:
    total_stones += get_stone_count_after_blinks(stone, BLINK_COUNT)

# Correct: 237994815702032
print(total_stones)
