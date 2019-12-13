#!/usr/bin/env python

from __future__ import print_function

import argparse
import matplotlib.pylab as plt
import numpy as np
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


# assume matrix [ts, ch]
def avg_spectrum(spectra, channel, threshold=0.9):
    avg_spectra = spectra.mean(axis=0)
    spectrum = spectra[:, channel]
    if (avg_spectra[channel-1]/avg_spectra[channel]) > threshold:
        spectrum = np.vstack([spectra[:, channel-1], spectrum])
    if (avg_spectra[channel+1]/avg_spectra[channel]) > threshold:
        spectrum = np.vstack([spectrum, spectra[:, channel+1]])
    if len(spectrum.shape) > 1:
        spectrum = spectrum.mean(axis=0)
    return [avg_spectra, spectrum]


if __name__ == '__main__':
    args = cli()

    # read input data assuming HartRAO format
    [_,
     chan_vel,
     timestamps,
     spectra,
     ts_jd] = io.input(args.filename,
                       epoch=args.epoch,
                       tsformat=args.tsformat)

    # red and blue shifted channels are found if not given
    avg_spectra = spectra.mean(axis=0)
    if args.channel is None:
        cen_channel = len(chan_vel)//2
        blue_ch = np.argmax(avg_spectra[:cen_channel])
        red_ch = cen_channel + np.argmax(avg_spectra[cen_channel:])
    else:
        [blue_ch, red_ch] = args.channel

    # average a couple of channels around peak if flat max
    [avg_spectra,
     blue_spectrum] = avg_spectrum(spectra, blue_ch)
    [_, red_spectrum] = avg_spectrum(spectra, red_ch)

    channels = [blue_ch, red_ch]
    show_spectra = np.vstack([blue_spectrum, red_spectrum]).T

    outfile = os.path.basename(args.filename)
    outfile = '{}_channels_{}'.format(
            outfile, '_'.join([str(chan) for chan in channels]))
    outfile = outfile.replace('.', '_')

    labels = []
    for channel in channels:
        chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])
        labels.append(chan_velocity)
        print('Channel {}\n{}'.format(channel, chan_velocity))
    fig, ax = display.inputdata(chan_vel,
                                avg_spectra,
                                ts_jd.datetime,
                                show_spectra)
    ax[0].set_title(outfile)
    ax[1].legend(labels,
                 loc='upper center',
                 bbox_to_anchor=(0.5, 1.05),
                 ncol=3,
                 numpoints=1,
                 fancybox=True,
                 shadow=True)

    if args.save:
        plt.savefig('{}.png'.format(outfile), bbox_inches='tight')
    else:
        plt.show()

# -fin-
