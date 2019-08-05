#!/bin/bash

PROTEINS_DIR=$1
DOWNLOAD_DIR=$2
RESULTS_DIR=$3 

if [ "$#" -ne 3 ]; then 
	echo "usage : searchNeighborhood.sh proteins_directory download_directory results_directory"
	exit 1
fi 	

for prot in $(ls $PROTEINS_DIR);do 
	grep "^>" $PROTEINS_DIR/$prot
done 