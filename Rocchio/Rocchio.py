import argparse
# per a poder executar l'script que tira les queries a l'ES
from os import system

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", type=list, required=True, help="Put a set of words to use as query.")
ap.add_argument("--nrounds", default=5, type=int, required=False, help="the number of applications of Rocchio rule.")
ap.add_argument("--ktop", default=5, type=int, required=False, help="The number of top documents considered relevant and used for applying Rocchio at each round.")
ap.add_argument("--rkept", default=5, type=int, required=False, help="The maximum number of new terms to be kept in the new query.")
ap.add_argument("--alpha", default=5, type=int, required=False, help="Alpha weight in the Rocchio rule.")
ap.add_argument("--beta", default=5, type=int, required=False, help="Beta weight in the Rocchio rule.")
args = vars(ap.parse_args())
# son els arguments de l'altre script -> cal adaptar aquestes linies peque sigui efectiu en aquest
parser.add_argument('--index', default=None, help='Index to search')
parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')



print(args)

nrounds = args["nrounds"]
k = args["ktop"]
R = args["rkept"]
alpha = args["alpha"]
beta = args["beta"]

#system("python SearchIndexWeights.py")
