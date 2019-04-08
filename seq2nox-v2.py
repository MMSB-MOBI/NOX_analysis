#! /xray/mickael/Softs/Python-3.3.3/bin/python3

def extractFasta(fichierFasta, fichierOut):
    """extraction des infos ID, AC, OS, SQ à partir d'un fichier contenant des sequences fasta dans un fichier input.
       Le programme ecrit dans un fichier output. Chaque indice de la permière liste contient une liste avec les champ ID ; AC ; OS ; SQ d'une proteine"""

    import re

    fichierFasta=open(fichierFasta,'r')                                                # ouverture du fichier fasta en lecture
    fichierOut=open(fichierOut,'w')                                                    # ouverture du fichier output en écriture
  
    n = 0                                                                              # initialise n

    for ligne in fichierFasta:                                                         # lecture de chaque ligne du fichier
        if re.search('^>', ligne):                                                     # si la ligne commence par '>'  signifie que on commence une nouvelle prot => n = 0
            if n == 1 :                                                                # si on a nouvelle prot et qu'une sequence est enregistré, la met dans le ficher output
                    fichierOut.write(sequence+'\n')
            n = 0                                                                      
            champ = re.search('^>[^\|]+\|([^\|]+)\|([^\|]+).*OS=([^=]+) ', ligne)                      # recherche et selectionne les champ AC ID et OS 


            fichierOut.write(champ.group(1)+'\t|\t'+champ.group(2)+'\t|\t'+champ.group(3)+'\t|\t')                 # ecrit les nouvelles valeurs dans le fichier output


        else :                                                                         # lecture de la sequence
            if n == 0 :                                                                # si nouvelle prot (n = 0) réinitialise la variable sequence et n = 1
                sequence = ''                                                          
                n = 1
            ligne = ligne.replace('\n', '')                                            # suprime les retour à la ligne 
            sequence = sequence + ligne                                                # ajoute les morceaux de sequence les une aux autres

    fichierOut.write(sequence+'\n')                                                    # ecrit la dernière sequence
    fichierFasta.close()                                                               # fermeture du fichier fasta
    fichierOut.close()                                                                 # fermeture du fichier output


def rechercheMotif(fichierFasta, fichierOut, motif):
    """recherche le motif dans une sequence protéique. L'input est un fichier avec une liste de protéine. Chaque protéine est une ligne contennat les champs ID, AC, OS, SQ. 
       Le programme ecrit dans un fichier une sous selection de proteines ayant le motif et donne la position du debut et de la fin du motif.
       le motif doit respecter les conventions du module re"""
    
    import re

    fichierFasta=open(fichierFasta,'r')                                                # ouverture du fichier fasta en lecture
    fichierOut=open(fichierOut,'w')                                                    # ouverture du fichier output en écriture
    
    for prot in fichierFasta :                                                         # pour chaque liste de la liste
         seq = re.search('.+\t\|\t.+\t\|\t.+\t\|\t([A-Z]+)', prot)                     # recupére la sequence dans prot
         sequence = str(seq.group(1))
         if re.search(motif, sequence) :                                               # si la séquence contient le motif
            prot = prot.replace('\n', '')                                              # suprimme les retour à la ligne     
            fichierOut.write(prot+'\t|\t')
            for match in re.finditer(motif, sequence) :                                # recherche toutes les aucurences du motif recherché
                fichierOut.write(str(match.start()+1)+'-'+str(match.end())+' ')        # ajoute la protéine à la liste des retenues
            fichierOut.write('\n')                                                     # ajoute la protéine à la liste des retenues

    fichierFasta.close()                                                               # fermeture du fichier fasta
    fichierOut.close()                                                                 # fermeture du fichier output


