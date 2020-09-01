#!/usr/bin/env python

from __future__ import print_function

from astropy.time import Time

import astropy.stats as stats
import matplotlib.pylab as plt
import numpy as np
import sys


def ts2datetime(timestamps, epoch=0., tsformat='mjd'):
    return Time(timestamps + epoch, format=tsformat)


def readfile(filename):
    with open(filename, 'r') as fin:
        # human readable string for information
        comment = fin.readline()
        # column headers
        header = fin.readline()
        data = fin.readlines()

    for cntr, line in enumerate(data):
        if cntr < 1:
            file_data = np.array(line.strip().split(','), dtype=float)
        else:
            file_data = np.vstack([file_data, np.array(line.strip().split(','), dtype=float)])
    return file_data


def lomb_scargle(ts_jd, values):
    ls = stats.LombScargle(ts_jd, values)
    frequency, power = ls.autopower()
    period = 1./frequency  # period is the inverse of frequency
    # period with most power / strongest signal
    best_period = 1./frequency[np.argmax(power)]
    best_freq = frequency[np.argmax(power)]
    return [period, frequency, power, best_period, best_freq]


# Fold the observation times with the best period of the variable signal.
def ls_fold_phase(ts_jd, values, period, frequency):
    # light curve over period, take the remainder
    # (i.e. the "phase" of one period)
    phase = (ts_jd / period) % 1

    # compute model fitted values
    phase_fit = np.linspace(0., 1.)
    mag_fit = stats.LombScargle(ts_jd,
                                values).model(t=phase_fit/frequency,
                                              frequency=frequency)
    return [phase, phase_fit, mag_fit]


if __name__ == '__main__':

    filename = sys.argv[1]
    data = readfile(filename)
    timestamps = data[:, 0]
    ts_jd = ts2datetime(timestamps)
    flux = data[:, 1]
    spline = data[:, 2]
    err = data[:, 3]

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
     best_freq] = lomb_scargle(ts_jd.unix,
                               base_flux)
    # output to display
    chan_period = 'Data period = {:.3f} seconds'.format(best_period)
    chan_frequency = 'Data frequency = {:.3e} Hz'.format(best_freq)


    fig = plt.subplots(figsize=(10, 7),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(period, power)
    ax.axvline(best_period, color='r', linestyle=':')
    ax.text(0.03, 0.93,
            'period = {:.3f} days'.format(best_period/(24.*3600.)),
            transform=ax.transAxes,
            color='r')
    ax.set_xlabel('period (days)')
    ax.set_ylabel('relative power')

    # folded lightcurve
    [phase,
     phase_fit,
     mag_fit] = ls_fold_phase(ts_jd.unix,
                              base_flux,
                              best_period,
                              best_freq)
    fig = plt.subplots(figsize=(10, 7),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(best_period*phase, base_flux,
            marker='.', ms=10, ls='none', lw=1, color='g', alpha=0.6)
    ax.plot(best_period*phase_fit, mag_fit, 'k')
    ax.set_xlabel('phase (days)')
    ax.set_ylabel('magnitude')





    fig = plt.subplots(figsize=(15, 7),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(ts_jd.datetime, flux, 'k--', marker='.', alpha=0.3)
    ax.plot(ts_jd.datetime, ffit(ts_jd.unix), 'k', alpha=0.6)
    ax.set_xlabel('date')
    ax.set_ylabel('channel flux [Jy]')
    ax.set_title('{}'.format(ffit))

    ax.plot(ts_jd.datetime, base_flux, 'b--', marker='.', alpha=0.3)


    fig = plt.subplots(figsize=(17, 5),
                       facecolor='white')
    ax = plt.subplot(111)
    ax.plot(ts_jd.datetime, flux, 'k.')
    ax.plot(ts_jd.datetime, spline, 'r')

    plt.show()

# -fin-
