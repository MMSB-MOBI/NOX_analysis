import sys
from gmpy2 import xmpz

if len(sys.argv) != 3:
    print("usage : python process_clustering.py <clustering results.tsv> <output same organisms>")
    exit()

def parse_clusters(clustering_results):
    print("PARSE CLUSTERS...")
    dic_cluster = {}
    nb_l = 0 
    with open(clustering_results) as f:
        for l in f:
            nb_l += 1
            if nb_l % 1000000 == 0:
                print(nb_l)
            rep = l.split("\t")[0].split(" ")[0].lstrip('"')
            seq = l.split("\t")[1].split(" ")[0].lstrip('"')
            if rep not in dic_cluster:
                dic_cluster[rep]=[]
            dic_cluster[rep].append(seq)
    
    print(len(dic_cluster), "clusters")
    print("RENAME CLUSTERS...")
    dic_cluster_nb = {}
    cluster_nb = 0
    for c in dic_cluster:
        dic_cluster_nb[cluster_nb] = dic_cluster[c]
        cluster_nb += 1 

    return dic_cluster_nb


def create_organisms_bits(dic_cluster_nb):
    print("CREATE BITS...")
    dic_organism_cluster = {}
    for c in dic_cluster_nb: 
        for p in dic_cluster_nb[c]:
            org = p.split("|")[0]
            if org not in dic_organism_cluster:
                dic_organism_cluster[org] = xmpz(0)
            dic_organism_cluster[org][int(c)] = 1

    return dic_organism_cluster

def compare_organisms(dic_organism_cluster, output):
    print("COMPARE ORGANISMS")
    o = open(output, "w")
    organism_list = list(dic_organism_cluster.keys())
    nb_organism = 0
    nb_close = 0
    for i in range(len(organism_list)):
        nb_organism += 1
        if nb_organism % 100 == 0:
            print(nb_organism, "/", len(organism_list))
        for j in range(i+1, len(organism_list)):
            clust1 = dic_organism_cluster[organism_list[i]]
            clust2 = dic_organism_cluster[organism_list[j]]
            if clust1 == clust2:
                nb_close += 1
                o.write(organism_list[i] + "\t" + organism_list[j] + "\n") 
    o.close()      
    print(nb_close, "redundant pairs.")

def __main__():
    clustering_results = sys.argv[1]
    output = sys.argv[2]
    dic_cluster_nb = parse_clusters(clustering_results)
    dic_organism_cluster = create_organisms_bits(dic_cluster_nb)
    compare_organisms(dic_organism_cluster, output)

__main__()
