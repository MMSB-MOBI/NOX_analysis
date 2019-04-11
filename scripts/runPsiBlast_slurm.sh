#!/bin/bash

#/mobi/group/NOX_GL $ ./scripts/runPsiBlast_slurm.sh /mobi/group/NOX_GL/toEMBOSS /mobi/group/NOX_GL/psiblastWork
DATA_DIR=$1
OUTDIR=$2
SCRIPT="/mobi/group/NOX_GL/scripts"
DB="uniprot_trembl"
MIN_COV="0.8"



#DB="nr"

for ifile in `ls $DATA_DIR/*fasta`
do
tag=$(basename $ifile .fasta)
echo $tag
wDir=$OUTDIR/$tag
mkdir -p $wDir
cat << EOF > $wDir/runPsiBlast.sbatch
#!/bin/bash

#SBATCH -J ${tag}_PB
#specify nameID for job allocation
#SBATCH -o ${tag}_PB.out
#connect standart output of Slurm to the file name specified
#SBATCH -e ${tag}_PB.err
#connect standart error of Slurm to the file name specified
#SBATCH -p medium-mobi # Partition to submit to
#specify the core for ressource allocation
#SBATCH --qos medium-mobi # Partition to submit to

#QOS value is define for quality of this job
source /etc/profile.d/modules.sh
#settings
#modules loaded
module load ncbi-blast/2.2.26
cd \$WORKDIR

blastpgp -m 7 -e 0.001 -i $ifile -d $DB -j 1 -b 2500 > $tag.xml
python $SCRIPT/blastFastaExtracter.py  $tag.xml $MIN_COV > $tag.lst
fastacmd  -d $DB  -i $tag.lst > $tag.fasta

# if j > 3, query may disappear
#inputRec="$(awk 'NR == 1 {print}' $ifile)"
# if the original record is not in the ouput
#if grep "\$inputRec" $tag.fasta > /dev/null; 
#    then
#    echo "original record in the output"
#else
#    echo "original record NOT in the output"
#    cp $ifile tmp.fasta
#    cat $tag.fasta >> tmp.fasta
#    mv tmp.fasta $tag.fasta
#fi
cp $tag.* $wDir

EOF
cd $wDir
sbatch $wDir/runPsiBlast.sbatch
done
