from __future__ import print_function

from astropy.time import Time


def ts2datetime(timestamps, epoch=0., tsformat='mjd'):
    return Time(timestamps + epoch, format=tsformat)

# -fin-
