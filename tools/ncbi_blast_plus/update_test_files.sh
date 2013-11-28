#!/bin/sh
echo "This will update test files using the current version of BLAST+"

if [ -f "tools/ncbi_blast_plus/make_ncbi_blast_plus.sh" ]
then
echo "Good, in the expected directory"
else
echo "ERROR. Run this from the GitHub repository root directory."
exit 1
fi

cd test-data

export EXT="6 std sallseqid score nident positive gaps ppos qframe sframe qseq sseq qlen slen salltitles"

echo
echo makeblastdb
echo ===========
#Doing this first in case future tests use one of the local databases

echo "four_human_proteins.fasta"
makeblastdb -out four_human_proteins.fasta -hash_index -in four_human_proteins.fasta  -title "Just 4 human proteins" -dbtype prot

echo
echo Main
echo ====

echo "blastn_rhodopsin_vs_three_human.tabular"
blastn -query rhodopsin_nucs.fasta -subject three_human_mRNA.fasta -task megablast -evalue 1e-40 -out blastn_rhodopsin_vs_three_human.tabular -outfmt 6

echo "blastp_four_human_vs_rhodopsin.xml"
blastp -query four_human_proteins.fasta -subject rhodopsin_proteins.fasta -task blastp -evalue 1e-08 -out blastp_four_human_vs_rhodopsin.xml -outfmt 5 -seg no -matrix BLOSUM62 -parse_deflines

echo "blastp_four_human_vs_rhodopsin_ext.tabular"
blastp -query four_human_proteins.fasta -subject rhodopsin_proteins.fasta -task blastp -evalue 1e-08 -out blastp_four_human_vs_rhodopsin_ext.tabular -outfmt "$EXT" -seg no -matrix BLOSUM62 -parse_deflines

echo "blastx_rhodopsin_vs_four_human.xml"
blastx -query rhodopsin_nucs.fasta -subject four_human_proteins.fasta -query_gencode 1 -evalue 1e-10 -out blastx_rhodopsin_vs_four_human.xml -outfmt 5

echo "blastx_rhodopsin_vs_four_human.tabular"
blastx -query rhodopsin_nucs.fasta -subject four_human_proteins.fasta -query_gencode 1 -evalue 1e-10 -out blastx_rhodopsin_vs_four_human.tabular -outfmt 6

echo "blastx_rhodopsin_vs_four_human_ext.tabular"
blastx -query rhodopsin_nucs.fasta -subject four_human_proteins.fasta -query_gencode 1 -evalue 1e-10 -out blastx_rhodopsin_vs_four_human_ext.tabular -outfmt "$EXT"

echo "tblastn_four_human_vs_rhodopsin.xml"
tblastn -query four_human_proteins.fasta -subject rhodopsin_nucs.fasta -evalue 1e-10 -out tblastn_four_human_vs_rhodopsin.xml -outfmt 5 -db_gencode 1 -seg no -matrix BLOSUM80

echo "tblastn_four_human_vs_rhodopsin.html"
tblastn -query four_human_proteins.fasta -subject rhodopsin_nucs.fasta -evalue 1e-10 -out tblastn_four_human_vs_rhodopsin.html -outfmt 0 -html -db_gencode 1 -seg no -matrix BLOSUM80

echo "tblastn_four_human_vs_rhodopsin_ext.tabular"
tblastn -query four_human_proteins.fasta -subject rhodopsin_nucs.fasta -evalue 1e-10 -out tblastn_four_human_vs_rhodopsin_ext.tabular -outfmt "$EXT" -db_gencode 1 -seg no -matrix BLOSUM80

echo "tblastx_rhodopsin_vs_three_human.tabular"
tblastx -query rhodopsin_nucs.fasta -subject three_human_mRNA.fasta -evalue 1e-40 -out tblastx_rhodopsin_vs_three_human.tabular -outfmt 6

echo
echo blastxml_to_tabular
echo ===================

echo "blastp_four_human_vs_rhodopsin_converted.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastp_four_human_vs_rhodopsin.xml blastp_four_human_vs_rhodopsin_converted.tabular std

echo "blastp_four_human_vs_rhodopsin_converted_ext.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastp_four_human_vs_rhodopsin.xml blastp_four_human_vs_rhodopsin_converted_ext.tabular ext

echo "blastp_sample_converted.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastp_sample.xml blastp_sample_converted.tabular std

echo "blastx_rhodopsin_vs_four_human_converted.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastx_rhodopsin_vs_four_human.xml blastx_rhodopsin_vs_four_human_converted.tabular std

echo "blastx_rhodopsin_vs_four_human_converted_ext.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastx_rhodopsin_vs_four_human.xml blastx_rhodopsin_vs_four_human_converted_ext.tabular ext

echo "blastx_sample_converted.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastx_sample.xml blastx_sample_converted.tabular std

echo "blastp_human_vs_pdb_seg_no_converted_std.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastp_human_vs_pdb_seg_no.xml blastp_human_vs_pdb_seg_no_converted_std.tabular std

echo "blastp_human_vs_pdb_seg_no_converted_ext.tabular"
python ../tools/ncbi_blast_plus/blastxml_to_tabular.py blastp_human_vs_pdb_seg_no.xml blastp_human_vs_pdb_seg_no_converted_ext.tabular ext

echo
echo deltablast
echo ==========

#It will be a problem if the exact version of the cdd_delta database alters the test output...
#Following (or similar) works for deltablast to find the cdd_delta database automatically:
#export BLASTDB=/data/blastdb/ncbi/cdd:/data/blastdb/ncbi
#Or, we can make it explicit (but specific to local setup) via -rpsdb
export CDD_DELTA=/data/blastdb/ncbi/cdd/cdd_delta

echo "deltablast_four_human_vs_rhodopsin.xml"
deltablast -query four_human_proteins.fasta -subject rhodopsin_proteins.fasta -evalue 1e-08 -out deltablast_four_human_vs_rhodopsin.xml -outfmt 5 -matrix BLOSUM62 -seg no -parse_deflines -rpsdb $CDD_DELTA

echo "deltablast_four_human_vs_rhodopsin.tabular"
deltablast -query four_human_proteins.fasta -subject rhodopsin_proteins.fasta -evalue 1e-08 -out deltablast_four_human_vs_rhodopsin.tabular -outfmt 6 -matrix BLOSUM62 -seg no -parse_deflines -rpsdb $CDD_DELTA

echo "deltablast_four_human_vs_rhodopsin_ext.tabular"
deltablast -query four_human_proteins.fasta -subject rhodopsin_proteins.fasta -evalue 1e-08 -out deltablast_four_human_vs_rhodopsin_ext.tabular -outfmt "$EXT" -matrix BLOSUM62 -seg no -parse_deflines -rpsdb $CDD_DELTA

echo "deltablast_rhodopsin_vs_four_human.tabular"
deltablast -query rhodopsin_proteins.fasta -subject four_human_proteins.fasta -evalue 1e-08 -out deltablast_rhodopsin_vs_four_human.tabular -outfmt 6 -rpsdb $CDD_DELTA
