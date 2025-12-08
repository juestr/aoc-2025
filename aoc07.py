#!/usr/bin/env python3

import numpy as np

from aoc_util import np_raw_table, run_aoc


def aoc07(grid: np.typing.NDArray[bool]):
    splitters = grid[1:]
    beams = grid.astype(int)
    beams[1:] = 0

    for r in range(1, beams.shape[0]):
        prev = r - 1
        split_beams = beams[prev] * splitters[prev]
        beams[r] = beams[prev] * ~splitters[prev]
        beams[r][:-1] += split_beams[1:]
        beams[r][1:] += split_beams[:-1]

    yield np.sum(np.logical_and(splitters, beams[:-1]))
    yield np.sum(beams[-1])


if __name__ == "__main__":
    run_aoc(
        aoc07,
        apply=(np_raw_table, dict(offs=ord("."), dtype=bool)),
        np_printoptions=dict(linewidth=120, threshold=100, edgeitems=10),
    )
