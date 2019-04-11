#!/bin/bash

DATA_DIR=$1 # Location of all fasta input gziped files 
OUT_DIR=$2  # Folder where slurm workdir will be created
HMM_DIR=$3  # Folders where hmm profile files are located



setJob() {
local rootDir=$1 
local inputFilePath=$2
local hmmProfileLocation=$3

id=`basename $inputFilePath  | awk -F. '{print $1}' `
originDir=$rootDir/$id
mkdir -p $originDir


cat << EOF > $originDir/runHMM.sbatch
#!/bin/bash

#SBATCH -J $id
#specify nameID for job allocation
#SBATCH -o HMMRjob.out
#connect standart output of Slurm to the file name specified
#SBATCH -e HMMRjob.err
#connect standart error of Slurm to the file name specified
#SBATCH -p medium # Partition to submit to
#specify the core for ressource allocation
#SBATCH --qos medium # Partition to submit to

#QOS value is define for quality of this job
source /etc/profile.d/modules.sh
#settings
#modules loaded
module load hmmr
module load netpbm
module load gnuplot
module load TMHMM

cd \$WORKDIR
gunzip -c $inputFilePath > ./trembl.fasta

hmmsearch $hmmProfileLocation/fad_binding.hmm trembl.fasta > hmmsearch.out
hmmsearch $hmmProfileLocation/ferric_reduct.hmm trembl.fasta >> hmmsearch.out
hmmsearch $hmmProfileLocation/nad_binding.hmm trembl.fasta >> hmmsearch.out

rm trembl.fasta
python /mobi/group/NOX_GL/scripts/extractHMMR_fasta.py hmmsearch.out $inputFilePath > hmmsearch.fasta
tmhmm hmmsearch.fasta > tmhmm.out
cp hmmsearch.out $originDir
cp hmmsearch.fasta $originDir
cp HMMRjob.* $originDir
cp tmhmm.out $originDir

EOF

echo $originDir/runHMM.sbatch
}

echo $DATA_DIR

i=0
for ifile in `find $DATA_DIR -name "uniprot_trembl_v*.fasta.gz"`
    do
    echo $ifile
    sbatchFile=`setJob $OUT_DIR $ifile $HMM_DIR`
    echo "Launching sbatch $sbatchFile"
    sbatch $sbatchFile
    ((i++))
    #[ $i -eq 10 ] && break
done