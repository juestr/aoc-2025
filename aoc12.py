#!/usr/bin/env python3

import re

import numpy as np
from funcy import autocurry, lmap, map, re_iter

from aoc_util import AOC, np_raw_table, run_aoc


def setup(input):
    return (
        np.array(
            lmap(
                autocurry(np_raw_table)(cmp=ord("#")),
                re_iter(r"^\d:\n(...\n...\n...\n)", input, re.M),
            )
        ),
        np.array(
            lmap(
                autocurry(lmap)(int),
                re_iter(
                    r"^(\d+)x(\d+): (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)", input, re.M
                ),
            )
        ),
    )


def aoc12(shapes: np.typing.NDArray[np.uint8], regions: np.typing.NDArray[int]) -> AOC:
    def check_region(region):
        shape, todo = region[:2], region[2:]
        if np.sum(todo) * 9 <= np.prod(shape // 3 * 3):
            return True
        elif todo @ weights > np.prod(shape):
            return False
        else:
            raise AssertionError("unclear case, this would require a lot of work")

    weights = np.sum(shapes, axis=(1, 2))
    yield sum(map(check_region, regions))


if __name__ == "__main__":
    run_aoc(aoc12, transform=setup)
