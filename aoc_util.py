"""AOC puzzle solving support"""

import abc
import logging
import os
import sys
import timeit
from argparse import ArgumentParser
from logging import debug, error, info, warn
from typing import Any

_keep_imports = error, warn, info, debug  # re-export
_root_logger = logging.getLogger()

# SESSION = os.environ.get("SESSION")
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
AOC_INTERACTIVE = int(os.environ.get("AOC_INTERACTIVE") or 0)

type AOC[T = int] = abc.Generator[T]


def _fix_lambda(f=None, default=lambda x: x):
    """Support flexible lambda argument specification"""

    match f:
        case None:
            return default
        case (f, *args, kw) if isinstance(kw, dict):
            return lambda input: f(input, *args, **kw)
        case (f, *args):
            return lambda input: f(input, *args)
        case _:
            return f


# --- exported utils not directly related to the cli runner ---


def dbg(
    *values,
    s=" ",
    r=False,
    p=False,
    m: str = None,
    t: str = None,
    l=logging.DEBUG,  # noqa: E741
    apply=None,
):  # noqa: E741
    """Simple debug logging helper

    *values: values to log, can be Any
    t: print a title on line above
    m: print a message prefix before values
    s: value separator
    r: use repr instead of str
    p: use pprint
    l: logging.LEVEL
    apply: map values (lazy, not called if loglevel not sufficient)
    """

    if _root_logger.isEnabledFor(l):
        n = len(values)
        if p:
            from pprint import pformat  # noqa: autoimport

            if s == " ":
                s = "\n"
            values = list(map(pformat, values))
        if apply:
            values = list(map(apply, values))
        logging.log(
            l,
            (str(t) + ":\n" if t is not None else "")
            + (str(m) + ":" + s if m is not None else "")
            + s.join(("%" + "sr"[r],) * n),
            *values,
        )
    if len(values) == 1:
        return values[0]
    else:
        return values


def prompt(msg="continue?", prompt=1, level=logging.DEBUG):
    if _root_logger.isEnabledFor(level):
        if AOC_INTERACTIVE >= prompt:
            return input(msg)


def np_condense(s: Any) -> str:
    """Condense str conversion of a np.array or similar"""
    return str(s).replace(" ", "").replace("[", "").replace("]", "")


# --- input readers and parsers ---


def readfile(fn: str) -> Any:
    """Default input reader"""
    with open(fn) as fd:
        return fd.read()


def read_pd_table(fn: str, *args, **kw) -> Any:
    """Read whitespace separated tabular data to a pandas dataframe"""
    import pandas as pd  # noqa: autoimport

    return pd.read_table(fn, *args, sep=r"\s+", header=None, **kw)


def np_raw_table(input: str, offs=None, cmp=None, dtype="uint8"):
    """Transform raw tabular data to a 2d np.array

    does:
    * ascii-encode input to bytes
    * frombuffer with dtype uint8
    * reshape using first line
    optional:
    * subtract offs
    * compare to cmp
    * change dtype
    """
    import numpy as np  # noqa: autoimport

    input = bytes(input, "ASCII")
    n = input.index(b"\n")
    table = np.frombuffer(input, dtype=np.uint8).reshape((-1, n + 1))[:, :-1]
    if offs:
        table = table - offs
    if cmp:
        table = np.equal(table, cmp)
    if dtype:
        table = table.astype(dtype)
    return table


# --- cli runner ---


