#! /bin/bash/

# Aquest script proba diferents combinacions de nrounds, k i R per l'script de Rocchio,
# preten veure quina combinacio dona millor resultats per la cerca de la paraula "species" a l'index "novels".

echo "nrounds = 6 | k = 4 | R = 1 | species weight = 1: "
python Rocchio.py --index novels --nrounds 6 --k 4 --R 1 --query species 2> /dev/null
echo
echo "nrounds = 4 | k = 4 | R = 1 | species weight = 1: "
python Rocchio.py --index novels --nrounds 4 --k 4 --R 1 --query species 2> /dev/null
echo
echo "nrounds = 3 | k = 4 | R = 1 | species weight = 1: "
python Rocchio.py --index novels --nrounds 3 --k 4 --R 1 --query species 2> /dev/null
echo
echo "nrounds = 6 | k = 4 | R = 2 | species weight = 1: "
python Rocchio.py --index novels --nrounds 6 --k 4 --R 2 --query species 2> /dev/null
echo
echo "nrounds = 5 | k = 3 | R = 2 | species weight = 1: "
python Rocchio.py --index novels --nrounds 5 --k 3 --R 2 --query species 2> /dev/null
echo
echo "nrounds = 4 | k = 3 | R = 2 | species weight = 1: "
python Rocchio.py --index novels --nrounds 4 --k 3 --R 2 --query species 2> /dev/null
echo
echo "nrounds = 3 | k = 3 | R = 2 | species weight = 1: "
python Rocchio.py --index novels --nrounds 3 --k 3 --R 2 --query species 2> /dev/null
echo
echo "nrounds = 4 | k = 3 | R = 2 | species weight = 6: "
python Rocchio.py --index novels --nrounds 4 --k 3 --R 2 --query "species^6" 2> /dev/null
echo "nrounds = 2 | k = 2 | R = 2 | species weight = 6: "
python Rocchio.py --index novels --nrounds 2 --k 2 --R 2 --query "species^6" 2> /dev/null
echo "nrounds = 4 | k = 4 | R = 4 | species weight = 6: "
python Rocchio.py --index novels --nrounds 4 --k 4 --R 2 --query "species^6" 2> /dev/null






