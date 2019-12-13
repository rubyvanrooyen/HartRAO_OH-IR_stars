#!/usr/bin/env python
from __future__ import print_function

from oh_ir import detrend, display, main, io
import argparse
import matplotlib.pylab as plt
import numpy as np
import os


def cli():
    usage = "%(prog)s [options]"
    description = 'detrend data using low order polynomial fit'
    # parser for detrending functionality
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            '--poly',
            type=int,
            default=2,
            help='order of fitted polynomial')
    # add common arguments
    main.cli_common(parser)

    args = parser.parse_args()
    if args.channel is None:
        msg = 'Specify channel data to detrend for analysis output'
        raise RuntimeError(msg)

    return args


def show_fit(ts_jd, flux, ffit, baseflux):
    fig = plt.subplots(figsize=(15, 7),
                       facecolor='white')
    ax = plt.subplot(111)
    fig, ax = display.timeseries(ts_jd.datetime,
                                 flux,
                                 color='k',
                                 marker='.',
                                 linestyle='--',
                                 alpha=0.3,
                                 fig=fig,
                                 ax=ax,
                                 )
    fig, ax = display.timeseries(ts_jd.datetime,
                                 ffit(ts_jd.unix),
                                 color='k',
                                 marker='',
                                 linestyle='-',
                                 alpha=0.6,
                                 fig=fig,
                                 ax=ax,
                                 )
    fig, ax = display.timeseries(ts_jd.datetime,
                                 baseflux,
                                 color='b',
                                 marker='.',
                                 linestyle='--',
                                 alpha=0.3,
                                 fig=fig,
                                 ax=ax,
                                 )
    ax.set_xlabel('date')
    ax.set_ylabel('channel flux [Jy]')
    ax.set_title('{}'.format(ffit))


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

    detrended_spectra = np.array([])
    for channel in args.channel:
        flux = spectra[:, channel]

        ffit = detrend.polyfit(ts_jd.unix,
                               flux,
                               args.poly)
        base_flux = flux - ffit(ts_jd.unix)
        show_fit(ts_jd, flux, ffit, base_flux)
        base_flux = base_flux.reshape(len(base_flux), 1)
        if len(detrended_spectra) < 1:
            detrended_spectra = base_flux
        else:
            detrended_spectra = np.hstack([detrended_spectra, base_flux])

        if args.save:
            outfile = os.path.basename(args.filename)
            outfile = '{}_channel_{}'.format(outfile, channel)
            outfile = outfile.replace('.', '_')
            plt.savefig('{}_detrend.png'.format(outfile),
                        bbox_inches='tight')

    if args.save:
        outfile = os.path.basename(args.filename)
        [name, ext] = os.path.splitext(outfile)
        filename = '{}_detrend{}'.format(
                name, ext)
        header = '{}\n'.format(name)
        header += 'MJD,  {},\n'.format(
                ',  '.join([str(vel) for vel in chan_vel[args.channel]]))
        timestamps = ts_jd.value
        io.output(filename, header, timestamps, detrended_spectra)

    if args.verbose:
        plt.show()


# -fin-
