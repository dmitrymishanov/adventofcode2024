"""AoC 13, 2024."""

import pathlib
import re
import sys
import time
from dataclasses import dataclass

TOKEN_A = 3
TOKEN_B = 1


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class Game:
    a: Coordinate
    b: Coordinate
    prize: Coordinate


a_button_re = re.compile("Button A: X\+(\d+), Y\+(\d+)")
b_button_re = re.compile("Button B: X\+(\d+), Y\+(\d+)")
prize_re = re.compile("Prize: X=(\d+), Y=(\d+)")


def parse_input(puzzle_input: str) -> list[Game]:
    games = []
    for game in puzzle_input.split("\n\n"):
        a = a_button_re.findall(game)[0]
        b = b_button_re.findall(game)[0]
        p = prize_re.findall(game)[0]
        games.append(
            Game(
                a=Coordinate(int(a[0]), int(a[1])),
                b=Coordinate(int(b[0]), int(b[1])),
                prize=Coordinate(int(p[0]), int(p[1])),
            )
        )
    return games


def play(game: Game) -> int:
    a, b, p = game.a, game.b, game.prize
    d = a.x * b.y - a.y * b.x
    result_a = (b.y * p.x - b.x * p.y) // d
    result_b = (a.x * p.y - a.y * p.x) // d
    if (
        result_a * a.x + result_b * b.x == p.x
        and result_a * a.y + result_b * b.y == p.y
    ):
        return result_a * TOKEN_A + result_b * TOKEN_B
    return 0


def part1(games: list[Game]) -> int:
    return sum(play(game) for game in games)


def part2(games: list[Game]) -> int:
    for game in games:
        game.prize.x += 10_000_000_000_000
        game.prize.y += 10_000_000_000_000
    return sum(play(game) for game in games)


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
