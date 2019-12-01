python SearchIndexWeights.py --index news --nhits 5 --query toronto nyc 2> /dev/null
echo "-------------------------------------------------------------------------"
python SearchIndexWeights.py --index news --nhits 5 --query toronto^2 nyc 2> /dev/null
echo "-------------------------------------------------------------------------"
python SearchIndexWeights.py --index news --nhits 5 --query toronto nyc^2 2> /dev/null
