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
Extracted data must contain only the selected red and blue peak information for phase lag
calculations.

