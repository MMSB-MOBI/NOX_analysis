import gzip
import re
import sys
### Extract protein Hit from a profile scan against a protein DB
hmmrResultFile=sys.argv[1]
fastaVolumeFile=sys.argv[2]

rBool = False
lBool = False
matchID=[]



# Extract sequence name that were annotated by HMMR
with open(hmmrResultFile,'r') as f:
    for l in f:
        if l.startswith('    ------- ------ -----    ------- ------ -----   ---- --  --------                       -----------'):
            rBool = True
            continue
        if l.startswith('  ------ inclusion threshold ------'):
            rBool = True
            continue
        if re.search('^[\s]*$', l):
            rBool = False
            
        if rBool:
            matchID.append(l.split()[8])

matchID = list( set(matchID) ) 

#print len(matchID)
if not matchID:
    #print '#No protein detected by HMMR'
    sys.exit()
# Write the content of the multifasta volumes thaht correspond to the aforextracted names
with gzip.open(fastaVolumeFile, 'r') as f:
    file_content = f.readlines()
    for l in file_content:
        if l.startswith('>'):
            lBool = False
            a = l.split()
            #print a[0]
            if a[0][1:] in matchID:
                lBool = True
            
        if lBool: # delte last char '\n', automatically added by print call...
            print l[:-1]
            
