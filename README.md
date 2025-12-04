# aoc-2025

[Advent of Code 2025](https://adventofcode.com/2025) workspace.

This year I am using *uv* to manage dependencies. There is no build system,
this is still meant to be checked out and run directly from the repository
directory.

Each day's puzzle solver can be run as a standalone script without arguments
in the following way. It also accepts command line options and environment
variables to enable various instrumentations, see --help for further details.

    uv run aoc<day>.py <args...>

aoc_util.py contains common utils, boilerplate and a commandline runner.

The puzzle solvers are written using Python 3.14, and formatted by ruff. I am
not bothering with types or type checking, except sometimes for documentation
purposes.

