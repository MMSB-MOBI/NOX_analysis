# Use this to browse all the psiblast workfolder and eliminate strictly identical proteins
import sys

import os, re

def listFastaInput(rootFolder):
    fastaFiles = []
    for idir in os.listdir(rootFolder):
        for item in os.listdir(rootFolder + '/' + idir):
            if item.endswith('.fasta'):
                fastaFiles.append(rootFolder + '/' + idir + '/' + item)
    return fastaFiles


rootFolder=sys.argv[1]
outputFile=sys.argv[2]
fastaFiles = listFastaInput(rootFolder)

print len(fastaFiles)

reHeader = re.compile('^(>.*)$')
f = open (outputFile, "w")

knownHeaders = []

for fastaFile in fastaFiles:
    print 'Opening ' + fastaFile
    cnt = 0
    with open(fastaFile, 'r') as f2:
        wBool = True
        for l in f2:
            m = reHeader.match(l)
            if m:
                if m.groups()[0] in knownHeaders:
                     wBool = False
                else:
                    knownHeaders.append(m.groups()[0])
                    cnt += 1
            if wBool:
                f.write(l)
    print str(cnt) + ' sequences wrote from ' + fastaFile
    

f.close()
                


