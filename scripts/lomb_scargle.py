#!/usr/bin/env python

from __future__ import print_function

import argparse
import math
import matplotlib.pylab as plt
import numpy as np
import os
import sys

from oh_ir import io, util, periodogram
from oh_ir import main, display


# width defines bar width
# percent defines current percentage
def progress(niter, width, percent):
    marks = math.floor(width * (percent / 100.0))
    spaces = math.floor(width - marks)

    loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'

    sys.stdout.write("%d %s %d%% iterations left\r" %
                     (niter, loader, percent))
    if percent >= 100:
        sys.stdout.write("\n")
    sys.stdout.flush()


def best_fit_period(timestamps,
                    flux,
                    start_period,
                    end_period,
                    nr_period=3600):  # day
    period_range = np.arange(start_period, end_period, nr_period)
    errs = []
    for idx, the_period in enumerate(period_range):
        progress(float(idx), 50, (float(idx)/float(len(period_range))*100.))
        [phase,
         phase_fit,
         mag_fit] = periodogram.ls_fold_phase(timestamps,
                                              flux,
                                              the_period,
                                              1./the_period)
        err = flux[np.argsort(phase)]-mag_fit
        err = np.sqrt(np.sum(err**2)/len(flux))  # rms
        errs.append(err)
    # dummy print for progress
    print()

    best_period = period_range[np.argmin(errs)]
    return best_period


def cli():
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
    parser.add_argument(
            '--bestfit',
            action='store_true',
            help='evaluate folding over a period range to find best fit')
    parser.add_argument(
            '--step',
            type=float,
            default=360.,
            help='epoch for modified jd = ts - epoch')
    # add common output arguments
    main.cli_common(parser)
    return parser.parse_args()


if __name__ == '__main__':

    args = cli()
    [_, chan_vel, timestamps, spectra] = io.readfile(args.filename)
    ts_jd = util.ts2datetime(timestamps,
                             epoch=args.epoch,
                             tsformat=args.tsformat)

    if args.channel is None:
        channels = range(len(chan_vel))
    else:
        channels = args.channel

    fig = None
    ax = None
    for channel in channels:
        flux = spectra[:, channel]

        # get period of data
        [period,
         frequency,
         power,
         best_period,
         best_freq] = periodogram.lomb_scargle(ts_jd.unix,
                                               flux)

        if args.bestfit:
            # get better fit of period
            fitted_period = best_fit_period(ts_jd.unix,
                                            flux,
                                            best_period/2.,
                                            2.*best_period,
                                            args.step,
                                            )
            best_period = fitted_period
            best_freq = 1./fitted_period

        # output to display
        chan_period = 'Data period = {:.3f} seconds'.format(best_period)
        chan_frequency = 'Data frequency = {:.3e} Hz'.format(best_freq)

        # output to display
        chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])
        chan_period_sec = 'Data period = {} sec'.format(best_period)
        best_period_day = best_period/(24.*3600.)
        chan_period_day = 'Data period = {:.3f} days'.format(best_period_day)
        output_str = 'Selected channel: {}\n'.format(channel)
        output_str += '  {}\n'.format(chan_velocity)
        output_str += '  {}\n'.format(chan_period_sec)
        output_str += '  {}\n'.format(chan_period_day)
        print(output_str)

        if args.save:
            outfile = os.path.basename(args.filename)
            outfile = '{}_channel_{}'.format(outfile, channel)
            outfile = outfile.replace('.', '_')

        if args.verbose:
            if ax is None:
                fig, ax = display.timeseries(ts_jd.datetime,
                                             flux,
                                             label=chan_velocity,
                                             color='b')
            else:
                fig, ax = display.timeseries(ts_jd.datetime,
                                             flux,
                                             label=chan_velocity,
                                             color='r',
                                             fig=fig,
                                             ax=ax)
            ax.set_ylabel('Flux density [Jy]')
            ax.set_xlabel('Timestamp')

        if args.phase:
            fig_ = plt.subplots(figsize=(15, 7),
                                facecolor='white')
            ax_ = plt.subplot(121)
        else:
            fig_ = plt.subplots(figsize=(10, 7),
                                facecolor='white')
            ax_ = plt.subplot(111)
        fig_, ax_ = display.periodogram(period/(24.*3600.),
                                        power,
                                        best_period=best_period/(24.*3600.),
                                        fig=fig_,
                                        ax=ax_)
        ax_.set_title(chan_velocity)

        if args.phase:
            ax_ = plt.subplot(122)
            # Plot folded lightcurve
            [phase,
             phase_fit,
             mag_fit] = periodogram.ls_fold_phase(ts_jd.unix,
                                                  flux,
                                                  best_period,
                                                  best_freq)
            fig_, ax_ = display.folded_phase(best_period*phase/(24.*3600.),
                                             flux,
                                             best_period*phase_fit/(24.*3600.),
                                             mag_fit,
                                             fig=fig_,
                                             ax=ax_)

        if args.save:
            plt.savefig('{}_periodogram.png'.format(outfile),
                        bbox_inches='tight')
            if args.phase:
                plt.savefig('{}_folded.png'.format(outfile),
                            bbox_inches='tight')

    if args.verbose or args.phase:
        plt.show()

# -fin-
