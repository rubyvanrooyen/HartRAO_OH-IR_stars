from __future__ import print_function

from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter as savitzky_golay

import numpy as np


def polyfit(x, y, order):
    # fit line to subtract additive functional equation
    coefs = np.polynomial.polynomial.polyfit(x, y, order)
    ffit = np.poly1d(coefs[::-1])
    return ffit


def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def smoothing_spline(ts,
                     data,
                     step=None,
                     win=None):
    x = ts.copy()
    y = data.copy()

    start = x.min()
    stop = x.max()
    if step is None:
        step = int(np.diff(x).mean())
    xx = np.arange(start, stop, step)

    if win is not None:
        x = running_mean(x, win)
        y = running_mean(y, win)

    spl = UnivariateSpline(x, y)
    spl.set_smoothing_factor(0.9)

    yy = spl(xx)
    spline_fit = []
    for t in ts:
        idx = np.abs(xx-t).argmin()
        spline_fit.append(yy[idx])

    return np.array(spline_fit)


def smooth(timestamps,
           data,
           window=21,
           order=3,
           sigma=3.,
           method='sg'):
    if method == 'sg':
        # apply a Savitzky-Golay filter to an array.
        fitted_trend = savitzky_golay(data,
                                      int(window),
                                      int(order))
    else:
        # use a running mean to compute smoothed values to fit
        fitted_trend = smoothing_spline(timestamps,
                                        data,
                                        win=window)
        # edges for splines are bad since it cannot extrapolate
        fitted_trend[:window] = data[:window]
        fitted_trend[-window:] = data[-window:]

    detrended = data - fitted_trend
    threshold = np.mean(detrended) + sigma*np.std(detrended)
    outliers = np.abs(detrended) > threshold

    return fitted_trend, outliers

# -fin-
