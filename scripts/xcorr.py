#!/usr/bin/env python

from __future__ import print_function

import argparse
import matplotlib.pylab as plt
import numpy as np
from oh_ir import detrend, display, io, main, util


def cli():
    usage = "%(prog)s [options]"
    description = 'Xcorrelate first 2 columns in file'
    # parser for periodogram script
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # correlation specific options
    ts_formats = ['full', 'same', 'valid']
    parser.add_argument(
            '--mode',
            type=str,
            default='full',
            choices=ts_formats,
            help="'full': correlation at each point of overlap"
                 "'same': only middle values of the correlation"
                 "'valid': only given for points where "
                 "the signals overlap")
    parser.add_argument(
        '--smooth',
        action='store_true',
        help='fit smoothing function before correlation')
    # add common output arguments
    main.cli_common(parser)
    return parser.parse_args()


def show_data(timestamps,
              red_chan,
              blue_chan,
              fig, ax,
              marker, linestyle,
              ):
    fig, ax = display.timeseries(timestamps,
                                 red_chan,
                                 marker=marker,
                                 linestyle=linestyle,
                                 color='r',
                                 fig=fig,
                                 ax=ax)
    fig, ax = display.timeseries(timestamps,
                                 blue_chan,
                                 marker=marker,
                                 linestyle=linestyle,
                                 color='b',
                                 fig=fig,
                                 ax=ax)
    return fig, ax


def get_lag(corr, len_, fig=None, ax=None):
    # Generate a lag axis
    corr_tickes = np.arange(corr.size)
    # Convert this into lag units, but still not really physical
    lags = corr_tickes - (len_ - 1)
    # This is just the x-spacing (or for you, the timestep) in your data
    distancePerLag = (corr_tickes[-1] - corr_tickes[0])/float(corr_tickes.size)
    # Convert your lags into physical units
    offsets = -lags*distancePerLag

    if ax is not None:
        ax = plt.subplot(212)
        label = 'Lag %.2f days' % offsets[np.argmax(corr)]
        fig, ax = display.timeseries(offsets,
                                     corr,
                                     label=label,
                                     color='k',
                                     marker='',
                                     linestyle='-',
                                     fig=fig,
                                     ax=ax)
        ax.axvline(x=offsets[np.argmax(corr)],
                   color='c',
                   linestyle=":")


if __name__ == '__main__':

    args = cli()
    [_, chan_vel, timestamps, spectra] = io.readfile(args.filename)
    ts_jd = util.ts2datetime(timestamps,
                             epoch=args.epoch,
                             tsformat=args.tsformat)

    red_chan_vel = 'Line velocity {} km/s'.format(chan_vel[0])
    red_chan = np.array(spectra[:, 0])
    blue_chan_vel = 'Line velocity {} km/s'.format(chan_vel[1])
    blue_chan = np.array(spectra[:, 1])

    if args.verbose:
        fig_ = plt.subplots(figsize=(15, 7),
                            facecolor='white')
        ax_ = plt.subplot(211)
        fit_, ax_ = show_data(ts_jd.datetime,
                              red_chan,
                              blue_chan,
                              fig_, ax_,
                              marker='.', linestyle=':')
    if args.smooth:
        [red_chan, _] = detrend.smooth(ts_jd.unix,
                                       red_chan)
        [blue_chan, _] = detrend.smooth(ts_jd.unix,
                                        blue_chan)
        fit_, ax_ = show_data(ts_jd.datetime,
                              red_chan,
                              blue_chan,
                              fig_, ax_,
                              marker='', linestyle='-')
        ax_.set_ylabel('Flux density [Jy]')
        ax_.set_xlabel('Timestamp')

    corr = np.correlate(red_chan, blue_chan, args.mode)
    get_lag(corr, red_chan.size, fig=fig_, ax=ax_)

    if args.verbose or args.phase:
        plt.show()

# -fin-
