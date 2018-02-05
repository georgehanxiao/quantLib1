# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:46:25 2018

@author: 44100521
"""
from QuantLib import *

# global data
calendar = TARGET()
todaysDate = Date(6,November,2001);
Settings.instance().evaluationDate = todaysDate
settlementDate = Date(8,November,2001);

# market quotes
deposits = { (1,Weeks): 0.0382,
             (1,Months): 0.0372,
             (3,Months): 0.0363,
             (6,Months): 0.0353,
             (9,Months): 0.0348,
             (1,Years): 0.0345 }

FRAs = { (3,6): 0.037125,
         (6,9): 0.037125,
         (9,12): 0.037125 }

futures = { Date(19,12,2001): 96.2875,
            Date(20,3,2002): 96.7875,
            Date(19,6,2002): 96.9875,
            Date(18,9,2002): 96.6875,
            Date(18,12,2002): 96.4875,
            Date(19,3,2003): 96.3875,
            Date(18,6,2003): 96.2875,
            Date(17,9,2003): 96.0875 }

swaps = { (2,Years): 0.037125,
          (3,Years): 0.0398,
          (5,Years): 0.0443,
          (10,Years): 0.05165,
          (15,Years): 0.055175 }


# convert them to Quote objects
for n,unit in deposits.keys():
    deposits[(n,unit)] = SimpleQuote(deposits[(n,unit)])
for n,m in FRAs.keys():
    FRAs[(n,m)] = SimpleQuote(FRAs[(n,m)])
for d in futures.keys():
    futures[d] = SimpleQuote(futures[d])
for n,unit in swaps.keys():
    swaps[(n,unit)] = SimpleQuote(swaps[(n,unit)])
    
# build rate helpers

dayCounter = Actual360()
settlementDays = 2
depositHelpers = [ DepositRateHelper(QuoteHandle(deposits[(n,unit)]),
                                     Period(n,unit), settlementDays,
                                     calendar, ModifiedFollowing,
                                     False, dayCounter)
                   for n, unit in [(1,Weeks),(1,Months),(3,Months),
                                   (6,Months),(9,Months),(1,Years)] ]

dayCounter = Actual360()
settlementDays = 2
fraHelpers = [ FraRateHelper(QuoteHandle(FRAs[(n,m)]),
                             n, m, settlementDays,
                             calendar, ModifiedFollowing,
                             False, dayCounter)
               for n, m in FRAs.keys() ]

dayCounter = Actual360()
months = 3
futuresHelpers = [ FuturesRateHelper(QuoteHandle(futures[d]),
                                     d, months,
                                     calendar, ModifiedFollowing,
                                     True, dayCounter,
                                     QuoteHandle(SimpleQuote(0.0)))
                   for d in futures.keys() ]

settlementDays = 2
fixedLegFrequency = Annual
fixedLegTenor = Period(1,Years)
fixedLegAdjustment = Unadjusted
fixedLegDayCounter = Thirty360()
floatingLegFrequency = Semiannual
floatingLegTenor = Period(6,Months)
floatingLegAdjustment = ModifiedFollowing
swapHelpers = [ SwapRateHelper(QuoteHandle(swaps[(n,unit)]),
                               Period(n,unit), calendar,
                               fixedLegFrequency, fixedLegAdjustment,
                               fixedLegDayCounter, Euribor6M())
                for n, unit in swaps.keys() ]

# term structure handles

discountTermStructure = RelinkableYieldTermStructureHandle()
forecastTermStructure = RelinkableYieldTermStructureHandle()

# term-structure construction

helpers = depositHelpers[:2] + futuresHelpers + swapHelpers[1:]
depoFuturesSwapCurve = PiecewiseFlatForward(settlementDate, helpers,
                                            Actual360())

helpers = depositHelpers[:3] + fraHelpers + swapHelpers
depoFraSwapCurve = PiecewiseFlatForward(settlementDate, helpers, Actual360())

tab = " " * 8

#print(tab + "5-years swap paying %s" % formatRate(fixedRate))

for yrs in depoFuturesSwapCurve.times():
    print ("%s\t%s" % (yrs,depoFuturesSwapCurve.discount(yrs)))
    #print ("%s\t" %yrs)
    
    
    
    
    
    
    
    
    
    