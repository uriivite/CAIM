#! /bin/bash/


echo "nrounds = 6 | k = 4 | R = 2 | weights = 1: "
python Rocchio.py --index news --nrounds 6 --k 4 --R 2 --query "windows apple" 2> /dev/null
echo

echo "nrounds = 6 | k = 4 | R = 3 | weights = 1: "
python Rocchio.py --index news --nrounds 6 --k 4 --R 3 --query "windows apple" 2> /dev/null
echo

echo "nrounds = 6 | k = 4 | R = 4 | weights = 1: "
python Rocchio.py --index news --nrounds 6 --k 4 --R 4 --query "windows apple" 2> /dev/null
echo

echo "nrounds = 10 | k = 4 | R = 2 | weights = apple: 20, windows 1: "
python Rocchio.py --index news --nrounds 10 --k 4 --R 2 --query "windows apple^20" 2> /dev/null
echo

echo "nrounds = 10 | k = 4 | R = 3 | weights = apple: 20, windows 1: "
python Rocchio.py --index news --nrounds 10 --k 4 --R 3 --query "windows apple^20" 2> /dev/null
echo

echo "nrounds = 10 | k = 4 | R = 3 | weights = apple: 1, windows 10: "
python Rocchio.py --index news --nrounds 10 --k 4 --R 3 --query "apple windows^10" 2> /dev/null
echo
