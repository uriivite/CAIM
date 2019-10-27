# !/usr/bin/python3
import sys
import re

with open(sys.argv[1]) as f:
    lineList = f.readlines()
    for elem in lineList:
        gf = re.match("[0-9]+(,)( )[a-z|A-Z]+(\\n)", elem)
        if gf:
            print (elem, end="")

