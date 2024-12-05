"""AoC 4, 2024."""

import pathlib
import sys

ORDER = {
    "X": "M",
    "M": "A",
    "A": "S",
    "S": None,
}


def parse_input(puzzle_input: str) -> list[list[str]]:
    return [list(row) for row in puzzle_input.split("\n")]


def observe(
    *,
    matrix: list[list[str]],
    i: int,
    j: int,
    value: str,
    direction_i: int,
    direction_j: int,
) -> int:
    if (
        i < 0
        or j < 0
        or i >= len(matrix)
        or j >= len(matrix[0])
        or matrix[i][j] != value
    ):
        return 0
    next_value = ORDER[value]
    if next_value is None:
        # дошли до конца слова
        return 1
    return observe(
        matrix=matrix,
        i=i + direction_i,
        j=j + direction_j,
        value=next_value,
        direction_i=direction_i,
        direction_j=direction_j,
    )


def part1(matrix: list[list[str]]) -> int:
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for direction_i, direction_j in (
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ):
                result += observe(
                    matrix=matrix,
                    i=i,
                    j=j,
                    value="X",
                    direction_i=direction_i,
                    direction_j=direction_j,
                )
    return result


def is_x_mas(matrix: list[list[str]], i: int, j: int) -> bool:
    if i < 1 or j < 1 or i >= len(matrix) - 1 or j >= len(matrix[0]) - 1:
        return False
    diagonal1 = (
        matrix[i - 1][j - 1] in ("M", "S")
        and matrix[i + 1][j + 1] in ("M", "S")
        and matrix[i - 1][j - 1] != matrix[i + 1][j + 1]
    )
    diagonal2 = (
        matrix[i - 1][j + 1] in ("M", "S")
        and matrix[i + 1][j - 1] in ("M", "S")
        and matrix[i - 1][j + 1] != matrix[i + 1][j - 1]
    )
    return matrix[i][j] == "A" and diagonal1 and diagonal2


def part2(matrix: list[list[str]]) -> int:
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if is_x_mas(matrix, i, j):
                result += 1
    return result


def solve(puzzle_input):
    matrix = parse_input(puzzle_input)
    yield part1(matrix)
    yield part2(matrix)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
