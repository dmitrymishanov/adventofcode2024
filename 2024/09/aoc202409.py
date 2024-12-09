"""AoC 9, 2024."""

import pathlib
import sys
import time
from collections.abc import Callable


def parse_input(puzzle_input: str) -> list[int | str]:
    return get_full_disk_view(puzzle_input)


def get_full_disk_view(disk: str) -> list[int | str]:
    full_view = []
    for i, value in enumerate(disk):
        if i % 2 == 0:
            full_view.extend([i // 2] * int(value))
        else:
            full_view.extend(["."] * int(value))
    return full_view


def get_checksum(full_view: list[int | str]) -> int:
    result = 0
    for i, value in enumerate(full_view):
        if value == ".":
            continue
        result += i * value
    return result


def move_files(
    disk: list[int | str],
    move_single_file: Callable[[list[int | str], int, int], tuple[int, int]],
) -> list[int | str]:
    disk = disk[:]
    left = 0
    right = len(disk) - 1
    while left < right:
        if disk[left] != ".":
            left += 1
        elif disk[right] == ".":
            right -= 1
        else:
            left, right = move_single_file(disk, left, right)

    return disk


def move_file_fragmented(
    disk: list[int | str],
    space_index: int,
    file_index: int,
) -> tuple[int, int]:
    disk[space_index], disk[file_index] = disk[file_index], disk[space_index]
    return space_index + 1, file_index - 1


def move_full_file(
    disk: list[int | str],
    space_index: int,
    file_index: int,
) -> tuple[int, int]:
    file_value = disk[file_index]
    file_size = 0
    while file_value == disk[file_index]:
        file_size += 1
        file_index -= 1

    space_size = 0
    space_i = space_index
    while space_size < file_size and space_i <= file_index:
        if disk[space_i] == ".":
            space_size += 1
        else:
            space_size = 0
        space_i += 1

    if space_size == file_size:
        (
            disk[space_i - space_size : space_i],
            disk[file_index + 1 : file_index + file_size + 1],
        ) = (
            disk[file_index + 1 : file_index + file_size + 1],
            disk[space_i - space_size : space_i],
        )
    return space_index, file_index


def part1(disk: list[int | str]) -> int:
    disk = move_files(disk, move_file_fragmented)
    return get_checksum(disk)


def part2(disk: list[int | str]) -> int:
    disk = move_files(disk, move_full_file)
    return get_checksum(disk)


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
