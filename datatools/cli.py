from __future__ import print_function

import collections
import csv
import code
import json
import random
import fileinput
import sys

import click
import numpy as np
import scipy.stats  
import toolz
import toolz.curried
import itertools
import six


# Fixes pipe handling. See https://stevereads.com/2015/09/25/python-sigpipe/
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

# Ensures unicode can be printed / piped without errors.
# Alternative to setting PYTHONIOENCODING=utf-8 envvar
# See http://stackoverflow.com/questions/11741574/how-to-print-utf-8-encoded-text-to-the-console-in-python-3/11742928#11742928
import codecs
import locale
#sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
#sys.stdin = codecs.getreader(locale.getpreferredencoding())(sys.stdin)
#sys.stdin = codecs.getreader('utf-8')(sys.stdin)
#sys.stdin = codecs.getreader('utf-8')(sys.stdin)
# Not needed if use click


COMPUTE_FUNCTIONS = {
    'sum': sum,
    'mean': np.mean,
    'max': max,
    'min': min,
    'median': np.median,
    'std': np.std,
}

BYROW_FUNCTIONS = {
    'flatten',
}

RFTYPE = click.File('r', encoding='utf-8')
WFTYPE = click.File('w', encoding='utf-8'),


def get_valid_values(iterdata):
    for i, value in enumerate(iterdata):
        value = value.strip()
        try:
            yield float(value)
        except ValueError:
            print("Warning: value `{}` in position {} is not valid. Ignoring.".format(value, i))


@click.command()
@click.option('--sep', '-s', default=u',', help="Separator")
def count(infile=sys.stdin, outfile=sys.stdout, sep=u","):
    infile = (line.rstrip('\n') for line in infile)
    cdict = collections.Counter(infile)
    writer = csv.writer(outfile, delimiter=sep.encode('ascii', 'replace'))
    for entry, count in cdict.most_common():
        writer.writerow([entry, count])


@click.command()
@click.argument('data', type=RFTYPE, default=sys.stdin)
def describe(data):
    values = list(get_valid_values(data))
    print(scipy.stats.describe(values))


@click.command()
@click.argument('data', type=RFTYPE, default=sys.stdin)
@click.option('--rowsep', '-s', default=',')
@click.option('--function', '-f', type=click.Choice(COMPUTE_FUNCTIONS), required=True)
def dformat(data, outfile, function, rowsep):
    """Convert data from one format to another, optionally apply another command and output
    everything either in the original or the transformed format."""
    raise NotImplementedError
    reader = csv.reader(data)
    writer = csv.writer(outfile)
    for row in reader:
	writer.writerow(row)


@click.command()
@click.argument('data', type=RFTYPE, default=sys.stdin)
@click.option('--rowsep', '-s', default=',')
@click.option('--function', '-f', type=click.Choice(COMPUTE_FUNCTIONS), required=True)
def byrow(data, function, rowsep):
    reader = csv.reader(data)
    func = COMPUTE_FUNCTIONS[function]
    for row in reader:
        values = list(get_valid_values(row))
	print(func(values))
        #line = line.rstrip("\n")
        #values = line.split(rowsep)
        #print "\n".join(values)


# Strangely enough, this is quicker than `awk '!x[$0]++'`
@click.command()
@click.argument('data', type=RFTYPE, default=sys.stdin)
@click.option('--rowsep', default=',')
def dunique(data, rowsep):
    seen = set()
    for line in data:
        line = line.rstrip("\n")
        if line not in seen:
            seen.add(line)
            print(line)


@click.command()
@click.argument('data', type=RFTYPE, default=sys.stdin)
@click.option('--function', '-f', type=click.Choice(COMPUTE_FUNCTIONS.keys()), required=True)
@click.option('--key', '-k', type=int, default=0, help="Field key, 0-based")
def compute(data, function, key):
    """Calculate some measures.

    For single-value measures (like average or median, for example) you need
    to specify only one key.

    """
    func = COMPUTE_FUNCTIONS[function]
    values = list(get_valid_values(data))
    print(func(values))


@click.command()
@click.argument('minimum', type=float)
@click.argument('maximum', type=float)
@click.argument('num_values', type=int, default=1)
@click.option('--seed', default=None)
@click.option('--dtype', '-t', type=click.Choice(['int', 'float']), default='int')
def drandom(minimum, maximum, num_values, seed, dtype):
    """Generate random values."""
    rand_fun = {
        'int': random.randint,
        'float': random.uniform,
    }[dtype]
    if seed:
        random.seed(seed)
    for i in xrange(num_values):
        print(rand_fun(minimum, maximum))


