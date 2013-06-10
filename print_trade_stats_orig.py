#!/usr/bin/env python

"""
Extract and print original trades data stats.
"""

import csv, datetime, re, sys
import numpy as np

trade_volume_total = 0
num_trades = 0
trade_price_mean = 0.0
trade_price_std = 0.0
with open(sys.argv[1], 'r') as f:
    for row in csv.reader(f):
        if re.match('.*9/14.*', row[3]):

            # Exit loop when specified time bound reached:
            if len(sys.argv) > 2:
                if datetime.datetime.strptime(row[4], '%H:%M:%S.%f') >= \
                  datetime.datetime.strptime(sys.argv[2], '%H:%M:%S.%f'):
                    break
            trade_volume_total += int(row[11])
            num_trades += 1
            if num_trades == 1:
                trade_price_mean += float(row[10])
            else:

                # mean[n] = (mean[n-1]*(n-1)+x[n])/n
                trade_price_mean = \
                  (trade_price_mean*(num_trades-1)+float(row[10]))/num_trades

                # std[n] = sqrt((std[n-1]**2*(n-1)+(x[n]-mean[n])**2)/n)
                trade_price_std = \
                  np.sqrt((trade_price_std**2*(num_trades-1)+(float(row[10])-trade_price_mean)**2)/num_trades)

print 'total trade volume: ', trade_volume_total
print 'number of trades: ', num_trades
print 'trade price mean:', trade_price_mean
print 'trade price STD:', trade_price_std
