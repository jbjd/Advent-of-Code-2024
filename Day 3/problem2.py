"""Input has garbled data, parse out text matching mul(___,___) where ___ is a numeric
value up to three digits long. Do the multiplicatison and sum results.

Now there is also do() and don't() which enable and disable mul()
"""


def perform_mul_call(possible_mul_call: str) -> int:
    """Given a possible call to mul with starting 'mul(' stripped,
    parses values and performs multiplication. Raises ValueError
    if formatted incorrectly"""

    first_number: int
    second_number: int

    # First char must be numeric
    if not possible_mul_call[0:1].isnumeric():
        raise ValueError

    index: int = 1

    # Next two optionally are numeric
    if possible_mul_call[1:2].isnumeric():
        index += 1
        if possible_mul_call[2:3].isnumeric():
            index += 1

    first_number = int(possible_mul_call[0:index])

    # After first number, must be a comma
    if possible_mul_call[index : index + 1] != ",":
        raise ValueError
    index += 1

    second_number_start_index: int = index

    # Second number starts, must be numeric
    if not possible_mul_call[index : index + 1].isnumeric():
        raise ValueError
    index += 1

    # Next two optionally are numeric
    if possible_mul_call[index : index + 1].isnumeric():
        index += 1
        if possible_mul_call[index : index + 1].isnumeric():
            index += 1

    second_number = int(possible_mul_call[second_number_start_index:index])

    if possible_mul_call[index : index + 1] != ")":
        raise ValueError

    return first_number * second_number


with open("Day 3/input.txt", "r", encoding="utf-8") as fp:
    program: str = fp.read()

PROGRAM_LENGTH = len(program)

mul_sum: int = 0
index: int = 0
mul_enabled: bool = True
while index < PROGRAM_LENGTH:
    first_four: str = program[index : index + 4]
    if first_four == "do()":
        mul_enabled = True
        index += 4
        continue
    elif first_four == "don'":
        if program[index + 4 : index + 7] == "t()":
            index += 7
            mul_enabled = False
        else:
            index += 4
        continue
    elif mul_enabled and first_four == "mul(":
        # Values can be 1-3 long so max length following mul(
        # is 8 mul(___,___)
        possible_mul_call: str = program[index + 4 : index + 12]
        try:
            mul_sum += perform_mul_call(possible_mul_call)
            index += 8  # 8 is minimum size mul(_,_)
        except ValueError:
            index += 4
        continue
    index += 1

# Correct: 82045421
print(mul_sum)
