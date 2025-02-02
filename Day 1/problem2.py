"""Given two lists of numbers, find their similarity score defined as
the value in the left list * the occurrences of that value in the right list"""

left_list: list[int] = []
right_list: list[int] = []

with open("Day 1/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        values: list[str] = line.split("   ")
        left_list.append(int(values[0]))
        right_list.append(int(values[1]))

right_list_occurrences: dict[int, int] = {}
for value in right_list:
    right_list_occurrences[value] = 1 + right_list_occurrences.get(value, 0)

similarity_score: int = 0
for value in left_list:
    similarity_score += value * right_list_occurrences.get(value, 0)

# Correct: 19097157
print(similarity_score)
