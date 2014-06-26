#!/usr/bin/env python

"""
limit_query_size.py [-q] querysize_max command... -query file ...

This program checks if the size of a query file exceeds a configured
maximum size.

Usage example:
limit_query_size.py "$GALAXY_BLAST_QUERYSIZE_MAX" blastn -query "$query" ...other blast options...

The querysize_max parameter can be a number, optionally suffixed by K,
M or G for kibibytes, mebibites or gibibytes. This program will search
for a '-query' option with a file argument, and verify that the file
is no larger than querysize_max. If so, limit_querysize.py will
execute the command, else it will print an error and not execute the
command. If the querysize_max parameter is empty the command will be
run normally.
"""

from __future__ import print_function, unicode_literals


import sys
import os.path
import re
import optparse
from optparse import OptionParser


self = querymax = command = quiet = None


def parse_cmdline():
    global self, querymax, command, quiet

    parser = OptionParser(usage=__doc__.rstrip())
    parser.add_option('-q', '--quiet', dest='quiet', action='count', default=0,
                      help="Don't print warning messages. Specify twice to also disable printing error messages.")
    parser.disable_interspersed_args()
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        exit(1)

    self = os.path.basename(sys.argv[0])
    querymax = args[0]
    command = args[1:]
    quiet = options.quiet
    

def main():
    # If querymax is not set or does not have a proper value, run the command anyway.
    if not querymax:
        exec_command()

    match = re.match(r'^(\d+)([KMG]?)(?:iB?)?$', querymax)
    if match is None:
        warn("Error in query limit format: %s" % querymax)
        exec_command()
    
    value, suffix = match.groups()
    value = int(value)
    if suffix:
        value *= dict(K=1024, M=1024**2, G=1024**3)[suffix]

    if check_query_file_size(value):
        exec_command()
        # exec_command does not return
    else:
        exit(2)

def warn(str):
    if quiet < 1:
        print("%s: Warning: %s" % (self, str), file=sys.stderr)

def err(str):
    if quiet < 2:
        print("%s: Error: %s" % (self, str), file=sys.stderr)
    

def check_query_file_size(max_length):
    try:
        i = command.index('-query')
        path = command[i+1]
    except (ValueError, IndexError):
        warn("No '-query' file path found in command")
        return True
    try:
        filesize = os.path.getsize(path)
        if filesize > max_length:
            err("query size too large (size %s bytes, max %s)" % (filesize, querymax))
            return False
        return True
    except OSError:
        warn("query file '%s' does not exist or is unreadable" % path)
        return True
            

def exec_command():
    try:
        os.execvp(command[0], command)
    except OSError as e:
        err("%s: %s" % (command[0], str(e)))
        exit(1)


parse_cmdline()
main()

