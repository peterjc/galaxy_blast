#!/bin/sh
set -e
echo "This will update test files using the current version of BLAST+"

if [ -f "tools/blast_rbh/update_tests.sh" ]
then
echo "Good, in the expected directory"
else
echo "ERROR. Run this from the GitHub repository root directory."
exit 1
fi

cd test-data

echo rbh_none.tabular
../tools/blast_rbh/blast_rbh.py rhodopsin_nucs.fasta three_human_mRNA.fasta -a nucl -t megablast -i 100 -c 100 -o rbh_none.tabular

echo rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular
../tools/blast_rbh/blast_rbh.py three_human_mRNA.fasta rhodopsin_nucs.fasta -a nucl -t blastn -i 0 -c 0 -o rbh_blastn_three_human_mRNA_vs_rhodopsin_nucs.tabular

echo rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular
../tools/blast_rbh/blast_rbh.py rhodopsin_nucs.fasta three_human_mRNA.fasta -a nucl -t megablast -i 0 -c 0 -o rbh_megablast_rhodopsin_nucs_vs_three_human_mRNA.tabular 

echo rbh_tblastx_rhodopsin_nucs_vs_three_human_mRNA.tabular
../tools/blast_rbh/blast_rbh.py rhodopsin_nucs.fasta three_human_mRNA.fasta -a nucl -t tblastx -i 0 -c 0 -o rbh_tblastx_rhodopsin_nucs_vs_three_human_mRNA.tabular

echo rbh_blastp_four_human_vs_rhodopsin_proteins.tabular
../tools/blast_rbh/blast_rbh.py four_human_proteins.fasta rhodopsin_proteins.fasta -a prot -t blastp -i 0 -c 0 -o rbh_blastp_four_human_vs_rhodopsin_proteins.tabular 

echo rbh_blastp_k12.tabular
../tools/blast_rbh/blast_rbh.py k12_edited_proteins.fasta k12_ten_proteins.fasta -a prot -t blastp -i 0 -c 0 -o rbh_blastp_k12.tabular

echo rbh_blastp_k12_self.tabular
../tools/blast_rbh/blast_rbh.py k12_edited_proteins.fasta k12_edited_proteins.fasta -a prot -t blastp -i 80 -c 80 -o rbh_blastp_k12_self.tabular
