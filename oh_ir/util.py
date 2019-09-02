from __future__ import print_function

from astropy.time import Time

import astropy.stats as stats
import numpy as np

def ts2datetime(timestamps, epoch=0., tsformat='mjd'):
    return Time(timestamps + epoch, format=tsformat)


def ls_periodogram(ts_jd, values):
    ls = stats.LombScargle(ts_jd.value, values)
    frequency, power = ls.autopower()
    period = 1./frequency # period is the inverse of frequency
    # period with most power / strongest signal
    best_period = 1./frequency[np.argmax(power)]
    best_freq = frequency[np.argmax(power)]
    return [period, frequency, power, best_period, best_freq]

# -fin-