def rechercheHelixAndHH(fichierFasta, fichierOut, minHelix, maxHelix, resiAdd, distanceMinCoupleHH):
    """fait tourné le programme tmhmm sur toute les séquences de l'input et ne selectionne que celles ayant entre minHelix et maxHelix helices. Puis il teste si la sequence à deux fois un couple d'Histidines séparé par 12 ou 14 résidus dans la zone des helices transmb, + ou - resiAdd résidus. Le programme test aussi si il y a au moins 2 couple HHvalid séparé d'au moins distanceMinCoupleHH résidus.
       L'input est un fichier avec une liste de protéine. Chaque protéine est une ligne contennat les champs ID, AC, OS, SQ. 
       Le programme ecrit dans un fichier une sous selection de proteines respectant la règle et écrit la position du premier résidu de la première helice trouvée et du dernier résidu de la dernière helice trouvée."""

    import re, subprocess, os

    fichierFasta=open(fichierFasta,'r')                                                # ouverture du fichier fasta en lecture
    fichierOut=open(fichierOut,'w')                                                    # ouverture du fichier output en écriture


    for prot in fichierFasta :                                                         # pour chaque proteine du fichier input
        fichierTmp=open('/tmp/seq_fasta.tmp', 'w')                                     # création et ouverture d'un fichier tmp ou est placé la dernière sequence
        seq = re.search('.+\t\|\t.+\t\|\t.+\t\|\t([A-Z]+)', prot)                      # recupére la sequence de la prot
        fichierTmp.write('>\n'+seq.group(1))                                           # écriture de la sequence au format fasta dans le fichier tmp
        fichierTmp.close()                                                             # fermeture du fichier tmp ou est placé la dernière sequence                      

        result = subprocess.check_output(['tmhmm', '/tmp/seq_fasta.tmp'])   # fait tourner TMHMM sur la sequence 
        result = result.splitlines()                                                   # chaque ligne devient un élément de la liste
        os.system('rm -rf TMHMM_*')                                                    # supprime le dossier TMHMM créé par le programme tmhmm
#        os.system('rm -f /tmp/seq_fasta.tmp')

        nbHelice = re.search('Number of predicted TMHs:[ ]+([0-9]+)', str(result[1]))  # recupere le numbre d'helices trouvées
        if int(nbHelice.group(1)) >= minHelix and int(nbHelice.group(1)) <= maxHelix : # si le nombre d'helices trouvées est compris entre minHelix et maxHelix
            i = 0                                                                      # intitialise un compteur permettant de savoir si on a deja passé la première helice
            for ligne in result :                                                      # pour chaque ligne du fichier output de TMHMM
                if re.search('TMhelix[^0-9]+[0-9]+', str(ligne)) :
                    if i == 0 :                                                        # si c'est la première helice
                        i = 1
                        heliceDebut = re.search('TMhelix[^0-9]+([0-9]+)', str(ligne))
                        heliceDebut = str(int(heliceDebut.group(1))+1)
                        if (int(heliceDebut) - int(resiAdd)) <1 :                      # si le premier résidu de la premiére helice - resiAdd < 1 => commence la recherche à 1 si non la commence à heliceDebut-resiAdd
                            heliceDebutSearch = 1
                        else :
                            heliceDebutSearch = int(heliceDebut) - int(resiAdd)
                    else :
                        heliceFin = re.search('TMhelix[^0-9]+[0-9]+[^0-9]+([0-9]+)', str(ligne))
                        heliceFin = str(int(heliceFin.group(1))+1)

                        if (int(heliceFin) + int(resiAdd)) > len(seq.group(1)) :        # si le dernier résidu de la dernière helice + resiAdd > à la fin de la sequence => arrete la recherche à la fin si non la commence à heliceDebut+resiAdd
                                heliceFinSearch = len(seq.group(1))
                        else :
                                heliceFinSearch = int(heliceFin) + int(resiAdd)

            coupleHH = rechercheHHliste(seq.group(1), heliceDebutSearch, heliceFinSearch) # cree la liste des couples de H séparé par 12 à 14 résidus entre les bornes heliceDebut, heliceFinSearch

            nbCoupleHHValid = 0                                                           # les couples valide doivent etre séparé d'au moins distanceMinCoupleHH résidus
            if len(coupleHH) >= 2 :                                                          # si la sequence contient au moins 2 fois les couples d'H séparées pars 12 à 14 résidus
                for i in range(len(coupleHH)) :

                    for j in range(i+1,len(coupleHH)) :

                        distance = coupleHH[j][0] - coupleHH[i][1] -1                     # calcule toutes les distance entre le debut du second couple (j) et la fin du premier (i)

                        if distance >= distanceMinCoupleHH :                              # si cette distance entre les 2 couples est sup à  distanceMinCoupleHH

                            nbCoupleHHValid = nbCoupleHHValid +1                          # compte le nombre de couple de 2 HH valide séparé de distanceMinCoupleHH


            if nbCoupleHHValid >= 1 :                                           # si la sequence contient au moins 1 fois 2 couples d'HH valide séparées de distanceMinCoupleHH
                prot = prot.replace('\n', '')                                      # suprimme les retour à la ligne     
                fichierOut.write(prot+'\t|\t'+nbHelice.group(1)+'/'+heliceDebut+'-'+heliceFin)      # ajoute la protéine à la liste des retenues
                for i in coupleHH :
                    fichierOut.write('/['+str(int(i[0])+int(heliceDebut)-int(resiAdd)-1)+', '+str(i[1]+int(heliceDebut)-int(resiAdd)-1)+']')                                   # ajoute la protéine à la liste des retenues
                fichierOut.write('\n')

    fichierFasta.close()                                                               # fermeture du fichier fasta
    fichierOut.close()                                                                 # fermeture du fichier output

