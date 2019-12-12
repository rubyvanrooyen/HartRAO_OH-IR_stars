#!/usr/bin/env python

from __future__ import print_function

import matplotlib.pylab as plt
import numpy as np
import os

from oh_ir import io, util, periodogram
from oh_ir import main, display


if __name__ == '__main__':

    args = main.cli_periodogram()
    [chan_vel, timestamps, spectra] = io.readfile(args.filename)
    ts_jd = util.ts2datetime(timestamps,
                             epoch=args.epoch,
                             tsformat=args.tsformat)

    if args.channel is None:
        if args.verbose:
            msg = ('No channels selected for display, '
                   'add --channel argument')
            raise RuntimeError(msg)
        channels = range(len(chan_vel))
    else:
        channels = args.channel

    fig = None
    ax = None
    for channel in channels:
        flux = spectra[:, channel]

        # fit line to subtract additive functional equation
        coefs = np.polynomial.polynomial.polyfit(ts_jd.unix,
                                                 flux, 1)
        ffit = np.poly1d(coefs[::-1])
        base_flux = flux - ffit(ts_jd.unix)

        # get period of data
        [period,
         frequency,
         power,
         best_period,
         best_freq] = periodogram.lomb_scargle(ts_jd.unix,
                                               base_flux)

        # output to display
        chan_period = 'Data period = {:.3f} seconds'.format(best_period)
        chan_frequency = 'Data frequency = {:.3e} Hz'.format(best_freq)

        # output to display
        chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])
        chan_period = 'Data period = {:.3f} days'.format(best_period/(24.*3600.))
        output_str = 'Selected channel: {}\n'.format(channel)
        output_str += '  {}\n'.format(chan_velocity)
        output_str += '  {}\n'.format(chan_period)
        print(output_str)

    #     if args.save:
    #         outfile = os.path.basename(args.filename)
    #         outfile = '{}_channel_{}'.format(outfile, channel)
    #         outfile = outfile.replace('.', '_')

        if args.verbose:
            if ax is None:
                fig, ax = display.timeseries(ts_jd.datetime,
                                             base_flux,
                                             label=chan_velocity,
                                             color='b')
            else:
                fig, ax = display.timeseries(ts_jd.datetime,
                                             base_flux,
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
                                                  base_flux,
                                                  best_period,
                                                  best_freq)
            fig_, ax_ = display.folded_phase(best_period*phase/(24.*3600.),
                                             base_flux,
                                             best_period*phase_fit/(24.*3600.),
                                             mag_fit,
                                             fig=fig_,
                                             ax=ax_)

    #     if args.save:
    #         plt.savefig('{}_periodogram.png'.format(outfile),
    #                     bbox_inches='tight')

    #         if args.save:
    #             plt.savefig('{}_folded.png'.format(outfile),
    #                         bbox_inches='tight')

    if args.verbose or args.phase:
        plt.show()

# -fin-
