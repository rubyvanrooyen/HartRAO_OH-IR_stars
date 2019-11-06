from __future__ import print_function

from oh_ir import io, util
from oh_ir import main

# import matplotlib.pylab as plt
# 
# def cli():
#     parser.add_argument(
#             '--filename',
#             type=str,
#             required=True,
#             help='name of HartRAO observation file containing timestamps and channel data')
#     ts_formats = ['jd', 'mjd']
#     parser.add_argument(
#             '--tsformat',
#             type=str,
#             default='mjd',
#             choices=ts_formats,
#             help='mjd ts assuming 1900 epoch, or modified jd = ts-epoch')
# 
#     parser.add_argument(
#             '--epoch',
#             type=int,
#             default=0.,
#             help='epoch for modified jd = ts-epoch')
#     parser.add_argument(
#             '--channel',
#             type=int,
#             nargs='+',
#             help='specific channels of interest')
#     parser.add_argument(
#             '--period',
#             action='store_true',
#             help='find period using LS periodogram calculation')
# 
# 
# 
if __name__ == '__main__':

    args = main.cli_periodogram()
#     [chan_vel, timestamps, spectra] = io.readfile(args.filename)
#     ts_jd = util.ts2datetime(timestamps,
#                              epoch=args.epoch,
#                              tsformat=args.tsformat)
# 
#     if args.channel is None:
#         channels = range(len(chan_vel))
#     else:
#         channels = args.channel
# 
#     for channel in channels:
#         chan_data = spectra[:, channel]
# 
# 
#         fig= plt.subplots(figsize=(17,3),
#                           facecolor='white')
#         ax = plt.subplot(111)
#         ax.plot(ts_jd.datetime,
#                 chan_data,
#                 'b.',
#                 label=r'Line velocity {} km/s'.format(chan_vel[channel]))
#         ax.legend(loc=0)
#         ax.set_ylabel('Flux density [Jy]')
#         ax.set_xlabel('Timestamp')
# 
#         if args.period:
#             [period,
#              frequency,
#              power,
#              best_period,
#              best_freq] = util.ls_periodogram(ts_jd,
#                                               chan_data - chan_data.mean())
#             fig= plt.subplots(figsize=(10,7),
#                               facecolor='white')
#             ax = plt.subplot(111)
#             ax.plot(period,power)
#             ax.axvline(best_period, color='r',linestyle=':');
#             ax.set_xlabel('period (days)')
#             ax.set_ylabel('relative power')
#             ax.text(0.03, 0.93,
#                     'period = {:.3f} days'.format(best_period),
#                     transform=ax.transAxes,
#                     color='r')
# 
# 
#     plt.show()


# -fin-
