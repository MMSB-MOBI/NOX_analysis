import sys, os
import pickle
import pyproteins.sequence.peptide as pep
import pyproteins.alignment.nw_custom as N
import pyproteins.alignment.scoringFunctions as scoringFunctions

try: 
    inp=sys.argv[1] #it's a pickled list of peptide pairs
except IndexError:
    raise Exception("Give input")

try:
    output=sys.argv[2]
except IndexError: 
    raise Exception("Give output")  

list_pairs=pickle.load(open(inp,'rb'))

blosum = scoringFunctions.Needle().fScore
nw = N.nw(gapOpen=-10, gapExtend=-0.5, matchScorer=blosum)

results=[]
for pair in list_pairs: 
    aliResObj=nw.align(pair[0],pair[1])
    results.append(aliResObj)

pickle.dump(results,open(output,"wb"))