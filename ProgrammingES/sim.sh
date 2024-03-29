#! /bin/bash

echo "comparing two identical documents..."

echo "Document: /tmp/novels/DarwinOriginofSpecies.txt"
python TFIDFViewer.py --index novels --files /tmp/novels/DarwinOriginofSpecies.txt /tmp/novels/DarwinOriginofSpecies.txt 2> /dev/null


echo "comparing documents which belong to same specific subset of the corpus..."

echo "Documents (selected randomly): (1) /tmp/20_newsgroups/alt.atheism/0000000 and (2) /tmp/20_newsgoups/alt.atheism/0000446"


echo "[Documents tokenized and filtered using: Standard | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newsstd --files /tmp/20_newsgroups/alt.atheism/0000000 /tmp/20_newsgroups/alt.atheism/0000446 2> /dev/null


echo "[Documents tokenized and filtered using: Classic | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newscl --files /tmp/20_newsgroups/alt.atheism/0000000 /tmp/20_newsgroups/alt.atheism/0000446 2> /dev/null

echo "[Documents tokenized and filtered using: Whitespace | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newsws --files /tmp/20_newsgroups/alt.atheism/0000000 /tmp/20_newsgroups/alt.atheism/0000446 2> /dev/null

echo "[Documents tokenized and filtered using: Letter | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newslett --files /tmp/20_newsgroups/alt.atheism/0000000 /tmp/20_newsgroups/alt.atheism/0000446 2> /dev/null


echo "comparing documents which belong to different subset of news corpus..."

echo "Documents (selected randomly): (1) /tmp/20_newsgroups/alt.atheism/0000338 and /tmp/20_newsgroups/sci.space/0014451"

echo "[Documents tokenized and filtered using: Standard | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newsstd --files /tmp/20_newsgroups/alt.atheism/0000338 /tmp/20_newsgroups/sci.space/0014451 2> /dev/null

echo "[Documents tokenized and filtered using: Classic | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newscl --files /tmp/20_newsgroups/alt.atheism/0000338 /tmp/20_newsgroups/sci.space/0014451 2> /dev/null

echo "[Documents tokenized and filtered using: Whitespace | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newsws --files /tmp/20_newsgroups/alt.atheism/0000338 /tmp/20_newsgroups/sci.space/0014451 2> /dev/null

echo "[Documents tokenized and filtered using: Letter | Lowercase + Ascii + Stop | Snowball]"
python TFIDFViewer.py --index newslett --files /tmp/20_newsgroups/alt.atheism/0000338 /tmp/20_newsgroups/sci.space/0014451 2> /dev/null


