"""AoC 3, 2024."""

import pathlib
import re
import sys


def part1(puzzle_input: str) -> int:
    env = {"result": 0, "mul": lambda a, b: a * b}
    for op in re.findall("(mul\(\d{1,3}\,\d{1,3}\))", puzzle_input):
        exec(f"result += {op}", env)
    return env["result"]


def part2(puzzle_input: str) -> int:
    env = {"result": 0, "mul": lambda a, b: a * b}
    enabled = True
    for op in re.findall("(mul\(\d{1,3}\,\d{1,3}\)|do\(\)|don't\(\))", puzzle_input):
        if op == "do()":
            enabled = True
        elif op == "don't()":
            enabled = False

        if enabled and op.startswith("mul"):
            exec(f"result += {op}", env)

    return env["result"]


def solve(puzzle_input):
    yield part1(puzzle_input)
    yield part2(puzzle_input)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
