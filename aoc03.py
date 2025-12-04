#!/usr/bin/env python3

from funcy import map, lmap, autocurry
from aoc_util import run_aoc


def aoc03(lines):
    @autocurry
    def max_joltage(n, bank, start=0, acc=0):
        n -= 1
        if n:
            digit = max(bank[start:-n])
            idx = bank.index(digit, start)
            return max_joltage(n, bank, idx + 1, acc * 10 + digit)
        else:
            return acc * 10 + max(bank[start:])

    banks = [lmap(int, iter(bank)) for bank in lines]
    yield sum(map(max_joltage(2), banks))
    yield sum(map(max_joltage(12), banks))


if __name__ == "__main__":
    run_aoc(aoc03, split="lines")
