#!/usr/bin/env python3

import concurrent.futures as fut

import numpy as np

from aoc_util import AOC, run_aoc


def aoc09(tiles: np.typing.NDArray[int]) -> AOC:
    triu0, triu1 = np.triu_indices(tiles.shape[0], k=1)
    # unique combinations of tiles, normalized cols <left_x top_y right_x bottom_y>
    rects = np.column_stack(tiles[[triu0, triu1]])
    rects[:, 0::2].sort(axis=1)
    rects[:, 1::2].sort(axis=1)
    areas = np.prod(rects[:, 2:4] - rects[:, 0:2] + 1, axis=1)
    yield np.max(areas)

    # all edges, normalized too
    edges = np.column_stack([tiles, np.roll(tiles, -1, axis=0)])
    edges[:, 0::2].sort(axis=1)
    edges[:, 1::2].sort(axis=1)

    # cross table whether edge is wholly <left, above, right, below> of rect
    with fut.ThreadPoolExecutor(max_workers=4) as pool:
        ready = fut.as_completed(
            [
                pool.submit(np.greater_equal.outer, rects[:, 0], edges[:, 2]),
                pool.submit(np.greater_equal.outer, rects[:, 1], edges[:, 3]),
                pool.submit(np.less_equal.outer, rects[:, 2], edges[:, 0]),
                pool.submit(np.less_equal.outer, rects[:, 3], edges[:, 1]),
            ]
        )
        rects_x_edges = next(ready).result()
        rects_x_edges |= next(ready).result()
        rects_x_edges |= next(ready).result()
        rects_x_edges |= next(ready).result()
    valid = np.all(rects_x_edges, axis=1)
    yield np.max(areas[valid])


if __name__ == "__main__":
    run_aoc(aoc09, read=(np.loadtxt, dict(dtype=int, delimiter=",")))
