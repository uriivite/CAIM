import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def f(rank, a, b, c):
    return c / ((rank + b)**a)

if len(sys.argv) < 2:
    print("Usage: script.py [fitxer]")

lastFreq = 0
lis = []
for line in reversed(list(open(sys.argv[1]))):
    for word in line.split():
        if word[-1] == ',':
            if word[:-1] != lastFreq:
                lastFreq = int(word[:-1])
                lis.append(lastFreq)
                
plt.loglog(lis, 'b-', label='data')

xdata = np.linspace(50, len(lis) - 5, len(lis) - 55)
ydata = np.array(lis[50:-5])


popt, pcov = curve_fit(f, xdata, ydata)
plt.loglog(xdata, f(xdata, *popt), 'r--', label='fit')

plt.xlabel("rank")
plt.ylabel("freq")
plt.legend()
plt.show()

print(popt)
