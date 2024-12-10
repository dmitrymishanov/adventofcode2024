"""AoC 10, 2024."""

import pathlib
import sys
import time


def parse_input(puzzle_input: str) -> list[list[int]]:
    return [[int(v) for v in line] for line in puzzle_input.split("\n")]


def find_scores(map_: list[list[int]], check_visited: bool) -> int:
    result = 0
    visited = set()

    def observe_trail(i: int, j: int, prev: int) -> int:
        if (
            not (0 <= i < len(map_) and 0 <= j < len(map_[0]))
            or (map_[i][j] - prev) != 1
            or (check_visited and (i, j) in visited)
        ):
            return 0
        if check_visited:
            visited.add((i, j))
        if map_[i][j] == 9:
            return 1
        return sum(
            observe_trail(i + coords[0], j + coords[1], map_[i][j])
            for coords in [(0, -1), (0, 1), (-1, 0), (1, 0)]
        )

    for i in range(len(map_)):
        for j in range(len(map_[0])):
            if map_[i][j] == 0:
                result += observe_trail(i, j, -1)
                visited.clear()
    return result


def part1(map_: list[list[int]]) -> int:
    return find_scores(map_, check_visited=True)


def part2(map_: list[list[int]]) -> int:
    return find_scores(map_, check_visited=False)


def solve(puzzle_input):
    data = parse_input(puzzle_input)
    start = time.monotonic()
    r1 = part1(data)
    p1 = time.monotonic()
    print(f"Part 1: {p1-start:.6f}s")
    print(f"Result: {r1}")
    r2 = part2(data)
    p2 = time.monotonic()
    print(f"Part 2: {p2 - p1:.6f}s")
    print(f"Result: {r2}")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
