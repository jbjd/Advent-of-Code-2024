"""Given streams of numbers representing levels in a report, determine if the
report is safe. Safe is defined as the levels strictly increasing or decreasing
and by 3 at most.

Include a dampener, which dampens one level of a Report if needed. This treats that
level as if it were not there"""


class Report:
    def __init__(self, report_input: str) -> None:
        # levels must be len > 0
        self.levels: list[int] = [int(level) for level in report_input.split(" ")]

    def __str__(self) -> str:
        return str(self.levels)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def _is_safe_single_direction(
        levels, increasing: bool, dampened_index: int = -1
    ) -> tuple[bool, int]:
        """Returns tuple of if its safe and index of issue if any"""
        previous_level: int
        current_level: int

        previous_level = levels[0 if dampened_index != 0 else 1]
        for i in range(1 if dampened_index != 0 else 2, len(levels)):
            if i == dampened_index:
                continue

            current_level = levels[i]

            is_safe: bool = (
                (
                    current_level > previous_level
                    and not current_level - 3 > previous_level
                )
                if increasing
                else (
                    current_level < previous_level
                    and not current_level + 3 < previous_level
                )
            )

            if not is_safe:
                return False, i

            previous_level = current_level

        return True, -1

    def is_safe(self, levels: list[int]) -> bool:
        """Levels are safe if they strictly increase/decrease by at least
        one and at most 3. Ignored dampened_index if passed"""
        return (
            self._is_safe_single_direction(levels, increasing=True)[0]
            or self._is_safe_single_direction(levels, increasing=False)[0]
        )

    def is_safe_with_dampener(self) -> bool:
        """Levels are safe if they strictly increase/decrease by at least
        one and at most 3. One bad level is tolerated aka if its not safe but
        would be if one level was removed, it is safe."""

        # This is structured weirdly for some optimization
        # A slower but more simple approach would be to check all variations of
        # self.levels with a single value missing, but only the index where the issue
        # first occured the two before that need to be checked.
        # Technically, this is now O(n) rather than O(n^2)
        increasing_safely: bool
        decreasing_safely: bool

        increasing_safely, problem_index_when_increasing = (
            self._is_safe_single_direction(self.levels, increasing=True)
        )
        if increasing_safely:
            return True

        decreasing_safely, problem_index_when_decreasing = (
            self._is_safe_single_direction(self.levels, increasing=False)
        )
        if decreasing_safely:
            return True

        # This is where dampening kicks in
        increasing_safely = (
            self._is_safe_single_direction(
                self.levels,
                increasing=True,
                dampened_index=problem_index_when_increasing,
            )[0]
            or self._is_safe_single_direction(
                self.levels,
                increasing=True,
                dampened_index=problem_index_when_increasing - 1,
            )[0]
            or self._is_safe_single_direction(
                self.levels,
                increasing=True,
                dampened_index=problem_index_when_increasing - 2,
            )[0]
        )
        if increasing_safely:
            return True

        decreasing_safely = (
            self._is_safe_single_direction(
                self.levels,
                increasing=False,
                dampened_index=problem_index_when_decreasing,
            )[0]
            or self._is_safe_single_direction(
                self.levels,
                increasing=False,
                dampened_index=problem_index_when_decreasing - 1,
            )[0]
            or self._is_safe_single_direction(
                self.levels,
                increasing=False,
                dampened_index=problem_index_when_decreasing - 2,
            )[0]
        )
        if decreasing_safely:
            return True

        return False


reports: list[Report] = []


with open("Day 2/input.txt", "r", encoding="utf-8") as fp:
    line: str
    while line := fp.readline().strip():
        reports.append(Report(line))

safe_reports_count: int = 0
for report in reports:
    safe_reports_count += report.is_safe_with_dampener()

# Correct: 328
print(safe_reports_count)