def mk_arg_parser(day: int, loglevel) -> ArgumentParser:
    parser = ArgumentParser(description=f"Run AOC example {day}")
    parser.add_argument(
        "--input",
        default=f"data/aoc{day:02}_input.txt",
        help=f"input file to read (data/aoc{day:02}_input.txt)",
    )
    parser.add_argument(
        "--example",
        action="store_const",
        dest="input",
        const=f"data/aoc{day:02}_example.txt",
        help=f"read input from data/aoc{day:02}_example.txt",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="test against <input>.results",
    )
    parser.add_argument(
        "--expect", action="append", default=[], help="check expected result (multiple)"
    )
    parser.add_argument(
        "--write-results",
        action="store_true",
        default=False,
        help="create <input>.results",
    )
    parser.add_argument(
        "--timeit", action="store_true", default=False, help="show timing information"
    )
    parser.add_argument(
        "--loglevel",
        default=loglevel,
        choices=["OFF", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="log level, overrides $LOGLEVEL",
    )
    parser.add_argument(
        "--show-input",
        action="store_true",
        default=False,
        help="log parsed input on INFO",
    )
    return parser


def read_input(
    filename: str, read=readfile, split=None, apply=None, transform=None
) -> tuple[Any, ...]:
    """Read and optionally parse/transform an input file

    readfile: filename -> str | Any
    split: -> various modes to optionally split read input into structures
    apply: called on all structure elements resulting from split or the whole
    transform: optionally called in the end -> tuple of arguments to main function
    """

    read = _fix_lambda(read)
    apply = _fix_lambda(apply)
    transform = _fix_lambda(transform, lambda x: (x,))

    input = read(filename)

    match split:
        case None:
            input = apply(input)
        case "fields":
            input = [apply(x) for x in input.split()]
        case "lines":
            input = [apply(x) for x in input.splitlines()]
        case "lines_fields":
            input = [
                tuple(apply(x) for x in line.split()) for line in input.splitlines()
            ]
        case (ls, fs):
            input = [
                tuple(apply(x) for x in line.split(fs)) for line in input.split(ls)
            ]
        # todo: unused atm, let's treat strings as re patterns
        case c:
            input = [apply(x) for x in input.split(c)]

    return transform(input)


def run_aoc[T = int](
    aocf: AOC[T],
    *,
    day: int = None,
    read=readfile,
    split=None,
    apply=None,
    transform=None,
    time=(1000, "ms"),
    np_printoptions=None,
) -> None:
    """Runs puzzle solving generator function aocf with appropriate input

    Use --help or see mk_arg_parser for options taken from the command line.

    The day parameter is auto detected if the name of aocf ends in 2 digits,
    and is used to select defaults for the input files read.

    The input file is read with read_input and related arguments, executed,
    and the resulting tuple is passed to aocf as arguments.

    The aocf function should yield its results of type T when they become
    available, any number is acceptable.
    """

    def lap_time(label="Time: "):
        nonlocal t1, t2
        if cmdargs.timeit:
            t1, t2 = t2, timeit.default_timer()
            info(f"🕚 {label}{(t2 - t1) * time[0]:_.3f} {time[1]}\n")

    def total_time(label="Total time: "):
        if cmdargs.timeit:
            t = timeit.default_timer()
            info(f"🕚{label}{(t - t0) * time[0]:_.3f} {time[1]}\n")
            info("🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n")

    t0 = t1 = t2 = timeit.default_timer()
    day = day or int(aocf.__name__[-2:])
    cmdargs = mk_arg_parser(day, LOGLEVEL).parse_args()
    assert not cmdargs.expect or not cmdargs.test, (
        "--expect and --test are incompatible"
    )
    cmdargs.results = cmdargs.input + ".results"

    logging.basicConfig(
        stream=sys.stdout,
        encoding="utf-8",
        format="%(message)s",
        level=100 if cmdargs.loglevel == "OFF" else getattr(logging, cmdargs.loglevel),
    )

    if cmdargs.test:
        with open(cmdargs.results) as fd:
            parts = fd.read().replace("\\\n", "\0").splitlines()
        cmdargs.expect = [part.replace("\0", "\n") for part in parts]
    cmdargs.expect.reverse()

    if np_printoptions:
        import numpy as np  # noqa: autoimport

        np.set_printoptions(**np_printoptions)

    aocf_args = read_input(cmdargs.input, read, split, apply, transform)

    if cmdargs.show_input:
        aocf_args = list(aocf_args)
        info(f"\n🎄🎄🎄🎄  Input of {aocf.__name__}() 🎄🎄🎄🎄\n")
        dbg(*aocf_args, p=True, l=logging.INFO)
        info("")

    lap_time("Setup time: ")

    try:
        results = []
        for i, r in enumerate(aocf(*aocf_args), start=1):
            info(f"\n🎄🎄🎄 Result {i} of {aocf.__name__}()  🎄🎄🎄\n")
            print(r)
            info("")
            results.append(r)
            if cmdargs.expect:
                expected = cmdargs.expect.pop()
                if str(r) == expected:
                    info("✅ matches the expected value\n")
                else:
                    warn(
                        "❌ does not match %s%s\n", "\n" * ("\n" in expected), expected
                    )
            lap_time("Result time: ")
            info("🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n")
        total_time()

        if cmdargs.write_results:
            info("Writing results to %s", cmdargs.results)
            results = [str(r).replace("\n", "\\\n") for r in results]
            with open(cmdargs.results, "w") as fd:
                fd.write("\n".join(results))

    except BaseException:
        error("\n🎄🎄🎄🎄🎄🎄  Error   🎄🎄🎄🎄🎄🎄\n")
        total_time()
        raise
    finally:
        logging.shutdown()
