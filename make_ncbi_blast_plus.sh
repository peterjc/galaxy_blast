#!/bin/sh
echo "This will create a tar-ball suitable to upload to the toolshed."

if [ -f "make_ncbi_blast_plus.sh" ]
then
echo "Good, in the expected directory"
else
echo "ERROR. Run this from the galaxy tools/ncbi_blast_plus directory."
exit 1
fi

if [ -f "ncbi_blast_plus.tar.gz" ]
then
echo "ERROR. File ncbi_blast_plus.tar.gz already exists."
exit 1
fi

#Create tar file with core XML wrappers
if [ -f "ncbi_blast_plus.tar" ]
then
rm ncbi_blast_plus.tar
fi

#Create tar file (-cf then -rf to add to it)
tar -cf ncbi_blast_plus.tar ncbi_*_wrapper.xml
tar -rf ncbi_blast_plus.tar blastxml_to_tabular.xml
tar -rf ncbi_blast_plus.tar blastxml_to_tabular.py
tar -rf ncbi_blast_plus.tar hide_stderr.py
tar -rf ncbi_blast_plus.tar tool_dependencies.xml
tar -rf ncbi_blast_plus.tar blastdb.loc.sample
tar -rf ncbi_blast_plus.tar blastdb_p.loc.sample
tar -rf ncbi_blast_plus.tar ncbi_blast_plus.txt
tar -rf ncbi_blast_plus.tar test-data/blastp_four_human_vs_rhodopsin.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_four_human_vs_rhodopsin.xml
tar -rf ncbi_blast_plus.tar test-data/blastp_four_human_vs_rhodopsin_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_four_human_vs_rhodopsin_converted_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_four_human_vs_rhodopsin_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_human_vs_pdb_seg_no.xml
tar -rf ncbi_blast_plus.tar test-data/blastp_human_vs_pdb_seg_no_converted_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_human_vs_pdb_seg_no_converted_std.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_rhodopsin_vs_four_human.tabular
tar -rf ncbi_blast_plus.tar test-data/blastp_sample.xml
tar -rf ncbi_blast_plus.tar test-data/blastp_sample_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human.xml
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_converted_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_sample.xml
tar -rf ncbi_blast_plus.tar test-data/blastx_sample_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta
tar -rf ncbi_blast_plus.tar test-data/rhodopsin_nucs.fasta
tar -rf ncbi_blast_plus.tar test-data/rhodopsin_proteins.fasta
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin.html
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin.tabular
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin.xml
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin_parse_deflines.tabular

#Zip the tar file
gzip ncbi_blast_plus.tar

#Check the output
echo "Expect a tar-ball 38 files, have:"
tar -tzf ncbi_blast_plus.tar.gz | wc -l
