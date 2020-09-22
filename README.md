# HartRAO_OH-IR_stars
Time series analysis of HartRAO OH-IR monitoring data

## Input data format
The notebooks presented will assume time series data from the HartRAO OH monitoring program.   
OH monitoring data files are comma separated (CSV) ASCII files tabulating the observed data.

The files have the following structure:    
* Line 0: a human readable string for information
* Line 1: a header line containing the timestamps followed by the channel velocities per column
* Line 2-N: time series data with a time stamp in the format indicated by the header in the first
  column, followed by the per channel spectra value

Layout of data per row:
* First column is timestamps in MJD / (JD - epoch)
* Remaining columns are spectral channels

Example data files for 2 mira variables (IKTau and VMic) can be found in this repo.

## Data extraction and processing
Extracted data must contain only the date in MJD/JD format and the two selected red and blue peak information for phase lag
calculations.

First the data can be detrended to remove long term slow trend present in the data that will aid
period and cross correlation calculations which will remove the mean of the data for numerical
calculation.

Followed by the periodogram calculation using the Lomb-Scargle algorithm.
Once a period is calculated and the false positive evaluation shows reasonable certainty of a single
period in the time series data, the calculated period can be used for cross correlation to obtain the
phase difference between the time series signals of the red and blue channels.

For better visualisation of the data over the period, a folded phase plot is also provided.

