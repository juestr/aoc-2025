#!/usr/bin/env python3

from funcy import autocurry, lmap, map

from aoc_util import AOC, run_aoc


def aoc03(banks: list[list[int]]) -> AOC:
    @autocurry
    def max_joltage(digits, bank, start=0, acc=0):
        digits -= 1
        if digits:
            n = max(bank[start:-digits])
            idx = bank.index(n, start) + 1
            return max_joltage(digits, bank, idx, acc * 10 + n)
        else:
            return acc * 10 + max(bank[start:])

    yield sum(map(max_joltage(2), banks))
    yield sum(map(max_joltage(12), banks))


if __name__ == "__main__":
    run_aoc(aoc03, split="lines", apply=autocurry(lmap)(int))
