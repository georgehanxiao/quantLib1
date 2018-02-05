# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:04:50 2018

@author: 44100521
"""

import QuantLib as ql
from pandas import DataFrame
import matplotlib.pyplot as plt
import csv

def get_spot_rates(yieldcurve, day_count, calendar=ql.UnitedStates(), months=121):
    spots = []
    tenors = []
    ref_date = yieldcurve.referenceDate()
    calc_date = ref_date
    for yrs in yieldcurve.times():
        d = calendar.advance(ref_date, ql.Period(int(yrs*365.25), ql.Days))
        compounding = ql.Compounded
        freq = ql.Semiannual
        zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
        tenors.append(round(yrs,8))
        eq_rate = zero_rate.equivalentRate(day_count,compounding,freq,calc_date,d).rate()
        spots.append(eq_rate*100)
    return DataFrame(list(zip(tenors, spots)),columns=["Maturities","Curve"],index=['']*len(tenors))

swap_maturities = [ql.Date(9,9,2016),
ql.Date(15,9,2016),
ql.Date(22,9,2016),
ql.Date(29,9,2016),
ql.Date(11,10,2016),
ql.Date(9,11,2016),
ql.Date(8,12,2016),
ql.Date(10,1,2017),
ql.Date(8,2,2017),
ql.Date(8,3,2017),
ql.Date(8,6,2017),
ql.Date(8,9,2017),
ql.Date(8,3,2018),
ql.Date(10,9,2018),
ql.Date(10,9,2019),
ql.Date(10,9,2020),
ql.Date(9,9,2021),
ql.Date(8,9,2022),
ql.Date(8,9,2023),
ql.Date(10,9,2024),
ql.Date(10,9,2025),
ql.Date(10,9,2026),
ql.Date(8,9,2028),
ql.Date(10,9,2031),
ql.Date(10,9,2036),
ql.Date(10,9,2041),
ql.Date(10,9,2046),
ql.Date(8,9,2056)
]

swap_periods = [ql.Period(1,ql.Days),
ql.Period(1,ql.Weeks),
ql.Period(2,ql.Weeks),
ql.Period(3,ql.Weeks),
ql.Period(1,ql.Months),
ql.Period(2,ql.Months),
ql.Period(3,ql.Months),
ql.Period(4,ql.Months),
ql.Period(5,ql.Months),
ql.Period(6,ql.Months),
ql.Period(9,ql.Months),
ql.Period(1,ql.Years),
ql.Period(18,ql.Months),
ql.Period(2,ql.Years),
ql.Period(3,ql.Years),
ql.Period(4,ql.Years),
ql.Period(5,ql.Years),
ql.Period(6,ql.Years),
ql.Period(7,ql.Years),
ql.Period(8,ql.Years),
ql.Period(9,ql.Years),
ql.Period(10,ql.Years),
ql.Period(12,ql.Years),
ql.Period(15,ql.Years),
ql.Period(20,ql.Years),
ql.Period(25,ql.Years),
ql.Period(30,ql.Years),
ql.Period(40,ql.Years)
]

swap_rates = [0.37,
0.4025,
0.4026,
0.399,
0.3978,
0.4061,
0.41,
0.4155,
0.4273,
0.4392,
0.461,
0.4805,
0.5118,
0.538,
0.587,
0.638,
0.7,
0.756,
0.818,
0.865,
0.913,
0.962,
1.045,
1.137,
1.2355,
1.281,
1.305,
1.346
]

""" Parameter Setup """
calc_date = ql.Date(1,9,2016)
ql.Settings.instance().evaluationDate = calc_date
calendar = ql.UnitedStates()
bussiness_convention = ql.ModifiedFollowing
day_count = ql.Actual365Fixed()
coupon_frequency = ql.Annual

""" SwapRateHelper """
swap_helpers = []
for rate,tenor in list(zip(swap_rates,swap_periods)):
    swap_helpers.append(ql.SwapRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100.0)),
        tenor, calendar,
        coupon_frequency, bussiness_convention,
        day_count,
        ql.Euribor3M()))

rate_helpers = swap_helpers
yc_linearzero = ql.PiecewiseLinearZero(calc_date,rate_helpers,day_count)
yc_cubiczero = ql.PiecewiseCubicZero(calc_date,rate_helpers,day_count)

max_maturity = 40*12

splz = get_spot_rates(yc_linearzero, day_count, months=max_maturity + 1)
spcz = get_spot_rates(yc_cubiczero, day_count, months=max_maturity + 1)

max_rate = swap_rates[-1]
min_rate = min(splz.Curve)
max_rate = max(splz.Curve)

"""Plotting"""
plt.plot(splz["Maturities"],splz["Curve"],'--', label="LinearZero")
plt.plot(spcz["Maturities"],spcz["Curve"],label="CubicZero")
plt.xlabel("Years", size=12)
plt.ylabel("Zero Rate", size=12)
plt.xlim(0,max_maturity/12.0)
plt.ylim([min_rate * 0.9,max_rate * 1.1])
plt.legend()

plt.show()

rows = zip(splz.Maturities,splz.Curve)

with open('OISBootstrap.csv','w',newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
