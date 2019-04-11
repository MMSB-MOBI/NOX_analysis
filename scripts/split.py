import gzip
import sys
import shutil
from os.path import basename
import os
#parser = argparse.ArgumentParser()
#parser.add_argument("a", help="the gziped TrEMBL archive")
#parser.add_argument("n", help="the number of volumes to produce")

#args = parser.parse_args()

print sys.argv[1]


#print args.n

def compress(filePath):
    with open(filePath, 'rb') as f_in:
        with gzip.open(filePath + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            os.remove(filePath)

LIMIT = 500000
fCnt=1
cnt =0
total = 0
#LIMIT = 10

suffix = basename(sys.argv[1]).split('.')[0] + '_v'

filePathOut = suffix + str(fCnt) + '.fasta'
fOut = open(filePathOut, 'w')

with gzip.open(sys.argv[1], 'r') as f:
    for l in f:
        if l.startswith('>'):
            cnt += 1
            total += 1
        if cnt >= LIMIT:
            fOut.close()
            compress(filePathOut)
            fCnt += 1
            cnt =0
            filePathOut = suffix +  str(fCnt) + '.fasta'
            fOut = open(filePathOut, 'w')
        fOut.write(l)

if cnt > 0:
    fOut.close()
    compress(filePathOut)



print str(total) + " entries split in " +  str(fCnt) + " volumes (" + str(LIMIT) + ") each."