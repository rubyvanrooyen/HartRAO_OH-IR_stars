from __future__ import print_function

import numpy as np

def readfile(filename):
    with open(filename, 'r') as fin:
        # human readable string for information
        comment = fin.readline()
        # timestamps [channel velocities]
        header = fin.readline()
        data = fin.readlines()

    chan_vel = np.array(header.strip().split(',')[1:-1], dtype=float)

    for cntr, line in enumerate(data):
        if cntr < 1:
            file_data = np.array(line.strip().split(',')[:-1], dtype=float)
        else:
            file_data = np.vstack([file_data, np.array(line.strip().split(',')[:-1], dtype=float)])

    timestamps = file_data[:,0]
    spectra = file_data[:,1:]

    return [chan_vel, timestamps, spectra]

# -fin-
