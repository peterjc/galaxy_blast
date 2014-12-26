#!/bin/sh
echo "This will create a tar-ball suitable to upload to the toolshed."

if [ -f "tools/ncbi_blast_plus/make_ncbi_blast_plus.sh" ]
then
echo "Good, in the expected directory"
else
echo "ERROR. Run this from the GitHub repository root directory."
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
tar -cf ncbi_blast_plus.tar tools/ncbi_blast_plus/repository_dependencies.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_macros.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_blastdbcmd_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_blastn_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_blastp_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_blastx_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_tblastn_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_tblastx_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_makeblastdb.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_makeprofiledb.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/check_no_duplicates.py
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_blastdbcmd_info.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_rpsblast_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_rpstblastn_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_dustmasker_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_segmasker_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_convert2blastmask_wrapper.xml
#tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/ncbi_deltablast_wrapper.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/blastxml_to_tabular.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/blastxml_to_tabular.py
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/tool_dependencies.xml
tar -rf ncbi_blast_plus.tar tools/ncbi_blast_plus/README.rst
tar -rf ncbi_blast_plus.tar tool-data/tool_data_table_conf.xml.sample
tar -rf ncbi_blast_plus.tar tool-data/blastdb.loc.sample
tar -rf ncbi_blast_plus.tar tool-data/blastdb_p.loc.sample
tar -rf ncbi_blast_plus.tar tool-data/blastdb_d.loc.sample
tar -rf ncbi_blast_plus.tar test-data/tool_data_table_conf.xml.test
tar -rf ncbi_blast_plus.tar test-data/blastdb.loc
tar -rf ncbi_blast_plus.tar test-data/blastdb_p.loc
tar -rf ncbi_blast_plus.tar test-data/blastdb_d.loc
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
tar -rf ncbi_blast_plus.tar test-data/blastn_arabidopsis.xml
tar -rf ncbi_blast_plus.tar test-data/blastn_arabidopsis.extended.tabular
tar -rf ncbi_blast_plus.tar test-data/blastn_arabidopsis.standard.tabular
tar -rf ncbi_blast_plus.tar test-data/blastn_rhodopsin_vs_three_human.xml
tar -rf ncbi_blast_plus.tar test-data/blastn_rhodopsin_vs_three_human.tabular
tar -rf ncbi_blast_plus.tar test-data/blastn_rhodopsin_vs_three_human.columns.tabular
tar -rf ncbi_blast_plus.tar test-data/blastn_rhodopsin_vs_three_human_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human.xml
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_converted_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_rhodopsin_vs_four_human_all.tabular
tar -rf ncbi_blast_plus.tar test-data/blastx_sample.xml
tar -rf ncbi_blast_plus.tar test-data/blastx_sample_converted.tabular
tar -rf ncbi_blast_plus.tar test-data/tblastx_rhodopsin_vs_three_human.tabular
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_masked.fasta
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.log.txt
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.phd
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.phi
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.phr
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.pin
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.pog
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.psd
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.psi
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.fasta.psq
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins.dbinfo.txt
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.log.txt
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.phd
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.phi
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.phr
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.pin
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.pog
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.psd
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.psi
tar -rf ncbi_blast_plus.tar test-data/four_human_proteins_taxid.fasta.psq
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.log.txt
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.ndh
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nhi
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nhr
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nin
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nog
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nsd
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nsi
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.fasta.nsq
tar -rf ncbi_blast_plus.tar test-data/three_human_mRNA.dbinfo.txt
tar -rf ncbi_blast_plus.tar test-data/rhodopsin_nucs.fasta
tar -rf ncbi_blast_plus.tar test-data/rhodopsin_proteins.fasta
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin.html
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin.tabular
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin.xml
tar -rf ncbi_blast_plus.tar test-data/tblastn_four_human_vs_rhodopsin_ext.tabular
tar -rf ncbi_blast_plus.tar test-data/dustmasker_three_human.fasta
tar -rf ncbi_blast_plus.tar test-data/dustmasker_three_human.maskinfo-asn1
tar -rf ncbi_blast_plus.tar test-data/dustmasker_three_human.maskinfo-asn1-binary
tar -rf ncbi_blast_plus.tar test-data/segmasker_four_human.fasta
tar -rf ncbi_blast_plus.tar test-data/segmasker_four_human.maskinfo-asn1
tar -rf ncbi_blast_plus.tar test-data/segmasker_four_human.maskinfo-asn1-binary
tar -rf ncbi_blast_plus.tar test-data/convert2blastmask_four_human_masked.maskinfo-asn1
tar -rf ncbi_blast_plus.tar test-data/convert2blastmask_four_human_masked.maskinfo-asn1-binary
tar -rf ncbi_blast_plus.tar test-data/cd00003.smp
tar -rf ncbi_blast_plus.tar test-data/cd00008.smp
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.aux
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.loo
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.pin
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.psi
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.rps
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.freq
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.phr
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.psd
tar -rf ncbi_blast_plus.tar test-data/cd00003_and_cd00008.psq
tar -rf ncbi_blast_plus.tar test-data/empty_file.dat

#Zip the tar file
gzip ncbi_blast_plus.tar

#Check the output
echo "Expect a tar-ball with 113 files, have:"
tar -tzf ncbi_blast_plus.tar.gz | wc -l
