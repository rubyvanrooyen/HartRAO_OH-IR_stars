## Define command line input arguments

from __future__ import print_function

import argparse

# def cli_common(parser):


def cli_periodogram():
    usage = "%(prog)s [options]"
    description = 'period calculation with Lomb-Scargle method'

    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    return parser.parse_args()

#def cli_...

# -fin-