@click.command()
@click.argument('left', type=RFTYPE)
@click.argument('right', type=RFTYPE, default=sys.stdin)
@click.option('--lkey', '-1', type=int, default=0, help="Left key")
@click.option('--rkey', '-2', type=int, default=0, help="Right key")
@click.option('--show', type=click.Choice(['left', 'right', 'both']),
              default='both',
              help="Show only left columns, right columns or both (default)")
@click.option('--sep', '-s', default=',', help="Separator")
@click.option('--sortedinput', default=False, is_flag=True, help="Sorted")
def join(left, lkey, right, rkey, sep, show, sortedinput):
    """Join two tabular datasets, LEFT and RIGHT, according to an "equality join".
    If RIGHT is missing, it will be assumed as STDIN.

    Please note that the LEFT content will need to be fully evaluated and kept
    in memory, while the RIGHT content will be streamed. Therefore, the largest
    sequence should always be in the RIGHT position.

    """
    #left = open(left, "r")
    #right = open(right, "r")
    left_sequence = (line.strip().split(sep)
                    for line in left)
    right_sequence = (line.strip().split(sep)
                    for line in right)

    # Perform the join
    if sortedinput:
        join_fun = sorted_join
    else:
        join_fun = toolz.join

    joined_sequence = join_fun(toolz.curried.nth(lkey),
                               left_sequence,
                               toolz.curried.nth(rkey),
                               right_sequence)

    # Show only left columns, only right or both (default)
    output_filter = {
        'left': toolz.first,
        'right': toolz.second,
        'both': toolz.curried.concat,
    }
    joined_sequence = toolz.map(output_filter[show], joined_sequence)

    for line in joined_sequence:
        line = escape_char(line, ",")
	#line = (i.encode('utf-8') for i in line)
        out= u','.join(list(line))
	#sys.stdout.write(out.encode('ascii', 'ignore'))
	#sys.stdout.write(out)
	click.echo(out)
	#sys.stdout.write("\n")


def escape_char(line, char):
    for field in line:
        if char in field:
            yield u'"{}"'.format(field)
        else:
            yield field


# Needs testing, perhaps refactoring too?
# See https://en.wikipedia.org/wiki/Sort-merge_join
def sorted_join(lkey, left, rkey, right):
    """Perform a join between two sequences sorted along their keys.

    This is useful when performing join over very large lists, as it is a full streaming join.

    """
    if not callable(lkey):
        lkey = toolz.itertoolz.getter(lkey)
    if not callable(rkey):
        rkey = toolz.itertoolz.getter(rkey)

    left_grouped = itertools.groupby(left, lkey)
    right_grouped = itertools.groupby(right, rkey)

    left_key, left_group = next(left_grouped)
    right_key, right_group = next(right_grouped)
    while True:
        if left_key == right_key:
            for a, b in itertools.product(left_group, right_group):
                yield (a, b)
            left_key, left_group = next(left_grouped)
            right_key, right_group = next(right_grouped)
        elif left_key < right_key:
            left_key, left_group = next(left_grouped)
        else:
            right_key, right_group = next(right_grouped)


@click.command()
@click.argument('jsonfile', type=RFTYPE, default=sys.stdin)
def jsonexplorer(jsonfile):
    """Load json file and launch a Python interactive console.

    This command is useful to explore the structure of the JSON document.

    """
    data = json.loads(jsonfile.read())
    banner = "### The JSON file has been loaded into the variable `data`. ###"
    code.interact(banner=banner, local=locals())


@click.command()
@click.argument('infile', type=RFTYPE, default=sys.stdin)
@click.option('--outfile', '-o', type=WFTYPE, default=sys.stdout)
@click.option('--patterns', '-f', type=RFTYPE)
@click.option('--value', '-v', type=str)
@click.option('--key', '-k', type=int, default=0, help="Field key, 0-based")
def grep(patterns, value,key, infile, outfile=sys.stdout):
    """Search for one or many values in a specific field."""
    if not (patterns or value):
        raise click.UsageError("Need to specify value (-v) or pattern file (-f)")
    if patterns:
        patterns = set([line.strip() for line in patterns])
    else:
        patterns = set([value, ])
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        if row[key] in patterns:
            writer.writerow(row)
