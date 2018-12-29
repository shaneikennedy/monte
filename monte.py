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
    data = list(reversed(data[0:60]))
    num_sims = 0
    mc = {'price': -1}
    expected = []
    # one hundred simulations
    while num_sims < 100:
        num_sims += 1
        mc[num_sims] = monte_carlo(data, 60)
        del(data[-60:])
    for i in range(0,60):
        today = []
        for key in mc:
            if key != 'price':
                today.append(mc[key][i])
        expected.append(np.mean(today))
    plt.plot(np.arange(0,60,1), expected)
    plt.title(symbol.upper())
    plt.xlabel('Days')
    plt.ylabel('Price ($)')
    plt.axis([0, 60, min(expected), max(expected)])
    plt.show()

def monte_carlo(orig, days):
    count = 0
    mc = []
    while count < days:
        pdr = []
        count = count + 1
        for i in range(1,len(orig)-1):
                pdr.append(math.log(orig[i]/orig[i-1])) #periodic daily return
        adr = np.mean(pdr) #average daily return
        stand_dev = np.std(pdr)
        x = random.random()
        drift = 0 #small look ahead period
        r_val = norm.ppf(x, loc=adr, scale=stand_dev)
        price = orig[len(orig)-1]*np.exp(r_val+drift)
        orig.append(price)
        mc.append(orig[len(orig)-1])
    return mc

print("Please enter a stock symbol: ")
prompt = input()
monte(prompt)
