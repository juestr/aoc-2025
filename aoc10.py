#!/usr/bin/env python3

from functools import cache
from itertools import product

import numpy as np
from funcy import lmap
from scipy.optimize import linprog

from aoc_util import AOC, run_aoc


def create_machine(line: str):
    def csv(seq):
        return lmap(int, seq[1:-1].split(","))

    def to_mask(seq):
        return lmap(set(csv(seq)), range(len(lights) - 2))

    lights, *buttons, joltage = line.split()
    return (
        np.array([c == "#" for c in lights[1:-1]]),
        np.array(lmap(to_mask, buttons)),
        np.array(csv(joltage)),
    )


def aoc10(
    lights: list[np.typing.NDArray[int, bool]],
    buttons: list[np.typing.NDArray[(int, int), bool]],
    joltages: list[np.typing.NDArray[int, int]],
) -> AOC:
    @cache
    def choices_asc(n):
        return lmap(list, sorted(product((False, True), repeat=n), key=sum))

    def analyze(lights, btns):
        for choice in choices_asc(len(btns)):
            selected = btns[choice]
            if np.all(lights == np.logical_xor.reduce(selected, axis=0)):
                return selected.shape[0]

    def analyze2(joltage, btns):
        result = linprog(
            np.ones(len(btns)),
            A_eq=btns.T,
            b_eq=joltage,
            integrality=1,
            method="highs",
        )
        assert result.success, "linprog failed"
        return int(result.fun)

    yield sum(map(analyze, lights, buttons))
    yield sum(map(analyze2, joltages, buttons))


if __name__ == "__main__":
    run_aoc(aoc10, split="lines", apply=create_machine, transform=lambda m: zip(*m))
