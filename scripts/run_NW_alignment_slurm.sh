#!/bin/bash

DATA_DIR=$1 # Location of all pickled peptides objects
OUT_DIR=$2  # Folder where slurm workdir will be created
SCRIPT_DIR=$3


setJob() {
local rootDir=$1 
local inputFilePath=$2

id=`basename $inputFilePath  | awk -F. '{print $1}' `
originDir=$rootDir/$id
mkdir -p $originDir


cat << EOF > $originDir/runNW.sbatch
#!/bin/bash

#SBATCH -J $id
#specify nameID for job allocation
#SBATCH -o NWjob.out
#connect standart output of Slurm to the file name specified
#SBATCH -e NWjob.err
#connect standart error of Slurm to the file name specified
#SBATCH -p express # Partition to submit to
#specify the core for ressource allocation
#SBATCH --qos express # Partition to submit to

#QOS value is define for quality of this job
source /etc/profile.d/modules.sh
#settings
#modules loaded
module load pyproteins

cd \$WORKDIR

python3 /mobi/group/NOX_CH/nox-analysis/scripts/pairwise_NW_alignment $inputFilePath nw_align.pickle
cp nw_align.pickle $originDir
cp NWjob.* $originDir

EOF

echo $originDir/runNW.sbatch
}

i=0
for ifile in `find $DATA_DIR -name "NAD_binding_package*.pickle"`
    do
    echo $ifile
    sbatchFile=`setJob $OUT_DIR $ifile`
    #echo "Launching sbatch $sbatchFile"
    #sbatch $sbatchFile
    ((i++))
    #[ $i -eq 10 ] && break
done
