from __future__ import print_function

import astropy.stats as stats
import numpy as np


def lomb_scargle(ts_jd, values):
    ls = stats.LombScargle(ts_jd.value, values)
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
    phase = (ts_jd.value / period) % 1

    # compute model fitted values
    phase_fit = np.linspace(0., 1.)
    mag_fit = stats.LombScargle(ts_jd.value,
                                values).model(t=phase_fit/frequency,
                                              frequency=frequency)
    return [phase, phase_fit, mag_fit]

# -fin-
