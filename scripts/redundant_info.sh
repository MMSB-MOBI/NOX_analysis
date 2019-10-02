if [[ $# == 0 ]]; then
    echo "usage : bash redundant_info.sh <list of accessions>"
    exit
fi

cd /mobi/group/databases/refseq95_proteins/ecoli
for acc in $@; do 
    grep_line=$(grep $acc refseq95_ecoli_assembly_summary_*)
    volume=$(echo $grep_line | cut -f 1 -d ":" | cut -f 5 -d "_")
    taxid=$(grep $acc refseq95_ecoli_assembly_summary_* | cut -f 6)
    strain=$(grep $acc refseq95_ecoli_assembly_summary_* | cut -f 9)
    nb_prot=$(zcat volume$volume/fasta/$acc\_protein.faa.gz | grep "^>" -c)
    echo $acc: $taxid, $strain, $nb_prot proteins
    zcat volume$volume/fasta/$acc\_protein.faa.gz | grep "^>" | head -n 5
    echo -e "\n"
done    
