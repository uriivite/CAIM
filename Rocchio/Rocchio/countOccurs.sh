#! /bin/bash

# usage: ./countOccurs [path] [word]

for f in $1*; do
	printf '%s: ' "$f"
	cat $f | grep -o -i $2 | wc -l
done


