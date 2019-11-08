#!/usr/bin/env python

from __future__ import print_function

import matplotlib.pylab as plt
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

    for channel in channels:
        chan_data = spectra[:, channel]

        [period,
         frequency,
         power,
         best_period,
         best_freq] = periodogram.lomb_scargle(ts_jd,
                                               chan_data - chan_data.mean())

        # output to display
        chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])
        chan_period = 'Data period = {:.3f} days'.format(best_period)
        output_str = 'Selected channel: {}\n'.format(channel)
        output_str += '  {}\n'.format(chan_velocity)
        output_str += '  {}\n'.format(chan_period)
        print(output_str)

        if args.save:
            outfile = os.path.basename(args.filename)
            outfile = '{}_channel_{}'.format(outfile, channel)
            outfile = outfile.replace('.', '_')

        if args.verbose:
            fig, ax = display.timeseries(ts_jd.datetime,
                                         chan_data,
                                         label=chan_velocity)
            ax.set_ylabel('Flux density [Jy]')
            ax.set_xlabel('Timestamp')

        fig, ax = display.periodogram(period,
                                      power,
                                      best_period=best_period,
                                      label=chan_velocity)
        if args.save:
            plt.savefig('{}_periodogram.png'.format(outfile),
                        bbox_inches='tight')

        if args.phase:
            # Plot folded lightcurve
            [phase,
             phase_fit,
             mag_fit] = periodogram.ls_fold_phase(ts_jd,
                                                  chan_data - chan_data.mean(),
                                                  best_period,
                                                  best_freq)
            fig, ax = display.folded_phase(best_period*phase,
                                           chan_data - chan_data.mean(),
                                           best_period*phase_fit,
                                           mag_fit,
                                           label=chan_velocity)
            if args.save:
                plt.savefig('{}_folded.png'.format(outfile),
                            bbox_inches='tight')

    if args.verbose or args.phase:
        plt.show()

# -fin-
