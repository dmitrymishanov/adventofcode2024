"""AoC 6, 2024."""

import pathlib
import sys
from copy import deepcopy
from dataclasses import dataclass, field

GUARD = "^"
OBSTACLE = "#"
VISITED = "X"
EMPTY = "."


DEBUG = False


def draw(room: list[list[str]]) -> None:
    with open("output.txt", "w") as file:
        file.write("\n".join(["".join(line) for line in room]))


@dataclass
class Data:
    guard_position: tuple[int, int]
    room: list[list[str]] = field(default_factory=list)


def parse_input(puzzle_input: str) -> Data:
    room = []
    guard_position = (0, 0)
    for i, line in enumerate(puzzle_input.split("\n")):
        line = list(line)
        try:
            j = line.index(GUARD)
            guard_position = (i, j)
        except ValueError:
            pass
        room.append(line)
    return Data(guard_position=guard_position, room=room)


def is_out(room: list[list[str]], i: int, j: int) -> bool:
    return not (0 <= i < len(room) and 0 <= j < len(room[0]))


def is_way(room: list[list[str]], i: int, j: int) -> bool:
    return is_out(room, i, j) or room[i][j] != OBSTACLE


DIRECTIONS = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def part1(data: Data) -> int:
    visited = 0
    room = deepcopy(data.room)
    if not room or not room[0]:
        return visited

    i, j = data.guard_position
    direction_i, direction_j = (-1, 0)
    while not is_out(room, i, j):
        if DEBUG:
            draw(room)

        if room[i][j] != VISITED:
            visited += 1
            room[i][j] = VISITED

        while not is_way(room, i + direction_i, j + direction_j):
            direction_i, direction_j = DIRECTIONS[(direction_i, direction_j)]
        i, j = i + direction_i, j + direction_j

    return visited


def is_loop(room: list[list[str]], i: int, j: int) -> bool:
    visited = 0
    loop_count = 0
    direction_i, direction_j = (-1, 0)
    while not is_out(room, i, j) and visited >= loop_count:
        if DEBUG:
            draw(room)
        if room[i][j] == VISITED:
            loop_count += 1
        else:
            visited += 1
            loop_count = 0
            room[i][j] = VISITED

        while not is_way(room, i + direction_i, j + direction_j):
            direction_i, direction_j = DIRECTIONS[(direction_i, direction_j)]
        i, j = i + direction_i, j + direction_j

    return loop_count and loop_count >= visited


def part2(data: Data) -> int:
    valid_obstacles = 0
    for i in range(len(data.room)):
        for j in range(len(data.room[0])):
            if data.room[i][j] == EMPTY:
                room = deepcopy(data.room)
                room[i][j] = OBSTACLE
                if is_loop(room, data.guard_position[0], data.guard_position[1]):
                    valid_obstacles += 1
    return valid_obstacles


def solve(puzzle_input):
    data = parse_input(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
