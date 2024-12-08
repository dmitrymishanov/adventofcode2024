"""AoC 8, 2024."""

import pathlib
import sys
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Data:
    antennas: dict[str, list[tuple[int, int]]]
    city_size: tuple[int, int]


def parse_input(puzzle_input: str) -> Data:
    antennas = defaultdict(list)
    matrix = [list(line) for line in puzzle_input.split("\n")]
    for i, line in enumerate(matrix):
        for j, symbol in enumerate(line):
            if symbol != ".":
                antennas[symbol].append((i, j))

    return Data(antennas=antennas, city_size=(len(matrix), len(matrix[0])))


def get_antinodes_for_pair1(
    first: tuple[int, int],
    second: tuple[int, int],
    city_size: tuple[int, int],
) -> set[tuple[int, int]]:
    if first == second:
        return set()
    return {
        loc
        for loc in [
            (first[0] - (second[0] - first[0]), first[1] - (second[1] - first[1])),
            (second[0] + (second[0] - first[0]), second[1] + (second[1] - first[1])),
        ]
        if 0 <= loc[0] < city_size[0] and 0 <= loc[1] < city_size[1]
    }


def get_antinodes_for_pair2(
    first: tuple[int, int],
    second: tuple[int, int],
    city_size: tuple[int, int],
) -> set[tuple[int, int]]:
    if first == second:
        return set()

    result = set()
    i_diff = second[0] - first[0]
    j_diff = second[1] - first[1]
    loc = first
    while 0 <= loc[0] < city_size[0] and 0 <= loc[1] < city_size[1]:
        result.add(loc)
        loc = (loc[0] - i_diff, loc[1] - j_diff)

    loc = second
    while 0 <= loc[0] < city_size[0] and 0 <= loc[1] < city_size[1]:
        result.add(loc)
        loc = (loc[0] + i_diff, loc[1] + j_diff)
    return result


def get_antinodes_count(
    data: Data,
    get_antinodes_for_pair: Callable[
        [tuple[int, int], tuple[int, int], tuple[int, int]], set[tuple[int, int]]
    ],
) -> int:
    antinodes = set()
    for antenna, locations in data.antennas.items():
        for loc1 in locations:
            for loc2 in locations:
                antinodes.update(get_antinodes_for_pair(loc1, loc2, data.city_size))
    return len(antinodes)


def part1(data: Data) -> int:
    return get_antinodes_count(data, get_antinodes_for_pair1)


def part2(data: Data) -> int:
    return get_antinodes_count(data, get_antinodes_for_pair2)


def solve(puzzle_input):
    data = parse_input(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
