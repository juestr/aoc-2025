#!/usr/bin/env python3

import numpy as np
import scipy.signal as sig
from funcy import autocurry

from aoc_util import AOC, np_raw_table, run_aoc


def aoc04(grid: np.typing.NDArray[np.int8]) -> AOC:
    WEIGHTS = np.array([[-1, -1, -1], [-1, 4, -1], [-1, -1, -1]], dtype=np.int8)
    takeable = sig.convolve(grid, WEIGHTS, mode="same") > 0
    yield np.sum(takeable)

    taken = 0
    while ...:
        takeable = sig.convolve(grid, WEIGHTS, mode="same") > 0
        n = np.sum(takeable)
        if n == 0:
            break
        grid[takeable] = 0
        taken += n
    yield taken


if __name__ == "__main__":
    run_aoc(aoc04, apply=autocurry(np_raw_table)(cmp=ord("@"), dtype=np.int8))
