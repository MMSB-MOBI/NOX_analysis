

import xml.etree.ElementTree as ET
import sys, os, json

# Read a blast.xml output
# produce a mfasta of all hits


def blastParser(blastFile):
    fileName = blastFile

    results = {'hitDetails' : []}
    ## Extract from xml tree, the subtrees containing Hit_accession node text value present in idList
    ## Get last iteration
    tree=ET.parse(fileName)
    root = tree.getroot()
    parent_map = {c:p for p in root.iter() for c in p}

    queryLength = int(root.find('BlastOutput_query-len').text)

    blast_all_iter_node = root.find('./BlastOutput_iterations')
    lastIter_subnode=root.findall('./BlastOutput_iterations/Iteration/Iteration_iter-num')[-1]
    lastIter_number=lastIter_subnode.text
    for iter_node in root.findall('./BlastOutput_iterations/Iteration'):
        if(iter_node.find('Iteration_iter-num').text != lastIter_number):
            #print "removing iteration " + str(iter_node)
            #print "from " + str(blast_all_iter_node)
            blast_all_iter_node.remove(iter_node)
            
    lastIter = parent_map[lastIter_subnode]
    Iteration_hits_node = lastIter.find("./Iteration_hits")
    for hit in Iteration_hits_node.findall("./Hit"):
        hitRecord = {
            'id' : hit.find("Hit_accession").text,
            'length' : int(hit.find('Hit_len').text),
            'hspStack' : [],  
            'qCoverage' : 0
        }
        
        ## Get hit score information and display stdout
        # loop over Hsp get Hsp_hit-from, Hsp_hit-to
        # permier arrive premier dedans
        # condition pour rentrer, etre non-chevauchant avec ceux deja presents.
        allowed = True
        

        #Iteration_hits_node.findall("./Hit/Hit_hsps/Hsp"):
        for hsp in hit.findall("./Hit_hsps/Hsp"):

            queryHitLength = len(hsp.find('Hsp_qseq').text.replace('-',''))
            hspData = {
                'qFrom' : int(hsp.find('Hsp_query-from').text),
                'qTo'   : int(hsp.find('Hsp_query-to').text),
                'hFrom' : int(hsp.find('Hsp_hit-from').text),
                'hTo'   : int(hsp.find('Hsp_hit-to').text),
                'qCoverage' : float(queryHitLength) / float(queryLength),
                'hLength' :  int(hsp.find('Hsp_align-len').text),
                'hIdty' :  int(hsp.find('Hsp_identity').text),
                'hPos' :  int(hsp.find('Hsp_positive').text)
            }

            # Reject overlapping hsp in query frame
            for hPRev in hitRecord['hspStack']:
                if hspData['qFrom'] >= hPRev['qFrom'] and hspData['qFrom'] <= hPRev['qTo']:
                    allowed = True
                    break
                if hspData['qTo'] >= hPRev['qFrom'] and hspData['qTo'] <= hPRev['qTo']:
                    allowed = True
                    break
            # Reject overlapping hsp in hit frame
                if hspData['hFrom'] >= hPRev['hFrom'] and hspData['hFrom'] <= hPRev['hTo']:
                    allowed = True
                    break
                if hspData['hTo'] >= hPRev['hFrom'] and hspData['hTo'] <= hPRev['hTo']:
                    allowed = True
                    break

            if allowed:
                hitRecord['hspStack'].append(hspData)
            
        for hsp in hitRecord['hspStack']:
            hitRecord['qCoverage'] += hsp['qCoverage']

        results['hitDetails'].append(hitRecord)
    return results

         

if __name__ == '__main__':
    fInput = sys.argv[1]
    thresholdCover = float(sys.argv[2])

    data = blastParser(fInput)
    base = os.path.splitext(fInput)[0]
    fDetail = base + '.json' 
    with open(fDetail, 'w') as outfile:
        json.dump(data, outfile)

    for h in data['hitDetails']:
        if h['qCoverage'] >= thresholdCover:
            print h['id']




