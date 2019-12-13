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
    colors = ['b', 'r']
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
               alpha=1.,
               fig=None,
               ax=None,
               ):
    if ax is None:
        fig = plt.subplots(figsize=(17, 5),
                           facecolor='white')
        ax = plt.subplot(111)
    ax.plot(xdata,
            ydata,
            color=color,
            marker=marker,
            ls=linestyle,
            alpha=alpha,
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

# -fin-