def rechercheHHliste(seq, resiDebut, resiFin):
    """recherche la présence d'histidines separées de 14 à 14 résidus. Le motif doit etre présent au moins deux fois. L'input est une sequence d'acide aminés. Le programme recherche le motif entre les bornes resiDebut et resiFin.
       Le programme renvoie la liste des couples de H valides."""

    import re

    resiH = []                                                                     # initialise la liste de la position de tous les H
    nbRes = 0                                                                      # conteur du nombre de résidus        
    coupleHHValid = []                                                             # iniialise la liste des couples valide de HH

    for i in seq[resiDebut-1:resiFin] :                                           # lis tous les AA
        nbRes = nbRes + 1
        if i == 'H' :
            resiH.append(nbRes)                                                    # ajoute la position à la liste resiH
    for n in range(len(resiH)) :                                                   # pour tous les indices de la liste contenant l'ensemble des position des H

        for m in range(n+1,len(resiH)) :                                           # pour les indices n+1 jusquà la fin
            distanceHH= resiH[m]-resiH[n]-1                                        # calcule le nombre de résidus entre les 2 H
            if distanceHH >= 12 and distanceHH <= 14 :                             # Si distance entre les HH est entre 12 et 14
                coupleHHValid.append([resiH[n],resiH[m]])                          # Ajoute position des deux H dans liste coupleHHValid
    return (coupleHHValid)

###################################################################################################################
import re

fichierFastaInput = input ('Fichier fasta : ')
if re.search('(.*)\..*',fichierFastaInput) :
    chemin = re.search('(.*)\..*',fichierFastaInput)
    fichierExtractOutput = chemin.group(1)+'-extract.txt'
    fichierNadphOutput = chemin.group(1)+'-extract-NADPH.txt'
    fichierNadphFadOutput = chemin.group(1)+'-extract-NADPH-FAD.txt'
    FichierNadphFadHelixHHOutput = chemin.group(1)+'-extract-NADPH-FAD-HelixHH.txt'
else :
    print ('entrez un chemin valide')
    
MotifNadph = input ('Motif NADPH recherché (G[ISVL]G[VIAF][TAS][PYTA]) :')
if MotifNadph == '' :
    MotifNadph = 'G[ISVL]G[VIAF][TAS][PYTA]'

MotifFad = input ('Motif FAD recherché (H[PSA]F[TS][LIMV]) :')
if MotifFad == '' :
    MotifFad = 'H[PSA]F[TS][LIMV]'

nbMinHelix = input ('nombre minimal d\'helices recherché (3):')
if nbMinHelix == '' :
    nbMinHelix = 3

nbMaxHelix = input ('nombre maximal d\'helices recherché (7):')
if nbMaxHelix == '' :
    nbMaxHelix = 7

resiGap = input ('nombre de résidus à ajouter lors de la recherche de couple HH (5):')
if resiGap == '' :
    resiGap = 5

distanceMinCoupleHH = input ('distance minimum entre deux couples HH valid (20):')
if distanceMinCoupleHH == '' :
    distanceMinCoupleHH = 20

extractFasta(fichierFastaInput, fichierExtractOutput) # cree un fichier contenant toutes les sequences protéiques

rechercheMotif(fichierExtractOutput, fichierNadphOutput, MotifNadph) # cree un fichier contenant  sequences ayant le motif 

rechercheMotif(fichierNadphOutput, fichierNadphFadOutput, MotifFad) # cree un fichier contenant  sequences ayant le motif 

rechercheHelixAndHH(fichierNadphFadOutput, FichierNadphFadHelixHHOutput, nbMinHelix, nbMaxHelix, resiGap, distanceMinCoupleHH)  # cree un fichier contenant  sequences ayant le motif H...H deux fois
