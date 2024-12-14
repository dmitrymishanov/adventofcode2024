"""AoC 14, 2024."""

import pathlib
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from functools import reduce

import colorama

WIDTH = 101
HEIGHT = 103

# p=0,4 v=3,-3
robot_re = re.compile("p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


@dataclass
class NumPair:
    x: int
    y: int


@dataclass
class Quadrant:
    end_position: NumPair
    robots: int = 0


@dataclass
class Robot:
    position: NumPair
    velocity: NumPair


def parse_input(puzzle_input: str) -> list[Robot]:
    robots = []
    for line in puzzle_input.split("\n"):
        px, py, vx, vy = robot_re.findall(line)[0]
        robots.append(
            Robot(
                position=NumPair(int(px), int(py)),
                velocity=NumPair(int(vx), int(vy)),
            )
        )
    return robots


def find_new_linear_coordinate(
    pos: int, velocity: int, seconds: int, limit: int
) -> int:
    pos += velocity * seconds
    return pos % limit


def change_position(robot: Robot, seconds: int) -> Robot:
    robot.position.x = find_new_linear_coordinate(
        robot.position.x, robot.velocity.x, seconds, WIDTH
    )
    robot.position.y = find_new_linear_coordinate(
        robot.position.y, robot.velocity.y, seconds, HEIGHT
    )

    return robot


def get_sorted_quadrants() -> list[Quadrant]:
    return [
        Quadrant(NumPair(WIDTH // 2, HEIGHT // 2)),
        Quadrant(NumPair(WIDTH // 2, HEIGHT)),
        Quadrant(NumPair(WIDTH, HEIGHT // 2)),
        Quadrant(NumPair(WIDTH, HEIGHT)),
    ]


def part1(robots: list[Robot]) -> int:
    quadrants = get_sorted_quadrants()
    for robot in robots:
        change_position(robot, 100)
        if robot.position.x == WIDTH // 2 or robot.position.y == HEIGHT // 2:
            continue
        for quadrant in quadrants:
            if (
                robot.position.x < quadrant.end_position.x
                and robot.position.y < quadrant.end_position.y
            ):
                quadrant.robots += 1
                break

    return reduce(lambda a, b: a * b, [q.robots for q in quadrants], 1)


def show(robots: list[Robot], seconds: int):
    grid = Counter((r.position.x, r.position.y) for r in robots)
    print("_" * WIDTH)
    print("SECONDS: ", seconds)
    print(colorama.Cursor.POS(x=1, y=1))
    for row in range(HEIGHT):
        for col in range(WIDTH):
            print("#" if grid.get((col, row)) else " ", end="")
        print()


def part2(robots: list[Robot]) -> None:
    seconds = 0
    while True:
        seconds += 1
        for robot in robots:
            change_position(robot, 1)
        show(robots, seconds)


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
