# Calculate best period from cyclic input data
from __future__ import print_function

import matplotlib.pylab as plt


def inputdata(chan_velocity,
              mean_spectrum,
              datetime,
              timeseries):
    n_ts, n_data = timeseries.shape
    fig, ax = plt.subplots(figsize=(17, 9),
                           nrows=2,
                           ncols=1,
                           facecolor='white')
    ax[0].plot(chan_velocity,
               mean_spectrum,
               'k--')
    ax[0].set_xlabel('velocity [km/s]')
    ax[0].set_ylabel('avg flux [Jy]')
    colors = ['b', 'r', 'k']
    for idx in range(n_data):
        ydata = timeseries[:, idx]
        ax[1].plot(datetime,
                   ydata,
                   color=colors[idx],
                   marker='.',
                   linestyle='-')
        ax[1].set_xlabel('date')
        ax[1].set_ylabel('avg flux [Jy]')

    return fig, ax


def timeseries(xdata,
               ydata,
               label=None,
               color='k',
               marker='.',
               linestyle=':',
               fig=None,
               ax=None,
               ):
    if ax is None:
        fig = plt.subplots(figsize=(17, 5),
                           facecolor='white')
        ax = plt.subplot(111)
    ax.plot(xdata,
            ydata,
            c=color,
            marker=marker,
            ls=linestyle,
            label=label)

    if label is not None:
        ax.legend(loc=0)

    return fig, ax


def periodogram(period,  # days
                power,
                best_period=None,  # days
                color='k',
                marker='',
                linestyle='-',
                fig=None,
                ax=None,
                ):
    if ax is None:
        fig = plt.subplots(figsize=(10, 7),
                           facecolor='white')
        ax = plt.subplot(111)
    ax.plot(period, power,
            color=color,
            marker=marker,
            linestyle=linestyle,
            alpha=0.3)
    if best_period is not None:
        ax.axvline(best_period, color='r', linestyle=':')
        ax.text(0.03, 0.93,
                'period = {:.3f} days'.format(best_period),
                transform=ax.transAxes,
                color='r')
    ax.set_xlabel('period (days)')
    ax.set_ylabel('relative power')

    return fig, ax


def folded_phase(phase,  # days
                 data,
                 phase_fit,
                 mag_fit,
                 color='k',
                 marker='',
                 linestyle='-',
                 fig=None,
                 ax=None,
                 ):
    if ax is None:
        fig = plt.subplots(figsize=(10, 7),
                           facecolor='white')
        ax = plt.subplot(111)
    ax.plot(phase, data,
            marker='.',
            ms=10,
            ls='none',
            lw=1,
            color='g',
            alpha=0.6)
    ax.plot(phase_fit, mag_fit)
    ax.set_xlabel('phase (days)')
    ax.set_ylabel('magnitude')

    return fig, ax


def show_fit(x,
             raw_y,
             process=None,
             outliers=None,
             channels=None):

    if channels is None:
        channels = [0]

    fig, ax = plt.subplots(nrows=len(channels),
                           ncols=1,
                           figsize=(17, 2*len(channels)),
                           sharex=True,
                           gridspec_kw={'hspace': 0},
                           facecolor='white')

    for cnt, channel in enumerate(channels):
        chan_data = raw_y[:, cnt]

        if process is None:
            label = 'channel {}'.format(channel)
        else:
            label = 'Line velocity {} km/s'.format(
                    process[channel]['velocity'])

        if len(channels) > 1:
            ax_cnt = ax[cnt]
        else:
            ax_cnt = ax

        ax_cnt.plot(x,
                    chan_data,
                    'b.',
                    label=label)
        if process is not None:
            chan_clean_data = process[channel]['smooth']
            if outliers is None:
                outlier_idx = process[channel]['outliers']
            else:
                outlier_idx = outliers
            ax_cnt.plot(x[outlier_idx],
                        chan_data[outlier_idx],
                        'r.')
            ax_cnt.plot(x, chan_clean_data, 'k-')
        ax_cnt.legend(loc=0)
        ax_cnt.set_ylabel('Flux density [Jy]')
        ax_cnt.set_xlabel('Timestamp')

    return fig
# -fin-
