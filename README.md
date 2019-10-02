# NOX analysis 

## 1. Predict NOX proteins in prokaryotes 

In notebook [Predict_NOX_proteins](https://github.com/glaunay/nox-analysis/blob/ch_all_trembl/notebook/Predict_NOX_proteins.ipynb)

* Starts from TrEMBL database (release 2019_02)
* Search NOX domains NAD, FAD and Ferric reductase with HMMER and predict transmembrane helixes with TMHMM
* Filter proteins
    * That contains the 3 domains
    * Between 2 and 7 transmembrane helixes
    * With bi-histidine pattern. Proteins has to have 2 histidines separate by 12 to 14 residues in at least 2 helixes. 
    * Non eukaryotic
    * Evalue filter : domains has to map with evalue <= 1e-3
* Refine domains. Initial used domains are defined with mostly eukaryotes proteins. We take sequences of matched domains in non eukaryotic proteins to create new refined domains and relaunch analysis. 
* Domains are refined until we don't found new proteins. 
