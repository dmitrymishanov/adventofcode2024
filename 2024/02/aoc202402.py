"""AoC 2, 2024."""

import pathlib
import sys
from dataclasses import dataclass, field


@dataclass
class Data:
    reports: list[list[int]] = field(default_factory=list)


def parse_data(puzzle_input: str) -> Data:
    data = Data(
        reports=[list(map(int, report.split())) for report in puzzle_input.split("\n")]
        if puzzle_input
        else []
    )
    return data


def part1(data: Data) -> int:
    safe_reports = 0
    for report in data.reports:
        decr = report[0] > report[1]
        if is_safe(report, decr):
            safe_reports += 1

    return safe_reports


def is_decreasing(report: list[int]) -> bool:
    """Определение направления с учетом 1 погрешности"""
    return (
        (report[0] > report[1]) + (report[1] > report[2]) + (report[2] > report[3])
    ) >= 2


def is_safe(report: list[int], decr: bool) -> bool:
    decr = is_decreasing(report)
    for i in range(len(report) - 1):
        diff = (report[i] - report[i + 1]) if decr else (report[i + 1] - report[i])
        if diff < 1 or diff > 3:
            return False
    return True


def part2(data: Data) -> int:
    safe_reports = 0
    for report in data.reports:
        decr = is_decreasing(report)
        if any(is_safe(report[:i] + report[i + 1 :], decr) for i in range(len(report))):
            safe_reports += 1

    return safe_reports


def solve(puzzle_input):
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
