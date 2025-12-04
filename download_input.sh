#!/usr/bin/env bash

if [ -z "$SESSION" ] ; then
  echo "export SESSION= missing (cookie from browser)"
  exit 1
fi
if [ -z "$1" ] ; then
  echo "Provide a number"
  exit 1
fi

fn=`printf 'aoc%02d.py' $1`
if [ -e "$fn" ] ; then
  echo "$fn already exists"
else
  echo "Creating skeleton $fn"
  printf "#!/usr/bin/env python3

from funcy import map, lmap, mapcat, lmapcat, pairwise
import numpy as np
import pandas as pd
from aoc_util import run_aoc, error, info, debug, dbg, np_raw_table

def aoc%02d(input):


    yield 1

    yield 2


if __name__ == '__main__':
    run_aoc(
        aoc%02d,
        #  read=(pd.read_table, dict(header=None, header=(), sep=' ', delim_whitespace=True)),
        #  split='lines',
        #  apply=int,
        #  transform=np_raw_table,
        #  np_printoptions=dict(linewidth=120, threshold=5000, edgeitems=10),
    )
" $1 $1 > $fn
chmod 755 $fn
codium $fn
fi

fn=`printf 'data/aoc%02d_example.txt' $1`
echo "Touching $fn"
touch $fn
codium $fn
fn=`printf 'data/aoc%02d_example.txt.results' $1`
echo "Touching $fn"
touch $fn
codium $fn
fn=`printf 'data/aoc%02d_input.txt.results' $1`
echo "Touching $fn"
touch $fn

fn=`printf 'data/aoc%02d_input.txt' $1`
echo "Downloading input for day <$1> to $fn"
curl --cookie session=${SESSION} "https://adventofcode.com/2025/day/$1/input" > $fn || ( echo "download failed" && exit 1 )
