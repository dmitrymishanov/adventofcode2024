"""AoC 15, 2024."""

import pathlib
import sys
import time
from dataclasses import dataclass


@dataclass
class Data:
    matrix: list[list[str]]
    moves: list[str]
    robot: tuple[int, int]


def parse_input(puzzle_input: str) -> Data:
    matrix_raw, moves_raw = puzzle_input.split("\n\n")
    robot_position: tuple[int, int] | None = None

    matrix = []
    for i, line_raw in enumerate(matrix_raw.split("\n")):
        line = []
        for j, el in enumerate(line_raw):
            if el == "@":
                robot_position = (i, j)
            line.append(el)
        matrix.append(list(line_raw))

    assert robot_position

    moves = [m for m in moves_raw if m in "v^<>"]
    return Data(matrix, moves, robot_position)


def make_move(
    robot: tuple[int, int], matrix: list[list[str]], move: str
) -> tuple[int, int]:
    current_pos = robot
    i, j = MOVE_MAPPER[move]
    while matrix[current_pos[0]][current_pos[1]] not in ".#":
        current_pos = (current_pos[0] + i, current_pos[1] + j)

    if matrix[current_pos[0]][current_pos[1]] == "#":
        return robot

    while robot != current_pos:
        (
            matrix[current_pos[0]][current_pos[1]],
            matrix[current_pos[0] - i][current_pos[1] - j],
        ) = (
            matrix[current_pos[0] - i][current_pos[1] - j],
            matrix[current_pos[0]][current_pos[1]],
        )
        current_pos = (current_pos[0] - i, current_pos[1] - j)
    return robot[0] + i, robot[1] + j


MOVE_MAPPER = {
    "v": (1, 0),
    "^": (-1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

DEBUG = True


def show(matrix: list[list[str]]) -> None:
    if DEBUG:
        with open("output.txt", "w") as f:
            f.write("\n".join("".join(line) for line in matrix))


def get_result(matrix: list[list[str]]) -> int:
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "O":
                result += i * 100 + j

    return result


def part1(data: Data) -> int:
    robot = data.robot
    show(data.matrix)
    for move in data.moves:
        robot = make_move(robot, data.matrix, move)
        show(data.matrix)
    return get_result(data.matrix)


def part2(data: Data) -> int:
    pass


def solve(puzzle_input):
    start = time.monotonic()
    r1 = part1(parse_input(puzzle_input))
    p1 = time.monotonic()
    print(f"Part 1: {p1-start:.6f}s")
    print(f"Result: {r1}")
    r2 = part2(parse_input(puzzle_input))
    p2 = time.monotonic()
    print(f"Part 2: {p2 - p1:.6f}s")
    print(f"Result: {r2}")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
