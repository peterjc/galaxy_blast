#!/bin/sh
set -e
echo "This will update test files using the current version of BLAST+"

if [ -f "tools/ncbi_blast_plus/make_ncbi_blast_plus.sh" ]
then
echo "Good, in the expected directory"
else
echo "ERROR. Run this from the GitHub repository root directory."
exit 1
fi

cd test-data

echo rbh_none.tabular
../tools/blast_rbh/blast_rbh.py rhodopsin_nucs.fasta three_human_mRNA.fasta nucl megablast 100 100 rbh_none.tabular

echo rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular
../tools/blast_rbh/blast_rbh.py three_human_mRNA.fasta rhodopsin_nucs.fasta nucl blastn 0 0 rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular

echo rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular
../tools/blast_rbh/blast_rbh.py rhodopsin_nucs.fasta three_human_mRNA.fasta nucl megablast 0 0 rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular 

echo rbh_blastp_four_human_vs_rhodopsin_proteins.tabular
../tools/blast_rbh/blast_rbh.py four_human_proteins.fasta rhodopsin_proteins.fasta prot blastp 0 0 rbh_blastp_four_human_vs_rhodopsin_proteins.tabular 
