#!/usr/bin/env python3

from funcy import re_tester, walk
from aoc_util import run_aoc


def aoc02(input):
    def sum_matching_ids(pattern):
        pred = re_tester(pattern)
        return sum(x for a, b in ids for x in range(a, b + 1) if pred(str(x)))

    ids = [walk(int, pair.split("-")) for pair in input.split(",")]
    yield sum_matching_ids(r"^(\d+)(\1)$")
    yield sum_matching_ids(r"^(\d+)(\1)+$")


if __name__ == "__main__":
    run_aoc(aoc02)
