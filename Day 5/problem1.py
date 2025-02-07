"""Given input page ordering rules in form X|Y where X must come before Y,
an empty line, and a series of comma deliminated numbers representing page numbers
that needs updates: Find series that follow the rules and sum the middle value of
the series. Assume series are always odd lengths"""

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


middle_page_sum: int = 0

for page_numbers in update_page_numbers:
    page_numbers_before: set[int] = set()

    follows_the_rules: bool = True
    for page_number in page_numbers:
        page_numbers_before.add(page_number)

        if page_number not in rules:
            continue

        must_come_after: set[int] = rules[page_number]
        rule_broken: bool = len(page_numbers_before.intersection(must_come_after)) > 0
        if rule_broken:
            follows_the_rules = False
            break

    if follows_the_rules:
        middle_page_sum += page_numbers[len(page_numbers) // 2]


# Correct: 4569
print(middle_page_sum)
