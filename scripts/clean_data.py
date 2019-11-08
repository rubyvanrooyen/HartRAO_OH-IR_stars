#!/usr/bin/env python

from __future__ import print_function

from oh_ir import detrend, display, main, io

import matplotlib.pylab as plt
import numpy as np
import os


def clean_channel(series,
                  data,
                  window=21,
                  niter=20,
                  method='sg'):

    outlier_idx = np.zeros(data.shape, dtype=bool)
    smooth_data = data.copy()
    for cntr in range(niter, 0, -1):
        [fitted_trend,
         outliers] = detrend.smooth(series,
                                    data,
                                    window=window,
                                    order=3.,
                                    sigma=3.,
                                    method=method)

        if np.nonzero(outliers)[0].size < 1:
            break

        smooth_data[outliers] = fitted_trend[outliers]
        outlier_idx = (outlier_idx | outliers)

    return fitted_trend, outlier_idx


def recurring_outliers(data, recurrence):
    outlier_eval = []
    for channel in data.keys():
        outlier_idx = data[channel]['outliers']
        outlier_eval.append(outlier_idx)

    outlier_eval = np.array(outlier_eval, dtype=bool)
    n_chan, n_ts = outlier_eval.shape
    outlier_idx = (outlier_eval.sum(axis=0)/float(n_chan) >= recurrence)

    return outlier_idx


if __name__ == '__main__':

    args = main.cli_outliers()

    [chan_vel,
     timestamps,
     spectra,
     ts_jd] = io.input(args.filename,
                       epoch=args.epoch,
                       tsformat=args.tsformat)

    if args.channel is None:
        # choose 5 strongest signal channels
        channels = spectra.max(axis=0).argsort()[-5:]
    else:
        channels = args.channel

    clean_data = {}
    for channel in channels:
        # remove outliers
        [fitted_trend,
         outliers_idx] = clean_channel(ts_jd.value,
                                       spectra[:, channel],
                                       window=args.win,
                                       niter=args.niter,
                                       method=args.method)
        clean_data[channel] = {'velocity': chan_vel[channel],
                               'smooth': fitted_trend,
                               'outliers': outliers_idx}

    recurrent_outlier_idx = None
    if args.recurrence is not None:
        recurrent_outlier_idx = recurring_outliers(clean_data,
                                                   args.recurrence)

    fig = display.show_fit(ts_jd.datetime,
                           spectra[:, channels],
                           process=clean_data,
                           outliers=recurrent_outlier_idx,
                           channels=channels)
    if args.save:
        outfile = os.path.basename(args.filename)
        outfile = '{}_channel_{}'.format(outfile, channel)
        outfile = outfile.replace('.', '_')
        plt.savefig('{}_outliers.png'.format(outfile),
                    bbox_inches='tight')

    if args.verbose:
        plt.show()

# -fin-
