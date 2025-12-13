#!/usr/bin/env python3

from itertools import islice, zip_longest

import numpy as np
from funcy import partition_by

from aoc_util import AOC, run_aoc


def setup(input: str):
    *lines, ops = input.splitlines()
    return lines, ops.split()


def aoc06(lines: list[str], ops: list[str]) -> AOC:
    xs = np.loadtxt(lines, dtype=int)
    is_add = np.equal(ops, "+")
    yield np.sum(xs[:, is_add]) + np.sum(np.prod(xs[:, ~is_add], axis=0))

    chars_t = zip_longest(*(iter(line) for line in lines), fillvalue="")
    lines_t = ("".join(line).strip() for line in chars_t)
    groups_t = islice(partition_by(bool, lines_t), 0, None, 2)
    yield sum(
        (np.sum if add else np.prod)(np.loadtxt(group, dtype=int))
        for group, add in zip(groups_t, is_add, strict=True)
    )


if __name__ == "__main__":
    run_aoc(aoc06, transform=setup)
