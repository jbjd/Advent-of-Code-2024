"""Given an input where each line is in the form "sum: _ _ _" where
the underscores are numbers, check if each sum can be created by using any combindation
of adding or multiplying the numbers. Find all sums that are valid and sum them
together to create a sum of sums"""

from enum import Enum


class Operation(Enum):
    ADD = 0
    MULT = 1


sum_and_values: list[tuple[int, list[int]]] = []
with open("Day 7/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        split_sum_values = line.split(": ")
        sum = int(split_sum_values[0])
        values = [int(v) for v in split_sum_values[1].split(" ")]

        sum_and_values.append((sum, values))


def values_sum_correctly(
    values: list[int],
    index: int,
    running_sum: int,
    target_sum: int,
    operation: Operation,
) -> bool:
    """Recursively trys all variations of adding/multiplying
    values to get to target_sum"""
    if index >= len(values):
        return running_sum == target_sum
    elif index == 0:
        running_sum = values[0]
    else:
        if operation == Operation.ADD:
            running_sum += values[index]
        else:
            running_sum *= values[index]

    if running_sum > target_sum:
        return False
    elif index + 1 >= len(values):
        return running_sum == target_sum

    return values_sum_correctly(
        values, index + 1, running_sum, target_sum, Operation.ADD
    ) or values_sum_correctly(
        values, index + 1, running_sum, target_sum, Operation.MULT
    )


running_sum: int = 0
for sum, values in sum_and_values:
    if values_sum_correctly(values, 0, 0, sum, Operation.ADD):
        running_sum += sum

# Correct: 6231007345478
print(running_sum)
