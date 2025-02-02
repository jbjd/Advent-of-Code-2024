"""Given two lists of numbers, find their difference defined as
the difference between the lowest pair plus the next lowest pair and so on"""

left_list: list[int] = []
right_list: list[int] = []

with open("Day 1/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        values: list[str] = line.split("   ")
        left_list.append(int(values[0]))
        right_list.append(int(values[1]))

left_list.sort()
right_list.sort()

total_difference = 0
for v1, v2 in zip(left_list, right_list):
    total_difference += abs(v1 - v2)

# Correct: 2113135
print(total_difference)
