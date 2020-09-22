from __future__ import print_function

import astropy.timeseries as stats
import numpy as np


def upsample(ts_start, ts_end, dt):
    upsample_time = [ts_start]
    while upsample_time[-1] < ts_end:
        next_time = upsample_time[-1] + dt
        upsample_time.append(next_time)
    return upsample_time


def lomb_scargle(timestamps, timeseries, dt=None):
    ls_hndl = stats.LombScargle(timestamps, timeseries,
                                fit_mean=True, center_data=True,
                                nterms=1,
                                )
    frequency, power = ls_hndl.autopower(method='slow',
                                         normalization='psd',
                                         nyquist_factor=2.*len(timeseries))
    # period with most power / strongest signal
    period = 1. / frequency[np.argmax(power)]

    # de-noise and smooth
    if dt is not None:
        model_time = upsample(timestamps[0], timestamps[-1], dt)
        model_timeseries = ls_hndl.model(model_time, frequency[np.argmax(power)])
    else:
        model_time = timestamps
        model_timeseries = ls_hndl.model(timestamps, frequency[np.argmax(power)])
    return [power, frequency, period, model_time, model_timeseries]


# Fold the observation times with the best period of the variable signal.
def ls_fold_phase(ts_jd, values, period, frequency):
    # light curve over period, take the remainder
    # (i.e. the "phase" of one period)
    # phase = (ts_jd.value / period) % 1
    phase = (ts_jd / period) % 1

    # compute model fitted values
    phase_fit = np.linspace(0., 1., len(ts_jd))
    mag_fit = stats.LombScargle(ts_jd,
                                values).model(t=phase_fit / frequency,
                                              frequency=frequency)
    return [phase, phase_fit, mag_fit]

# -fin-
