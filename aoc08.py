#!/usr/bin/env python3


import numpy as np
from scipy.spatial.distance import pdist

from aoc_util import AOC, run_aoc


def aoc08(boxes: np.typing.NDArray[int]) -> AOC:
    def get_circuits_and_last_boxes(closest):
        circuits = np.arange(N, dtype=int)
        n = N
        for box1, box2 in closest:
            c1, c2 = circuits[box1], circuits[box2]
            if c1 != c2:
                circuits[circuits == c2] = c1
                n -= 1
            if n == 1:
                break
        return circuits, box1, box2

    N = boxes.shape[0]
    CABLES = 10 if N == 20 else 1000  # implicit param for example
    closest_condensed = np.argsort(pdist(boxes))
    triu_a, triu_b = np.triu_indices(N, k=1)
    closest = np.column_stack([triu_a[closest_condensed], triu_b[closest_condensed]])

    circuits, _, _ = get_circuits_and_last_boxes(closest[:CABLES])
    _, sizes = np.unique(circuits, return_counts=True)
    yield np.prod(np.sort(sizes)[-3:])

    _, box1, box2 = get_circuits_and_last_boxes(closest)
    yield boxes[box1, 0] * boxes[box2, 0]


if __name__ == "__main__":
    run_aoc(aoc08, read=(np.loadtxt, dict(dtype=int, delimiter=",")))
