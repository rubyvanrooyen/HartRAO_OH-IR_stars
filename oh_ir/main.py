# Define command line input arguments

from __future__ import print_function

import argparse


def cli_common_output(parser):
    group = parser.add_argument_group(
            title='output options',
            description='results and output display options')
    group.add_argument(
        '-s', '--save',
        action='store_true',
        help='save figure as PNG to working directory')
    group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='verbose display of input data and output results')


def cli_common_input(parser):
    group = parser.add_argument_group(
            title='input arguments',
            description='input data and processing parameters')
    group.add_argument(
            '--filename',
            type=str,
            required=True,
            help='**required**: name of HartRAO observation file containing '
                 'timestamps and channel data')
    ts_formats = ['jd', 'mjd']
    group.add_argument(
            '--tsformat',
            type=str,
            default='mjd',
            choices=ts_formats,
            help='mjd ts assuming 1900 epoch, '
                 'or modified jd = ts - epoch')
    group.add_argument(
            '--epoch',
            type=int,
            default=0.,
            help='epoch for modified jd = ts - epoch')
    group.add_argument(
            '--channel',
            type=int,
            nargs='+',
            help='specific channels of interest')


def cli_common(parser):
    # add common input arguments
    cli_common_input(parser)
    # add common output arguments
    cli_common_output(parser)


def cli_periodogram():
    usage = "%(prog)s [options]"
    description = 'period calculation with Lomb-Scargle method'
    # parser for periodogram script
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # periodogram specific input arguments
    parser.add_argument(
            '--phase',
            action='store_true',
            help='fold phase using using LS periodogram calculated')
    # add common output arguments
    cli_common(parser)

    return parser.parse_args()


def cli_outliers():
    usage = "%(prog)s [options]"
    description = 'smoothing calculation with Savitzky-Golay method'
    # parser for smoothing and outlier identification script
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            '--win',
            type=int,
            default=21,
            help='data smoothing window size')
    parser.add_argument(
            '--niter',
            type=int,
            default=100,
            help='max number of iterations')
    parser.add_argument(
            '--method',
            type=str,
            default='sg',
            help='fractional occurrence of outliers in strongest 5 channels')
    parser.add_argument(
            '--recurrence',
            type=float,
            default=None,
            help='fractional occurrence of outliers in strongest 5 channels')
    # add common input arguments
    cli_common_input(parser)
    # add common output arguments
    cli_common_output(parser)

    return parser.parse_args()

# -fin-
