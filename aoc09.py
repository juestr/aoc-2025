#!/usr/bin/env python3

import numpy as np
from scipy.spatial.distance import pdist

from aoc_util import run_aoc


def aoc09(tiles: np.typing.NDArray[int]):
    areas = pdist(tiles, lambda t1, t2: np.prod(np.abs(t1 - t2) + 1)).astype(int)
    yield np.max(areas)

    triu0, triu1 = np.triu_indices(tiles.shape[0], k=1)
    rects = np.column_stack([tiles[triu0], tiles[triu1]])
    rects[:, 0::2].sort(axis=1)
    rects[:, 1::2].sort(axis=1)
    edges = np.column_stack([tiles, np.roll(tiles, -1, axis=0)])
    edges[:, 0::2].sort(axis=1)
    edges[:, 1::2].sort(axis=1)
    rects_x_edges = np.logical_or.reduce(
        (edges[None, :, 2:4] <= rects[:, None, 0:2])
        | (edges[None, :, 0:2] >= rects[:, None, 2:4]),
        axis=-1,
    )
    valid = np.all(rects_x_edges, axis=1)
    yield np.max(areas[valid])


if __name__ == "__main__":
    run_aoc(aoc09, read=(np.loadtxt, dict(dtype=int, delimiter=",")))
