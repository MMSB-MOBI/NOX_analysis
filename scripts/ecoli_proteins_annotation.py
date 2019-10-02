import sys 
sys.path.append("/Users/chilpert/Dev/pyproteinsExt/src")
sys.path.append("/Users/chilpert/Dev/pyproteins/src")
import pyproteinsExt.fastaNOX as fasta
import glob
import time
import pickle

def save(data, tag=None):
    saveDir="/Volumes/arwen/mobi/group/NOX_ecoli_full/pickle_saved"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fTag = "NOX_ecoli_" + tag + "_" if tag else "NOX_ecoli_"
    fSerialDump = fTag + timestr + ".pickle"
    with open(saveDir + '/' + fSerialDump, 'wb') as f:
        pickle.dump(data, f)
    print('data structure saved to', saveDir + '/' + fSerialDump)

def parsing_results(dataDir):
    dataDir_length=len(dataDir)
    c=1
    print(c,"/",dataDir_length)
    dataContainer=fasta.parse(dataDir[0])
    for d in dataDir[1:]:
        c+=1
        print(c,"/",dataDir_length)
        dataContainer=dataContainer.addParsing(fasta.parse(d))
    return dataContainer

def parse_clusters(clusters_file):
    f = open(clusters_file, "r")
    dic_cluster = {}
    i = 0
    for l in f:
        i += 1
        if i % 10000 == 0:
            print(i)
        cluster = l.split("\t")[0]
        prots = set(l.rstrip().split("\t")[1].split(";"))
        dic_cluster[cluster] = prots
    f.close()
    print(len(dic_cluster),"clusters")
    return dic_cluster

def annotation(dic_cluster, fastaContainer):
    o = open("/Users/chilpert/Results/NOX_ecoli/clusters_annotation.tsv", "w")    
    o.write("Cluster\tAnnotations\n")
    for c in dic_cluster:
        if int(c) % 10000 == 0:
            print(c, "/", len(dic_cluster))
        annotations = set()
        prot_ids = set([p.split("|")[1] for p in dic_cluster[c]])
        for p in prot_ids:
            annot = fastaContainer.entries[p].annotation.replace("MULTISPECIES: ", "").split("[")[0].rstrip()
            annotations.add(annot)
        o.write(str(c)+"\t" + "\t".join(annotations) + "\n")
    o.close()

dataDir = glob.glob('/Volumes/arwen/mobi/group/NOX_ecoli_full/volumes_concat10/*.fasta.gz')
print(len(dataDir))
#dataContainer = parsing_results(dataDir)
print("Serialize...")
#save(dataContainer,"protein_product")

print("LOAD")
dataContainer = pickle.load(open("/Users/chilpert/Results/NOX_ecoli/NOX_ecoli_protein_product_20190925-124216.pickle", "rb"))
print("CLUSTER")
dicCluster = parse_clusters("/Users/chilpert/Results/NOX_ecoli/all_ecoli_cluster_parse.tsv")
print("ANNOT")
annotation(dicCluster, dataContainer)
