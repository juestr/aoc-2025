#!/usr/bin/env python3

import numpy as np
import numpy.typing as npt

from aoc_util import run_aoc


def setup(input):
    p1, p2 = input.split("\n\n")
    return (
        np.fromstring(p1.replace("-", "\n"), sep="\n", dtype=int).reshape((-1, 2)),
        np.fromstring(p2, sep="\n", dtype=int),
    )


def aoc05(fresh: npt.NDArray[int], available: npt.NDArray[int]):
    in_range_cross = np.logical_and(
        np.greater_equal.outer(available, fresh[:, 0]),
        np.less_equal.outer(available, fresh[:, 1]),
    )
    in_any_range = np.logical_or.reduce(in_range_cross, axis=1)
    yield np.sum(in_any_range)

    fresh_sorted = np.sort(np.sort(fresh, axis=1), axis=0, stable=True)
    running_floor = np.roll(np.maximum.accumulate(fresh_sorted[:, 1]), 1)
    running_floor[0] = -1
    unique_ids = fresh_sorted[:, 1] - np.maximum(fresh_sorted[:, 0] - 1, running_floor)
    yield np.sum(unique_ids)


if __name__ == "__main__":
    run_aoc(aoc05, transform=setup)
