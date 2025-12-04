"""AOC puzzle solving support"""

import logging
import os
import sys
import timeit
from argparse import ArgumentParser
from logging import debug, error, info, warn
from typing import Any, Callable

_keep_imports = error, warn, info, debug  # re-export
_root_logger = logging.getLogger()

AOC_INTERACTIVE = int(os.environ.get("AOC_INTERACTIVE") or 0)


def _fix_lambda(f, default=lambda x: x):
    match f:
        case None:
            return default
        case (f, *args, kw) if isinstance(kw, dict):
            return lambda input: f(input, *args, **kw)
        case (f, *args):
            return lambda input: f(input, *args)
        case _:
            return f


def dbg(*args, s=" ", r=False, p=False, m=None, t=None, l=logging.DEBUG, apply=None):  # noqa: E741
    """Simple logging.debug helper"""
    if _root_logger.isEnabledFor(l):
        n = len(args)
        if p:
            from pprint import pformat  # noqa: autoimport

            if s == " ":
                s = "\n"
            args = list(map(pformat, args))
        if apply:
            args = list(map(apply, args))
        logging.log(
            l,
            (str(t) + ":\n" if t is not None else "")
            + (str(m) + ":" + s if m is not None else "")
            + s.join(("%" + "sr"[r],) * n),
            *args,
        )
    if len(args) == 1:
        return args[0]
    else:
        return args


def prompt(msg="continue?", prompt=1, level=logging.DEBUG):
    if logging.getLogger().isEnabledFor(level):
        if AOC_INTERACTIVE >= prompt:
            return input(msg)


def np_condense(s: Any) -> str:
    """Condense str conversion of a np.array or similar"""
    return str(s).replace(" ", "").replace("[", "").replace("]", "")


def readfile(fn):
    """Default input reader"""
    with open(fn) as fd:
        return fd.read()


def read_pd_table(fn, *args, **kw):
    """Read whitespace separated tabular data to a pandas dataframe"""
    import pandas as pd  # noqa: autoimport

    return pd.read_table(fn, sep=r"\s+", header=None, *args, **kw)


def np_raw_table(input, dtype="uint8", offs=0):
    """Transform raw tabular data to a 2d np.array"""
    import numpy as np  # noqa: autoimport

    n = input.index("\n")
    flat = np.fromstring(input, dtype=dtype)
    return (flat.reshape((-1, n + 1))[:, :-1] - offs,)


def mk_input_reader(
    read=readfile, split=None, apply=None, transform=None
) -> Callable[[str], tuple[Any, ...]]:
    """Returns a function reading and transforming an input file"""

    def get_input(filename: str) -> tuple[Any, ...]:
        input = read(filename)
        match split:
            case None:
                pass
            case "fields":
                input = [apply(x) for x in input.split()]
            case "lines":
                input = [apply(x) for x in input.splitlines()]
            case "lines_fields":
                input = [
                    tuple(apply(x) for x in line.split()) for line in input.splitlines()
                ]
            case c:
                input = [apply(x) for x in input.split(c)]
        if transform:
            return transform(input)
        else:
            return (input,)

    read = _fix_lambda(read)
    apply = _fix_lambda(apply)
    transform = _fix_lambda(transform, lambda x: (x,))
    return get_input


def mk_parser(day: int, loglevel):
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
    return parser


def run_aoc(
    aocf,
    *,
    day=None,
    read=readfile,
    split=None,
    apply=None,
    transform=None,
    time=(1, "s"),
    np_printoptions=None,
):
    """Runs puzzle solving generator function aocf with appropriate input

    The day parameter is auto detected if the name of aocf ends in 2 digits,
    and is used to select defaults for the input files read.

    The input file is read(), optionally split into lines and/or fields which
    are mapped by appy(), then finally passed through transform() and provided
    as multiple arguments to aocf.

    The aocf function should yield its results when ready.

    See --help or mk_parser for options taken from command line.
    """

    def lap_time(label="Time: "):
        nonlocal t1, t2
        if cmdargs.timeit:
            t1, t2 = t2, timeit.default_timer()
            info(f"🕚 {label}{(t2-t1)*time[0]:_.3f}{time[1]}\n")

    def total_time(label="Total time: "):
        if cmdargs.timeit:
            t = timeit.default_timer()
            info(f"🕚{label}{(t-t0)*time[0]:_.3f}{time[1]}\n")
            info("🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n")

    t0 = t1 = t2 = timeit.default_timer()
    day = day or int(aocf.__name__[-2:])
    # session = os.environ.get("SESSION")
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    cmdargs = mk_parser(day, loglevel).parse_args()
    assert (
        not cmdargs.expect or not cmdargs.test
    ), "--expect and --test are incompatible"
    cmdargs.results = cmdargs.input + ".results"

    logging.basicConfig(
        stream=sys.stdout,
        encoding="utf-8",
        format="%(message)s",
        level=100 if cmdargs.loglevel == "OFF" else getattr(logging, cmdargs.loglevel),
    )

    aocf_args = mk_input_reader(read, split, apply, transform)(cmdargs.input)

    if cmdargs.test:
        with open(cmdargs.results) as fd:
            parts = fd.read().replace("\\\n", "\0").splitlines()
        cmdargs.expect = [part.replace("\0", "\n") for part in parts]
    cmdargs.expect.reverse()

    if np_printoptions:
        import numpy as np  # noqa: autoimport

        np.set_printoptions(**np_printoptions)

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
