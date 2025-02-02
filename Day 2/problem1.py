"""Given streams of numbers representing levels in a report, determine if the
report is safe. Safe is defined as the levels strictly increasing or decreasing
and by 3 at most"""


class Report:
    def __init__(self, report_input: str) -> None:
        self.levels: list[int] = [int(level) for level in report_input.split(" ")]

    def __str__(self) -> str:
        return str(self.levels)

    def __repr__(self) -> str:
        return str(self)

    def is_safe(self) -> bool:
        """Levels are safe if they strictly increase/decrease by at least
        one and at most 3"""
        return all(
            self.levels[i] > self.levels[i - 1]
            and not self.levels[i] - 3 > self.levels[i - 1]
            for i in range(1, len(self.levels))
        ) or all(
            self.levels[i] < self.levels[i - 1]
            and not self.levels[i] + 3 < self.levels[i - 1]
            for i in range(1, len(self.levels))
        )


reports: list[Report] = []


with open("Day 2/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        reports.append(Report(line))

safe_reports: int = 0
for report in reports:
    safe_reports += report.is_safe()

# Correct: 257
print(safe_reports)
