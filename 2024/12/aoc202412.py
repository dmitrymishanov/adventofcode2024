"""AoC 12, 2024."""

import pathlib
import sys
import time
from collections import deque
from collections.abc import Callable


def parse_input(puzzle_input: str) -> list[list[str]]:
    return [list(line) for line in puzzle_input.split("\n")]


def observe_region1(
    map_: list[list[str | int]], start: tuple[int, int], region: int
) -> int:
    area = perimeter = 0
    region_letter = map_[start[0]][start[1]]
    map_[start[0]][start[1]] = region
    queue = deque([start])
    while queue and (plot := queue.pop()):
        i, j = plot
        area += 1

        for i_shift, j_shift in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not (
                0 <= (i + i_shift) < len(map_) and 0 <= (j + j_shift) < len(map_[0])
            ) or map_[i + i_shift][j + j_shift] not in (region_letter, region):
                # граничит с краем карты или другим регионом
                perimeter += 1
            elif map_[i + i_shift][j + j_shift] != region:
                # если еще не присоединили к региону
                map_[i + i_shift][j + j_shift] = region
                queue.appendleft((i + i_shift, j + j_shift))
    return area * perimeter


def observe_region2(
    map_: list[list[str | int]], start: tuple[int, int], region: int
) -> int:
    area = sides = 0
    # TODO
    return area * sides


def count_price(
    map_: list[list[str | int]],
    observe_region: Callable[[list[list[str | int]], tuple[int, int], int], int],
) -> int:
    regions = set()
    # числовое обозначение региона нужно из-за того,
    # что регионов с одинаковой буквой может быть несколько
    current_region = 0
    result = 0
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            if map_[i][j] not in regions:
                # еще не осматривали
                regions.add(current_region)
                result += observe_region(map_, (i, j), current_region)
                current_region += 1
    return result


def part1(map_: list[list[str]]) -> int:
    return count_price(map_, observe_region1)


def part2(map_: list[list[str]]) -> int:
    return count_price(map_, observe_region2)


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
