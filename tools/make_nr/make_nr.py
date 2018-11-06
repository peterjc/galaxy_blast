#!/usr/bin/env python3
"""Check for combining duplicate sequence in FASTA files.

This script takes one or more FASTA filenames as input, and
will return a non-zero error if any duplicate identifiers
are found. Writes output to stdout.

Keeps all the sequences in memory, beware!
"""
from __future__ import print_function

import gzip
import os
import sys

from optparse import OptionParser

from Bio.SeqIO.FastaIO import SimpleFastaParser

if "-v" in sys.argv or "--version" in sys.argv:
    print("v0.0.0")
    sys.exit(0)


# Parse Command Line
usage = """Use as follows:

$ python make_nr.py [options] A.fasta [B.fasta ...]

For example,

$ python make_nr.py -o dedup.fasta -s ";" input1.fasta input2.fasta

There is additional guidance in the help text in the make_nr.xml file,
which is shown to the user via the Galaxy interface to this tool.
"""

parser = OptionParser(usage=usage)
parser.add_option("-s", "--sep", dest="sep",
                  default=";",
                  help="Separator character for combining identifiers of duplicated records e.g. '|' or ';' (required)")
parser.add_option("-o", "--output", dest="output",
                  default="/dev/stdout", metavar="FILE",
                  help="Output filename (defaults to stdout)")
options, args = parser.parse_args()

if not args:
    sys.exit("Expects at least one input FASTA filename")


def make_nr(input_fasta, output_fasta, sep=";"):
    """Make the sequences in a FASTA file non-redundant."""
    by_seq = dict()
    try:
        from Bio import SeqIO
    except KeyError:
        sys.exit("Missing Biopython")
    for record in SeqIO.parse(input_fasta, "fasta"):
        s = str(record.seq).upper()
        try:
            by_seq[s].append(record.id)
        except KeyError:
            by_seq[s] = [record.id]
    unique = 0
    representatives = dict()
    duplicates = set()
    for cluster in by_seq.values():
        if len(cluster) > 1:
            representatives[cluster[0]] = cluster
            duplicates.update(cluster[1:])
        else:
            unique += 1
    del by_seq
    if duplicates:
        # TODO - refactor as a generator with single SeqIO.write(...) call
        with open(output_fasta, "w") as handle:
            for record in SeqIO.parse(input_fasta, "fasta"):
                if record.id in representatives:
                    cluster = representatives[record.id]
                    record.id = sep.join(cluster)
                    record.description = "representing %i records" % len(cluster)
                elif record.id in duplicates:
                    continue
                SeqIO.write(record, handle, "fasta")
        print("%i unique entries; removed %i duplicates leaving %i representative records"
              % (unique, len(duplicates), len(representatives)))
    else:
        os.symlink(os.path.abspath(input_fasta), output_fasta)
        print("No perfect duplicates in file, %i unique entries" % unique)

if len(args) > 1:
    sys.exit("Sorry, currently only one input FASTA file is supported.")
make_nr(args[0], options.output, options.sep)
