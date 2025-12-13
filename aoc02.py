#!/usr/bin/env python3

from funcy import re_tester

from aoc_util import AOC, run_aoc


def aoc02(id_ranges: list[tuple(int, int)]) -> AOC:
    def sum_matching_ids(pattern):
        p = re_tester(pattern)
        return sum(x for a, b in id_ranges for x in range(a, b + 1) if p(str(x)))

    yield sum_matching_ids(r"^(\d+)(\1)$")
    yield sum_matching_ids(r"^(\d+)(\1)+$")


if __name__ == "__main__":
    run_aoc(aoc02, split=(",", "-"), apply=int)
