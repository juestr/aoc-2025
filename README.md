# aoc-2025

[Advent of Code 2025](https://adventofcode.com/2025) workspace.

Each day's puzzle can be run as a standalone script without arguments. It accepts command line options for various instrumentations, see --help.

aoc_util.py contains common utils, boilerplate and a commandline runner.

The puzzles were written using Python 3.14, and are formatted by ruff in default configuration. I am not bothering with types or type checking.

This year I am using uv to manage dependencies, the individual scripts can be run by:

    uv run aocXY.py <args...>
