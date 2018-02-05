# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 17:18:09 2018

Pandas read file

@author: 44100521
"""

import pandas as pd
import os

os.getcwd()

os.chdir('C://Users/44100521/Documents/GMS Model Studies/NFOS Trades')

d= pd.read_table('NFOS_GMIS-003292_trades.txt',sep='|')
print (d.shape)
print (d.columns)

print (d['product_code'].unique())

#d.drop_duplicates(inplace=True)
print (d.shape)
print (d.head())
#d.to_excel('NFOS_GMIS-003292_trades.xlsx')

"""
Some other stats:

d2.groupby(['remaining_notional','deal_ccy'])['notional'].sum()[0]['USD']
d.groupby(['deal_ccy','deal_foreign_ccy'])['notional'].sum()

"""



