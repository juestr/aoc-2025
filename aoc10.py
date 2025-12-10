#!/usr/bin/env python3

from functools import cache
from itertools import product

import numpy as np
from funcy import autocurry, lmap
from scipy.optimize import linprog

from aoc_util import run_aoc


def parse_line(line):
    def csv(seq):
        return lmap(int, seq[1:-1].split(","))

    lights, *buttons, joltage = line.split()
    return ([c == "#" for c in lights[1:-1]], lmap(csv, buttons), csv(joltage))


def aoc10(
    lights: list[list[bool]],
    buttons: list[list[list[int]]],
    joltages: list[list[int]],
):
    @autocurry
    def to_state(button, n, dtype):
        s = np.zeros(n, dtype=dtype)
        s[button] = 1
        return s

    @cache
    def choices_asc(n):
        return lmap(list, sorted(product((False, True), repeat=n), key=sum))

    def analyze(lights, buttons):
        toggles = np.array(lmap(to_state(n=len(lights), dtype=bool), buttons))
        for choice in choices_asc(len(buttons)):
            if np.all(lights == np.logical_xor.reduce(toggles[choice], axis=0)):
                return sum(choice)

    def analyze2(joltage, buttons):
        toggles = np.array(lmap(to_state(n=len(joltage), dtype=int), buttons))
        result = linprog(
            np.ones(len(buttons)),
            A_eq=toggles.T,
            b_eq=joltage,
            integrality=1,
            method="highs",
        )
        assert result.success
        return int(np.sum(result.x))

    yield sum(map(analyze, lights, buttons))
    yield sum(map(analyze2, joltages, buttons))


if __name__ == "__main__":
    run_aoc(aoc10, split="lines", apply=parse_line, transform=lambda m: zip(*m))
