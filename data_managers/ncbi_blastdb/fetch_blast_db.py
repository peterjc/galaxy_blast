#!/usr/bin/env python
# Dan Blankenberg
# Script that calls update_blastdb.pl to download preformatted databases

from __future__ import print_function

import hashlib
import optparse
import os
import subprocess
import sys

from galaxy.util.json import from_json_string, to_json_string
DEFAULT_ALGORITHM = hashlib.sha512
CHUNK_SIZE = 2**20  # 1mb


def get_dir_hash(directory, algorithm=None, followlinks=True, chunk_size=None):
    chunk_size = chunk_size or CHUNK_SIZE
    algorithm = algorithm or DEFAULT_ALGORITHM
    if isinstance(algorithm, basestring):
        hash = hashlib.new(algorithm)
    else:
        hash = algorithm()
    # we hash a directory by taking names of directories, files and their
    # contents
    for dirpath, dirnames, filenames in os.walk(directory, followlinks=followlinks):
        dirnames.sort()
        filenames.sort()
        for name in dirnames:
            hash.update(os.path.relpath(
                os.path.join(dirpath, name), directory))
        for name in filenames:
            filename = os.path.join(dirpath, name)
            hash.update(os.path.relpath(filename, directory))
            fh = open(filename, 'rb')
            while True:
                data = fh.read(chunk_size)
                if not data:
                    break
                hash.update(data)
            fh.close()

    return hash.hexdigest()


def main():
    # Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option('-f', '--filename', dest='filename',
                      action='store', type='string', default=None, help='filename')
    parser.add_option('-t', '--tool_data_table_name', dest='tool_data_table_name',
                      action='store', type='string', default=None, help='tool_data_table_name')
    (options, args) = parser.parse_args()

    params = from_json_string(open(options.filename).read())
    target_directory = params['output_data'][0]['extra_files_path']
    os.mkdir(target_directory)

    blastdb_name = params['param_dict']['blastdb_name']  # value
    data_description = params['param_dict'][
        'advanced'].get('data_description', None)
    data_id = params['param_dict']['advanced'].get('data_id', None)

    cmd_options = ['--decompress']

    args = ['update_blastdb.pl'] + cmd_options + [blastdb_name]
    proc = subprocess.Popen(args=args, shell=False, cwd=target_directory)
    return_code = proc.wait()
    if return_code != 1:
        sys.exit("Error obtaining blastdb (%s)" % return_code)

    if not data_id:
        data_id = "%s_%s" % (blastdb_name, get_dir_hash(target_directory))

    if not data_description:
        alias_date = None
        try:
            for line in open(os.path.join(target_directory, "%s.nal" % (blastdb_name))):
                if line.startswith('# Alias file created '):
                    alias_date = line.split(
                        '# Alias file created ', 1)[1].strip()
                if line.startswith('TITLE'):
                    data_description = line.split(None, 1)[1].strip()
                    break
        except Exception as e:
            sys.stderr.write("Error Parsing Alias file for TITLE and date: %s\n" % e)
        if alias_date and data_description:
            data_description = "%s (%s)" % (data_description, alias_date)

    if not data_description:
        data_description = data_id

    data_table_entry = {'value': data_id, 'name': data_description, 'path': os.path.join(
        blastdb_name, data_id), 'nucleotide_alias_name': blastdb_name}
    data_manager_dict = {'data_tables': {
        options.tool_data_table_name: [data_table_entry]}}

    # save info to json file
    with open(options.filename, 'wb') as fh:
        fh.write(to_json_string(data_manager_dict))


if __name__ == "__main__":
    main()
