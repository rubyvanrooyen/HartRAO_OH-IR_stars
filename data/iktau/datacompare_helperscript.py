#!/usr/bin/env python

# Compare multiple datasets,
# assuming all datasets have the same format and layout

from __future__ import print_function

from oh_ir import display, io, main
import argparse
import matplotlib.pylab as plt


def cli():
    usage = "%(prog)s [options]"
    description = 'overlay multiple datasets'
    parser = argparse.ArgumentParser(
            usage=usage,
            description=description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    main.cli_common_input(parser)
    group = parser.add_argument_group(
            title='comparison datasets',
            description='input data to over plot on main dataset')
    group.add_argument(
            '--compare',
            type=str,
            nargs='+',
            default=[],
            help='filename of additional HartRAO data files containing '
                 'timestamps and channel data')

    args = parser.parse_args()

    # this comparison script will require channels to compare
    if args.channel is None:
        raise RuntimeError('Please specify selected channels '
                           'for comparison, --channel')
    if len(args.compare) > 3:
        raise SystemExit('To many data sets, 3 sets maximum')

    return args


if __name__ == '__main__':
    args = cli()

    [chan_vel,
     timestamps,
     base_spectra,
     ts_jd] = io.input(args.filename,
                       epoch=args.epoch,
                       tsformat=args.tsformat)

    comp_spectra = []
    comp_jd = []
    for filename in args.compare:
        [_, _, spectra, jd] = io.input(filename,
                                       epoch=args.epoch,
                                       tsformat=args.tsformat)
        comp_spectra.append(spectra)
        comp_jd.append(jd)

    for channel in args.channel:
        chan_velocity = 'Line velocity {} km/s'.format(chan_vel[channel])

        base_spectrum = base_spectra[:, channel]
        fig, ax = display.timeseries(ts_jd.datetime,
                                     base_spectrum,
                                     label=chan_velocity)

        colors = ['r', 'b', 'g']
        for idx, spectrum in enumerate(comp_spectra):
            fig, ax = display.timeseries(comp_jd[idx].datetime,
                                         spectrum[:, channel],
                                         color=colors[idx],
                                         linestyle='',
                                         fig=fig,
                                         ax=ax)
        ax.set_xlabel('date')
        ax.set_ylabel('channel flux [Jy]')

    plt.show()


# -fin-
