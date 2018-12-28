import sys, os, math, base64, random
from io import BytesIO
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from fetchHist import fetchHist

def monte(symbol):
    data = fetchHist(symbol) #get last 60 days
    data = data[0:60]
    data = list(reversed(data))
    numSims = 0
    MC = {'price': -1}
    expect = []
    # one hundred simulations
    while numSims < 100:
        numSims = numSims + 1
        MC[str(numSims)] = monte_carlo(data, 60)
        del(data[-60:])
    for i in range(0,60):
        today = []
        for key in MC:
            if key != 'price':
                today.append(MC[key][i])
        expect.append(np.mean(today))
    plt.plot(np.arange(0,60,1), expect)
    plt.title(symbol.upper())
    plt.xlabel('Days')
    plt.ylabel('Price ($)')
    plt.axis([0, 60, min(expect), max(expect)])
    plt.show()

def monte_carlo(orig, days):
    count = 0
    mc = []
    while count<days:
        pdr = []
        count = count + 1
        for i in range(1,len(orig)-1):
                pdr.append(math.log(orig[i]/orig[i-1])) #periodic daily return
        adr = np.mean(pdr) #average daily return
        standDev = np.std(pdr)
        x = random.random()
        drift = 0 #small look ahead period
        Rval = norm.ppf(x, loc=adr, scale=standDev)
        price = orig[len(orig)-1]*np.exp(Rval+drift)
        orig.append(price)
        mc.append(orig[len(orig)-1])
    return mc

print("Please enter a stock symbol: ")
prompt = input()
monte(prompt)
