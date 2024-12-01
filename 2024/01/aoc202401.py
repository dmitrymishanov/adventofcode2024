"""AoC 1, 2024."""

import pathlib
import sys
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Data:
    left_column: list[int] = field(default_factory=list)
    right_column: list[int] = field(default_factory=list)


def parse_data(puzzle_input: str) -> Data:
    data = Data()
    if not puzzle_input:
        return data
    for pair in puzzle_input.split("\n"):
        left, right = pair.split()
        data.left_column.append(int(left))
        data.right_column.append(int(right))
    return data


def part1(data: Data) -> int:
    data.left_column.sort()
    data.right_column.sort()

    distance = 0
    for left, right in zip(data.left_column, data.right_column):
        distance += abs(abs(left) - abs(right))
    return distance


def part2(data: Data) -> int:
    score = 0
    counter = Counter(data.right_column)
    for value in data.left_column:
        score += value * counter[value]
    return score


def solve(puzzle_input):
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
