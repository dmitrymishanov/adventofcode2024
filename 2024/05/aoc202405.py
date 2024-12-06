"""AoC 5, 2024."""

import pathlib
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cmp_to_key


@dataclass
class Data:
    rules: dict[int, set[int]] = field(default_factory=lambda: defaultdict(set))
    updates: list[list[int]] = field(default_factory=list)


def parse_input(puzzle_input: str) -> Data:
    data = Data()
    for line in puzzle_input.split("\n"):
        if "|" in line:
            first, second = map(int, line.split("|"))
            data.rules[first].add(second)
        elif line:
            data.updates.append(list(map(int, line.split(","))))
    return data


def is_correct(update: list[int], rules: dict[int, set[int]]) -> bool:
    visited = set()
    for item in update:
        if rules[item].intersection(visited):
            return False
        visited.add(item)
    return True


def part1(data: Data) -> int:
    result = 0

    for update in data.updates:
        if is_correct(update, data.rules):
            result += update[len(update) // 2]

    return result


def part2(data: Data) -> int:
    result = 0

    def compare(a: int, b: int) -> int:
        if b in data.rules[a]:
            return 1
        if a in data.rules[b]:
            return -1
        return 0

    for update in data.updates:
        if not is_correct(update, data.rules):
            update.sort(key=cmp_to_key(compare))
            result += update[len(update) // 2]

    return result


def solve(puzzle_input):
    data = parse_input(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
