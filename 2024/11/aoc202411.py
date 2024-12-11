"""AoC 11, 2024."""

import pathlib
import sys
import time
from functools import cache


def parse_input(puzzle_input: str) -> list[str]:
    return puzzle_input.split(" ")


@cache
def get_stone_result(stone: str, times: int) -> int:
    if times == 0:
        return 1
    if stone == "0":
        return get_stone_result("1", times - 1)
    elif len(stone) % 2 == 0:
        return get_stone_result(stone[: len(stone) // 2], times - 1) + get_stone_result(
            stone[len(stone) // 2 :].lstrip("0") or "0", times - 1
        )
    else:
        return get_stone_result(str(int(stone) * 2024), times - 1)


def blink(stones: list[str], times: int) -> int:
    result = 0
    for s in stones:
        result += get_stone_result(s, times)
    return result


def part1(stones: list[str]) -> int:
    return blink(stones, 25)


def part2(stones: list[str]) -> int:
    return blink(stones, 75)


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
