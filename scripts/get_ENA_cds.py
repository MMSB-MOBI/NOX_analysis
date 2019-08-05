import sys
import pickle
import json
sys.path.append("/home/chilpert/Dev/pyproteinsExt/src")
sys.path.append("/home/chilpert/Dev/pyproteins/src")
import pyproteinsExt.ena as ena


if len(sys.argv) != 3:
    raise Exception("Give input list and output directory")

# Initialize ENA Collection
enaColl = ena.getENACollection()
enaColl.setCache("/home/chilpert/cache/ena")

inp = sys.argv[1]
outdir = sys.argv[2]
dic_results = {}
json_dic = {}
outfile = outdir+"/"+inp.split(".")[:-1][0]+"_CDS.pickle"
outfile_json = outdir+"/"+inp.split(".")[:-1][0]+"_CDS.json"
print(outfile)

with open(inp, "r") as f:
    for l in f:
        l_split = l.rstrip().split("\t")
        protein = l_split[0]
        ena_id = l_split[1]
        # For now, take first ena id
        ena_id = ena_id.split(",")[0]
        ena_entry = enaColl.get(ena_id)
        dic_results[protein] = ena_entry.CDS
        json_dic[protein] = []
        for cds in ena_entry.CDS:
            CDS_json = {'protein_id': cds.qualifiers["protein_id"],
                        'product': cds.qualifiers["product"],
                        "sequence": cds.qualifiers["translation"],
                        'location': cds.location["start"] + ";" + cds.location["end"] + ";" + cds.location["strand"]}
            json_dic[protein].append(CDS_json)

json.dump(json_dic, open(outfile_json, "w"))
#sys.setrecursionlimit(50000)
pickle.dump(dic_results, open(outfile, "wb"))
#sys.setrecursionlimit(3000)
