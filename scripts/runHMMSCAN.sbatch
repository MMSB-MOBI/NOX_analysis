#!/bin/bash

#SBATCH -J hmmscan
#specify nameID for job allocation
#SBATCH -o hmmscanJob.out
#connect standart output of Slurm to the file name specified
#SBATCH -e hmmscanJob.err
#connect standart error of Slurm to the file name specified
#SBATCH -p medium # Partition to submit to
#specify the core for ressource allocation
#SBATCH --qos medium # Partition to submit to

#QOS value is define for quality of this job
source /etc/profile.d/modules.sh
#settings
#modules loaded
module load hmmr
#echo $WORKDIR
cd $WORKDIR

PROFILE_FILE=$1
INPUT_FILE=$2
OUTPUT_FILE=$3

hmmscan $PROFILE_FILE $INPUT_FILE > hmmscan.out 

cp hmmscan.out $OUTPUT_FILE
