#! /bin/bash

echo "Standard | Lowercase | Snowball:"
python CountWords.py --index newsstdlwsn 2> /dev/null | tail -1
echo "Standard | Lowercase | Porter_Stem:"
python CountWords.py --index newsstdlwps 2> /dev/null | tail -1
echo "Standard | Lowercase | Kstem:"
python CountWords.py --index newsstdlwks 2> /dev/null | tail -1
echo "Standard | Lowercase + Ascii | Snowball:"
python CountWords.py --index newsstdlwascsn 2> /dev/null | tail -1
echo "Standard | Lowercase + Ascii + Stop | Snowball:"
python CountWords.py --index newsstd 2> /dev/null | tail -1
echo "Letter | Lowercase + Ascii + Stop | Snowball:"
python CountWords.py --index newslett 2> /dev/null | tail -1
echo "Whitespace | Lowercase + Ascii + Stop | Snowball:"
python CountWords.py --index newsws 2> /dev/null | tail -1
echo "Classic | Lowercase + Ascii + Stop | Snowball:"
python CountWords.py --index newscl 2> /dev/null | tail -1

