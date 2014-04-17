#!/usr/bin/env python
#Adapted from Dan Blankenberg's data_manager_example_blastdb_ncbi_update_blastdb
#Michael Li, Microbial Biodiversity Bioinformatics group, Agriculture and Agri-Food Canada, April 2014
#Script that downloads preformatted databases from NCBI.

import optparse
import os
import sys
import subprocess
import time
import tarfile
import ftplib
from ftplib import FTP
from galaxy.util.json import from_json_string, to_json_string

def main():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option( '-f', '--filename', dest='filename', action='store', type='string', default=None, help='filename' )
    parser.add_option( '-t', '--tool_data_table_name', dest='tool_data_table_name', action='store', type='string', default=None, help='tool_data_table_name' )
    (options, args) = parser.parse_args()
    
    #Take the JSON input file for parsing
    params = from_json_string( open( options.filename ).read() )
    target_directory = params[ 'output_data' ][0]['extra_files_path']
    os.mkdir( target_directory )

    #Fetch parameters from input JSON file
    blastdb_name = params['param_dict']['db_type'].get( 'blastdb_name' )
    blastdb_type = params['param_dict']['db_type'].get( 'blastdb_type' )
    data_description = params['param_dict']['advanced'].get( 'data_description', None )
    data_id = params['param_dict']['advanced'].get( 'data_id', None )
    
    #update_blastdb.pl doesn't download protein domains, so we use ftp
    if blastdb_type == 'blastdb_d':
        try:
            archive_name = blastdb_name + '_LE.tar.gz'
            tar_file = open( os.path.join( target_directory, archive_name ), "wb" )

            #Connect via ftp and download
            ftp = FTP('ftp.ncbi.nih.gov')
            ftp.login()
            ftp.cwd('pub/mmdb/cdd/little_endian')
            ftp.retrbinary('RETR %s' % archive_name, tar_file.write)
            tar_file.close()

            #Extract contents
            tar_file = tarfile.open(os.path.join( target_directory, archive_name ), mode='r')
            tar_file.extractall( target_directory )
            tar_file.close()

        #If the download fails, ftplib should generate an error in ftplib.all_errors
        #Likewise, tarfile.ReadError should catch any errors when reading from the tar
        #And other possible errors that can occur here...
        except IOError, e:
            print >> sys.stderr, "Cannot create file: %s: %s" % ( archive_name, e )
            sys.exit( 1 )

        except os.error, e:
            print "Error while joining %s and %s: %s" % ( target_directory, archive_name, e )
            sys.exit( 1 )

        except ftplib.all_errors, e:
            print >> sys.stderr, "Error while downloading protein domain database: %s" % ( e )
            sys.exit( 1 )

        except tarfile.TarError, e:
            print >> sys.stderr, "Error while opening/extracting the tar file: %s" % ( e )
            sys.exit( 1 )

    else:
        #Run update_blastdb.pl
        cmd_options = [ '--decompress' ]
        args = [ 'update_blastdb.pl' ] + cmd_options + [ blastdb_name ]
        proc = subprocess.Popen( args=args, shell=False, cwd=target_directory )
        return_code = proc.wait()

        #Check if download was successful (exit code 1)
        if return_code != 1:
            print >> sys.stderr, "Error obtaining blastdb (%s)" % return_code
            sys.exit( 1 )
    
    #Set id and description if not provided in the advanced settings
    if not data_id:
        #Use download time to create uniq id
        localtime = time.localtime()
        timeString = time.strftime("%Y_%m_%d", localtime)
        data_id = "%s_%s" % ( blastdb_name, timeString )
    
    # Attempt to automatically set description from alias file
    # Protein domain databases don't have an alias file
    if not data_description and blastdb_type != 'blastdb_d':
        alias_date = None
        alias_file = None
        try:
            if blastdb_type == 'blastdb':
                alias_file = "%s.nal" % ( blastdb_name )
            if blastdb_type == 'blastdb_p':
                alias_file = "%s.pal" % ( blastdb_name )
            if alias_file:
                for line in open( os.path.join( target_directory, alias_file ) ):
                    if line.startswith( '# Alias file created ' ):
                        alias_date = line.split( '# Alias file created ', 1 )[1].strip()
                    if line.startswith( '# Date created: ' ):
                        alias_date = line.split( '# Date created: ', 1)[1].strip()
                    if line.startswith( 'TITLE' ):
                        data_description = line.split( None, 1 )[1].strip()
                        break
        except Exception, e:
            print >> sys.stderr, "Error Parsing Alias file for TITLE and date: %s" % ( e )
        #If we manage to parse the pal or nal file, set description
        if alias_date and data_description:
            data_description = "%s (%s)" % ( data_description, alias_date )
    
    #If we could not parse the nal or pal file for some reason
    if not data_description:
        data_description = data_id
    
    #Prepare output string to convert into JSON format
    data_table_entry = { 'value':data_id, 'name':data_description, 'path': os.path.join( blastdb_name, data_id ), 'database_alias_name': blastdb_name }
    data_manager_dict = { 'data_tables': { options.tool_data_table_name: [ data_table_entry ]  } }
    
    #save info to json file
    with open( options.filename, 'wb' ) as fh:
        fh.write( to_json_string( data_manager_dict ) )

if __name__ == "__main__":
    main()
