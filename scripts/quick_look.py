#!/usr/bin/env python

from __future__ import print_function

import argparse
import matplotlib.pylab as plt
import os

from oh_ir import display, io, main


def cli():
    usage = "%(prog)s [options]"
    description = 'quick display of input data'
    # parser for periodogram script
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    main.cli_common(parser)
    return parser.parse_args()


if __name__ == '__main__':
    args = cli()

    [chan_vel,
     timestamps,
     spectra,
     ts_jd] = io.input(args.filename,
                       epoch=args.epoch,
                       tsformat=args.tsformat)

    if args.channel is None:
        for channel in range(len(chan_vel)):
            print('Channel {} has line velocity {} km/s'.format(
                channel, chan_vel[channel]))
        quit()
    else:
        channels = args.channel

    for channel in channels:
        chan_data = spectra[:, channel]

        chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])
        fig, ax = display.inputdata(chan_vel,
                                    spectra.mean(axis=0),
                                    ts_jd.datetime,
                                    spectra.mean(axis=1),
                                    label=chan_velocity)
        if args.save:
            outfile = os.path.basename(args.filename)
            outfile = '{}_channel_{}'.format(outfile, channel)
            outfile = outfile.replace('.', '_')
            plt.savefig('{}.png'.format(outfile), bbox_inches='tight')
        else:
            plt.show()

# -fin-
