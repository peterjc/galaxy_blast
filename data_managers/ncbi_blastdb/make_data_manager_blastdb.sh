#!/bin/sh
echo "This will create a tar-ball suitable to upload to the toolshed."

if [ -f "data_managers/ncbi_blastdb/make_data_manager_blastdb.sh" ]
then
echo "Good, in the expected directory"
else
echo "ERROR. Run this from the GitHub repository root directory."
exit 1
fi

if [ -f "ncbi_blastdb.tar.gz" ]
then
echo "ERROR. File ncbi_blastdb.tar.gz already exists."
exit 1
fi

#Create tar file with core XML wrappers
if [ -f "ncbi_blastdb.tar" ]
then
rm data_manager_blastdb.tar
fi

#Create tar file (-cf then -rf to add to it)
tar -cf  ncbi_blastdb.tar test-data/est_out.json
tar -rf  ncbi_blastdb.tar test-data/cog.out
tar -rf  ncbi_blastdb.tar test-data/pataa.out
tar -rf  ncbi_blastdb.tar test-data/patnt.out
tar -rf  ncbi_blastdb.tar tool-data/blastdb.loc.sample
tar -rf  ncbi_blastdb.tar tool-data/blastdb_p.loc.sample
tar -rf  ncbi_blastdb.tar tool-data/blastdb_d.loc.sample
tar -rf  ncbi_blastdb.tar tool-data/tool_data_table_conf.xml.sample
tar -rf  ncbi_blastdb.tar data_managers/ncbi_blastdb/data_manager_conf.xml
tar -rf  ncbi_blastdb.tar data_managers/ncbi_blastdb/README.rst
tar -rf  ncbi_blastdb.tar data_managers/ncbi_blastdb/tool_dependencies.xml
tar -rf  ncbi_blastdb.tar data_managers/ncbi_blastdb/blastdb.xml
tar -rf  ncbi_blastdb.tar data_managers/ncbi_blastdb/fetch_blast_db.py


#Zip the tar file
gzip ncbi_blastdb.tar

#Check the output
echo "Expect a tar-ball with 13 files, have:"
tar -tzf ncbi_blastdb.tar.gz | wc -l
