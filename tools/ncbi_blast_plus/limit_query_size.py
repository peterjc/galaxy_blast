#!/usr/bin/env python

"""
This program checks if the size of a query file exceeds a configured maximum size. 

Usage example:
limit_query_size.py "$GALAXY_BLAST_QUERYSIZE_MAX" blastn -query "$query" ...other blast options...

The GALAXY_BLAST_QUERYSIZE_MAX parameter can be a number, optionally suffixed by K, M or G for kibibytes, mebibites or gibibytes.
If the parameter is empty the command will be run normally.
"""

from __future__ import print_function, unicode_literals


import sys
import os.path
import re


self = querymax = command = None


def parse_cmdline():
    global self, querymax, command

    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        exit(0)
    if len(sys.argv) < 3:
        print(__doc__)
        exit(1)

    self = os.path.basename(sys.argv[0])
    querymax = sys.argv[1]
    command = sys.argv[2:]
    

def main():
    # If querymax is not set or does not have a proper value, run the command anyway.
    if not querymax:
        exec_command()

    match = re.match(r'^(\d+)([KMG]?)i?$', querymax)
    if match is None:
        print("%s: Warning: Error in query limit format: %s" % (self, querymax), file=sys.stderr)
        exec_command()
    
    value, suffix = match.groups()
    value = int(value)
    if suffix:
        value *= dict(K=1024, M=1024**2, G=1024**3)[suffix]

    if check_query_file_size(value):
        exec_command()

    return 2
    

def check_query_file_size(max_length):
    try:
        i = command.index('-query')
        path = command[i+1]
    except (ValueError, IndexError):
        print("%s: Warning: No '-query' file path found in command" % self)
        return True
    try:
        filesize = os.path.getsize(path)
        if filesize > max_length:
            print("%s: Error: query is larger than %s bytes" % (self, querymax), file=sys.stderr)
            return False
        return True
    except OSError:
        print("%s: Warning: query file '%s' does not exist or is unreadable" % (self, path), file=sys.stderr)
        return True
            

def exec_command():
    try:
        os.execvp(command[0], command)
    except OSError as e:
        print("%s: Error: %s: %s" % (self, command[0], str(e)), file=sys.stderr)
        exit(1)


parse_cmdline()
main()

