#!/usr/bin/env python

from __future__ import print_function

from oh_ir import detrend, display, main, io

import argparse
import matplotlib.pylab as plt
import numpy as np
import os


def cli():
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
            '--thres',
            type=float,
            default=3.,
            help='deviation from mean threshold')
    parser.add_argument(
            '--order',
            type=float,
            default=3.,
            help='order of fitted function')
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
    # add common arguments
    main.cli_common(parser)

    return parser.parse_args()


def _avg_chans(data, outliers):
    idx_ = np.nonzero(outliers)[0]
    return (data[idx_ - 1] + data[idx_ + 1]) / 2.


def clean_channel(series,
                  data,
                  window=21,
                  threshold=3.,
                  order=3.,
                  niter=20,
                  method='sg',
                  avg_fill=False,
                  ):

    outlier_idx = np.zeros(data.shape, dtype=bool)
    smooth_data = data.copy()

    for cntr in range(niter, 0, -1):
        [fitted_trend,
         outliers] = detrend.smooth(series,
                                    smooth_data,
                                    window=window,
                                    order=order,
                                    sigma=threshold,
                                    method=method)

        if np.nonzero(outliers)[0].size < 1:
            break

        if avg_fill:
            smooth_data[outliers] = _avg_chans(data, outliers)
        else:
            smooth_data[outliers] = fitted_trend[outliers]
        outlier_idx = (outlier_idx | outliers)

    return fitted_trend, outlier_idx


if __name__ == '__main__':

    args = cli()

    # read input data assuming HartRAO format
    [header,
     chan_vel,
     timestamps,
     spectra,
     ts_jd] = io.input(args.filename,
                       epoch=args.epoch,
                       tsformat=args.tsformat)

    # use only the strongest channel to clean outliers
    if args.channel is None:
        avg_spectra = spectra.mean(axis=0)
        channel = np.argmax(avg_spectra)
    else:
        avg_spectra = spectra[:, args.channel].mean(axis=0)
        channel = args.channel[np.argmax(avg_spectra)]

    chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])
    base_spectrum = spectra[:, channel]

    # remove outliers
    [fitted_trend,
     outliers_idx] = clean_channel(ts_jd.value,
                                   base_spectrum,
                                   window=args.win,
                                   threshold=args.thres,
                                   order=args.order,
                                   niter=args.niter,
                                   method=args.method,
                                   avg_fill=False)

    fig, ax = display.timeseries(ts_jd.datetime,
                                 base_spectrum,
                                 label=chan_velocity)
    fig, ax = display.timeseries(ts_jd[~outliers_idx].datetime,
                                 base_spectrum[~outliers_idx],
                                 color='r',
                                 linestyle='',
                                 fig=fig,
                                 ax=ax)
    ax.set_xlabel('date')
    ax.set_ylabel('channel flux [Jy]')

    # use outliers to flag all channels
    clean_ts = timestamps[~outliers_idx]
    clean_spectra = spectra[~outliers_idx, :]

    if args.save:
        outfile = os.path.basename(args.filename)
        [name, ext] = os.path.splitext(outfile)
        filename = '{}_clean{}'.format(name, ext)
        io.output(filename, header, clean_ts, clean_spectra)
        outfile = '{}_channel_{}'.format(outfile, channel)
        outfile = outfile.replace('.', '_')
        plt.savefig('{}_outliers.png'.format(outfile),
                    bbox_inches='tight')

    if args.verbose:
        plt.show()

# -fin-
