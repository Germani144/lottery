# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 20:56:15 2020

@author: Pedro Germani
"""

import pandas as pd
from pyquery import PyQuery as pq

years = [*range(2012,2022,1)]
initStr = 'To view more information about a particular draw simply click on the draw date, where you will find more in-depth jackpot and prize data.\nLast Six Months › 2021 Results › 2020 Results › 2019 Results › 2018 Results › 2017 Results › 2016 Results › 2015 Results › 2014 Results › 2013 Results › 2012 Results ›\n\nDate\nResults\nJackpot:'
endStr = '\n\n\n#fourAcross {position: relative; width: 960px; margin: 20px auto -190px; overflow: hidden; z-index: 3; padding: 0 ;}\nFree Danske Lotto Apps › Results Checker › Number Generator › Play Casino Games ›\nDanske Lotto Results\n\n\nViking Lotto Results\n\n\nEuroJackpot Results\n\n\nCasino Games\nCookie Policy\n\nSe denne side på dansk »\n\n\n\n\nMaterial Copyright © 2021 DanskeLotto.com. All rights reserved.'
docs = []

for year in years:
    url = 'https://www.danskelotto.com/en/results/eurojackpot-results-'+str(year)
    doc = pq(url=url).text()
    start = doc.index(initStr)
    end = doc.index(endStr)
    doc = doc[start+len(initStr)+1:end].split()
    doc = [e for e in doc if e not in ('Rollover','›','Kr.')]
    docs.append(doc)

Month = []
Day = []
Year = []
n1 = []
n2 = []
n3 = []
n4 = []
n5 = []
n6 = []
s1 = []
s2 = []
Prize = []

for doc in docs:
    for i in range(int(len(doc)/11)):
        Month.append(doc[0+11*i])
        Day.append(int(doc[1+11*i][:-2]))
        Year.append(int(doc[2+11*i]))
        n1.append(int(doc[3+11*i]))
        n2.append(int(doc[4+11*i]))
        n3.append(int(doc[5+11*i]))
        n4.append(int(doc[6+11*i]))
        n5.append(int(doc[7+11*i]))
        s1.append(int(doc[8+11*i]))
        s2.append(int(doc[9+11*i]))
        Prize.append(int(doc[10+11*i].replace(',','')))

mydict = {'Month': Month, 'Day': Day, 'Year': Year, 'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4, 'n5': n5,
        's1': s1, 's2': s2, 'Prize': Prize}  
    
df = pd.DataFrame(mydict)

m = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
     'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

df.Month = df.Month.map(m)
df['SumN'] = df['n1'] + df['n2'] + df['n3'] + df['n4'] + df['n5']
df['SumS'] = df['s1'] + df['s2']
df['nOdds'] = df['n1']%2 + df['n2']%2 + df['n3']%2 + df['n4']%2 + df['n5']%2
df['sOdds'] = df['s1']%2 + df['s2']%2

df.to_csv(r'lottery_historical.csv', index = False)
df.to_excel(r'lottery_historical.xlsx', index = False)