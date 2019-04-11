#!/bin/bash

# Preparing folders/sbatch scripts
# for pairwise N&W across a set of fasta sequence

#./scripts/runEMBOSS_slurm.sh /mobi/group/NOX_GL/toEMBOSS/ NOX_noEukaryota /mobi/group/NOX_GL/EMBOSS_work

DATA_DIR=$1
TAG=$2
OUTDIR=$3
jMax=`ls $DATA_DIR/$TAG*.fasta | wc -l`
iMax=$jMax
((iMax--))

setJob(){

echo $iMax $jMax
for i in `seq $iMax`
    do
    wDir=$OUTDIR/${TAG}_$i
    mkdir -p $wDir
    jMin=$i
    ((jMin++))
cat << EOF > $wDir/runEMBOSS.sbatch
#!/bin/bash

#SBATCH -J EMBOSS_$i
#specify nameID for job allocation
#SBATCH -o EMBOSS.out
#connect standart output of Slurm to the file name specified
#SBATCH -e EMBOSS.err
#connect standart error of Slurm to the file name specified
#SBATCH -p express # Partition to submit to
#specify the core for ressource allocation
#SBATCH --qos express # Partition to submit to

#QOS value is define for quality of this job
source /etc/profile.d/modules.sh
#settings
#modules loaded
module load emboss
cd \$WORKDIR
for j in \$(seq $jMin 1 $jMax)
do
needle -asequence $DATA_DIR/${TAG}_$i.fasta -bsequence $DATA_DIR/${TAG}_\$j.fasta -gapopen 10 -gapextend 0.5 -outfile \$j.needle
cat \$j.needle
done > ${TAG}_${i}.needle
cp ${TAG}_${i}.needle $wDir
EOF
done
}

setJob

for i in $(seq $(( $jMax -1 ))); do 
	sbatch $OUTDIR/${TAG}_$i/runEMBOSS.sbatch
done 

