# Calculate best period from cyclic input data
from __future__ import print_function

import matplotlib.pylab as plt


def timeseries(xdata,
               ydata,
               label=None):
    fig = plt.subplots(figsize=(17, 3),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(xdata,
            ydata,
            'b.',
            label=label)

    if label is not None:
        ax.legend(loc=0)

    return fig, ax


def periodogram(period,  # days
                power,
                best_period=None,  # days
                label=None):
    fig = plt.subplots(figsize=(10, 7),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(period, power, label=label)
    if best_period is not None:
        ax.axvline(best_period, color='r', linestyle=':')
        ax.text(0.03, 0.93,
                'period = {:.3f} days'.format(best_period),
                transform=ax.transAxes,
                color='r')
    ax.set_xlabel('period (days)')
    ax.set_ylabel('relative power')

    if label is not None:
        ax.legend(loc=0)

    return fig, ax


def folded_phase(phase,
                 data,
                 phase_fit,
                 mag_fit,
                 label=None):
    fig = plt.subplots(figsize=(10, 7),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(phase, data, label=label,
            marker='.',
            ms=10,
            ls='none',
            lw=1,
            color='g',
            alpha=0.6)
    ax.plot(phase_fit, mag_fit)
    ax.set_xlabel('phase (days)')
    ax.set_ylabel('magnitude')

    if label is not None:
        ax.legend(loc=0)

    return fig, ax

# -fin-
