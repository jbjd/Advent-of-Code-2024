"""Given input page ordering rules in form X|Y where X must come before Y,
an empty line, and a series of comma deliminated numbers representing page numbers
that needs updates: Find series that don't follow the rules, fix them, and sum
the middle value of those series. Assume series are always odd lengths"""

# key values come before all values in list they point to
rules: dict[int, set[int]] = {}
update_page_numbers: list[list[int]] = []

with open("Day 5/input.txt", "r", encoding="utf-8") as fp:
    line: str

    while line := fp.readline().strip():
        rule: list[int] = line.split("|")
        comes_before: int = int(rule[0])
        comes_after: int = int(rule[1])

        if comes_before in rules:
            rules[comes_before].add(comes_after)
        else:
            rules[comes_before] = {comes_after}

    while line := fp.readline().strip():
        page_numbers: list[int] = [int(page) for page in line.split(",")]
        update_page_numbers.append(page_numbers)


def rules_boken_index(page_numbers: list[int]) -> int:
    page_numbers_before: set[int] = set()

    for i, page_number in enumerate(page_numbers):
        page_numbers_before.add(page_number)

        if page_number not in rules:
            continue

        must_come_after: set[int] = rules[page_number]
        rule_broken: bool = len(page_numbers_before.intersection(must_come_after)) > 0
        if rule_broken:
            return i

    return -1


middle_page_sum: int = 0

for page_numbers in update_page_numbers:
    if rules_boken_index(page_numbers) == -1:
        continue

    corrected_page_numbers: list[int] = page_numbers

    # This effectively bubble sorts by moving values that break the rules
    # one index in negative direction
    while (i := rules_boken_index(page_numbers)) != -1:
        corrected_page_numbers[i - 1], corrected_page_numbers[i] = (
            corrected_page_numbers[i],
            corrected_page_numbers[i - 1],
        )

    middle_page_sum += corrected_page_numbers[len(corrected_page_numbers) // 2]


# Correct: 6456
print(middle_page_sum)
