#! /usr/bin/bash

rm resultsFinalsHeap

for i in {1..33}
do
    python IndexFiles.py --index novels$i --path ./novels --nfiles $i
done


for i in {1..33}
do
	echo "python CountWords.py --index novels"$i" > countedAux"$i""
	python CountWords.py --index novels"$i" > countedAux"$i"
	head countedAux"$i"
	python remove.py countedAux"$i" > cleanedAux"$i"
	head cleanedAux"$i"
	python script2.py cleanedAux$i >> resultsFinalsHeap
done

cat resultsFinalsHeap
echo "removing aux"
rm countedAux*
rm cleanedAux*
