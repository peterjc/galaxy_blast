#!/usr/bin/env python3
"""Make FASTA files non-redundant by combining duplicated sequences.

This script takes one or more (optionally gzipped) FASTA filenames as input,
and will return a non-zero error if any duplicate identifiers are found.

Writes output to stdout by default.

Keeps all the sequences in memory, beware!
"""
from __future__ import print_function

import gzip
import os
import sys

from optparse import OptionParser


if "-v" in sys.argv or "--version" in sys.argv:
    print("v0.0.1")
    sys.exit(0)


# Parse Command Line
usage = """Use as follows:

$ python make_nr.py [options] A.fasta [B.fasta ...]

For example,

$ python make_nr.py -o dedup.fasta -s ";" input1.fasta input2.fasta

The input files should be plain text FASTA format, optionally gzipped.

The -a option controls how the representative replacement record for
duplicated records are named. By default the identifiers are taken
in the input file order, combined with the separator. If the -a or
alphasort option is picked, the identifiers are alphabetically sorted
first. This ensures the same names are used even if the input file
order (or the record order within the input files) is randomised.

There is additional guidance in the help text in the make_nr.xml file,
which is shown to the user via the Galaxy interface to this tool.
"""

parser = OptionParser(usage=usage)
parser.add_option("-s", "--sep", dest="sep",
                  default=";",
                  help="Separator character for combining identifiers "
                  "of duplicated records e.g. '|' or ';' (required)")
parser.add_option("-a", "--alphasort", action="store_true",
                  help="When merging duplicated records sort their "
                  "identifiers alphabetically before combining them. "
                  "Default is input file order.")
parser.add_option("-o", "--output", dest="output",
                  default="/dev/stdout", metavar="FILE",
                  help="Output filename (defaults to stdout)")
options, args = parser.parse_args()

if not args:
    sys.exit("Expects at least one input FASTA filename")


def gzip_open(filename):
    """Open a possibly gzipped text file."""
    with open(filename, "rb") as h:
        magic = h.read(2)
    if magic == b'\x1f\x8b':
        return gzip.open(filename, "rt")
    else:
        return open(filename)


def make_nr(input_fasta, output_fasta, sep=";", sort_ids=False):
    """Make the sequences in FASTA files non-redundant.

    Argument input_fasta is a list of filenames.
    """
    by_seq = dict()
    try:
        from Bio.SeqIO.FastaIO import SimpleFastaParser
    except ImportError:
        sys.exit("Missing Biopython")
    for f in input_fasta:
        with gzip_open(f) as handle:
            for title, seq in SimpleFastaParser(handle):
                idn = title.split(None, 1)[0]  # first word only
                seq = seq.upper()
                try:
                    by_seq[seq].append(idn)
                except KeyError:
                    by_seq[seq] = [idn]
    unique = 0
    representatives = dict()
    duplicates = set()
    titles = set()
    for cluster in by_seq.values():
        if len(cluster) > 1:
            # Is it useful to offer to sort here?
            # if sort_ids:
            #     cluster.sort()
            representatives[cluster[0]] = cluster
            duplicates.update(cluster[1:])
        else:
            unique += 1
    del by_seq
    if duplicates:
        # TODO - refactor as a generator with single SeqIO.write(...) call
        with open(output_fasta, "w") as handle:
            for f in input_fasta:
                with gzip_open(f) as in_handle:
                    for title, seq in SimpleFastaParser(in_handle):
                        idn = title.split(None, 1)[0]  # first word only
                        if idn in representatives:
                            cluster = representatives[idn]
                            if sort_ids:
                                cluster.sort()
                            idn = sep.join(cluster)
                            title = "%s representing %i records" % (idn, len(cluster))
                        elif idn in duplicates:
                            continue
                        # TODO - line wrapping
                        if not title in titles:
                            handle.write(">%s\n%s\n" % (title, seq))
                            titles.update([title])
        sys.stderr.write("%i unique entries; removed %i duplicates "
                         "leaving %i representative records\n"
                         % (unique, len(duplicates), len(representatives)))
    else:
        os.symlink(os.path.abspath(input_fasta), output_fasta)
        sys.stderr.write("No perfect duplicates in file, %i unique entries\n"
                         % unique)


make_nr(args, options.output, options.sep, options.alphasort)
