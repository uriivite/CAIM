import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def f(N, k, beta):
    return k * (N**beta)


if len(sys.argv) < 2:
    print("Usage: script.py [fitxer]")

xdata = []
ydata = []
for line in list(open(sys.argv[1])):
    first = True
    for word in line.split():
        if (first):
            ydata.append(int(word))
            first = False
        else:
            xdata.append(int(word))

plt.plot(xdata, ydata, 'r-', label='data')

popt, pcov = curve_fit(f, xdata, ydata)
plt.plot(xdata, f(xdata, *popt), 'b--', label='fit')

plt.xlabel("totalWords")
plt.ylabel("distinctWords")
plt.legend()
plt.show()

print(popt)
