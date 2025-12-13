#!/usr/bin/env python3

import numpy as np

from aoc_util import AOC, run_aoc


def aoc01(rotations: list[int]) -> AOC:
    positions = np.add.accumulate([50, *rotations])
    zeros = np.logical_not(positions % 100)
    yield np.sum(zeros)

    revolution_r = positions // 100
    right_pass_zero = np.maximum(revolution_r[1:] - revolution_r[:-1], 0)
    revolution_l = (positions - 1) // 100
    left_pass_zero = np.maximum(revolution_l[:-1] - revolution_l[1:], 0)
    yield np.sum(right_pass_zero) + np.sum(left_pass_zero)


if __name__ == "__main__":
    run_aoc(
        aoc01,
        split="lines",
        apply=lambda line: int(line[1:]) * (-1) ** (line[0] == "L"),
        np_printoptions=dict(linewidth=120, threshold=100, edgeitems=10),
    )
