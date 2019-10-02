#!/bin/bash
#SBATCH -J matrix_ecoli
#SBATCH -p medium
#SBATCH --qos medium

if [[ $# -lt 2 ]]; then 
    echo "usage : sbatch run_presence_absence_ecoli.sbatch <clusters input.tsv> <matrix output.tsv> <optional:discarded organisms.txt>"
    exit
fi

INPUT=$1
OUTPUT=$2
if [[ $3 ]]; then
    DISCARD=$3
fi


if [[ $DISCARD ]]; then
    echo run command python /home/chilpert/Dev/NOX/presence_absence_ecoli.py -d $DISCARD $INPUT $OUTPUT
    python /home/chilpert/Dev/NOX/presence_absence_ecoli.py -d $DISCARD $INPUT $OUTPUT
else
    echo run command python /home/chilpert/Dev/NOX/presence_absence_ecoli.py $INPUT $OUTPUT
    python /home/chilpert/Dev/NOX/presence_absence_ecoli.py $INPUT $OUTPUT
fi