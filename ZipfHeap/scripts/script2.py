import sys
import numpy as np

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
total = 0
for i in lis:
    total += i

print(len(lis), total)
