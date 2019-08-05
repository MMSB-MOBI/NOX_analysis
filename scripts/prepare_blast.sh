DOWNLOAD_DIR=$1
RESULT_DIR=$2
PROTEINS_DIR=$3
wget -O $DOWNLOAD_DIR/taxid_28230cds_from_genomic.fna.gz ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/900/143/105/GCF_900143105.1_IMG-taxon_2698536812_annotated_assembly/GCF_900143105.1_IMG-taxon_2698536812_annotated_assembly_cds_from_genomic.fna.gz
gunzip $DOWNLOAD_DIR/taxid_28230cds_from_genomic.fna.gzmkdir -p $RESULT_DIR/taxid_28230
fasta_protein=$(grep -l "tr|A0A1N6G2S4|A0A1N6G2S4_9LACT" $PROTEINS_DIR/*)
echo $fasta_protein
