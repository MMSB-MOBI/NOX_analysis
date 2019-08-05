#!/bin/bash

DATA_DIR=$1 
OUT_DIR=$2

setJob() {
local rootDir=$1 
local inputFilePath=$2
id=`basename $inputFilePath  | awk -F. '{print $1}' `
originDir=$rootDir/$id
mkdir -p $originDir

cat << EOF > $originDir/getCDS.sbatch
#!/bin/bash

#SBATCH -J $id\_CDS
#specify nameID for job allocation
#SBATCH -o getCDSjob.out
#connect standart output of Slurm to the file name specified
#SBATCH -e getCDSjob.err
#connect standart error of Slurm to the file name specified
#SBATCH -p medium # Partition to submit to
#specify the core for ressource allocation
#SBATCH --qos medium # Partition to submit to

#QOS value is define for quality of this job
source /etc/profile.d/modules.sh
#settings

cd \$WORKDIR

python /mobi/group.NOX_CH/nox_analysis/scripts/get_ENA_cds.py $inputFilePath

rm trembl.fasta
/bin/python /mobi/group/NOX_CH/nox-analysis/scripts/extractHMMR_fasta.py hmmsearch.out $inputFilePath > hmmsearch.fasta
tmhmm hmmsearch.fasta > tmhmm.out
cp hmmsearch.out $originDir
cp hmmsearch.fasta $originDir
cp HMMRjob.* $originDir
cp tmhmm.out $originDir

EOF

echo $originDir/runHMM.sbatch
}

for ifile in `find $DATA_DIR -name "volume*.txt"`; do
    echo $ifile
    sbatchFile=`setJob $OUT_DIR $ifile`
    #echo "Launching sbatch $sbatchFile"
    #sbatch $sbatchFile
    #(i++))
    #[ $i -eq 10 ] && break
done