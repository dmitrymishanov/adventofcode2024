"""AoC 7, 2024."""

import pathlib
import sys
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Equation:
    test_value: int
    numbers: list[int]


def parse_input(puzzle_input: str) -> list[Equation]:
    data = []
    for line in puzzle_input.split("\n"):
        test_value, numbers = line.split(":")
        data.append(
            Equation(
                test_value=int(test_value),
                numbers=[int(n) for n in numbers.strip().split(" ")],
            )
        )

    return data


def is_valid_equation(
    equation: Equation,
    apply_operators: Callable[[int, int], set[int]],
) -> bool:
    numbers = equation.numbers
    solutions_space = {numbers[0]}
    for number in numbers[1:]:
        new_solutions_space = set()
        for s in solutions_space:
            if s > equation.test_value:
                continue
            new_solutions_space.update(apply_operators(s, number))
        solutions_space = new_solutions_space
    return equation.test_value in solutions_space


def apply_operators1(value1: int, value2: int) -> set[int]:
    return {value1 + value2, value1 * value2}


def check_equations(
    equations: list[Equation],
    apply_operators: Callable[[int, int], set[int]],
) -> int:
    result = 0
    for equation in equations:
        if is_valid_equation(equation, apply_operators):
            result += equation.test_value
    return result


def part1(equations: list[Equation]) -> int:
    return check_equations(equations, apply_operators1)


def apply_operators2(value1: int, value2: int) -> set[int]:
    return {value1 + value2, value1 * value2, int(str(value1) + str(value2))}


def part2(equations: list[Equation]) -> int:
    return check_equations(equations, apply_operators2)


def solve(puzzle_input):
    data = parse_input(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
