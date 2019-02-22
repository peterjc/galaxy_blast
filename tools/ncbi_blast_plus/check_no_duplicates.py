#!/usr/bin/env python
"""Check for duplicate sequence identifiers in FASTA files.

This is run as a pre-check before makeblastdb, in order to avoid
a regression bug in BLAST+ 2.2.28 which fails to catch this. See:
http://blastedbio.blogspot.co.uk/2012/10/my-ids-not-good-enough-for-ncbi-blast.html

This script takes one or more FASTA filenames as input, and
will return a non-zero error if any duplicate identifiers
are found.
"""
import gzip
import os
import sys


if "-v" in sys.argv or "--version" in sys.argv:
    print("v0.0.23")
    sys.exit(0)

identifiers = set()
files = 0
for filename in sys.argv[1:]:
    if not os.path.isfile(filename):
        sys.stderr.write("Missing FASTA file %r\n" % filename)
        sys.exit(2)
    files += 1

    with open(filename, "rb") as binary_handle:
        magic = binary_handle.read(2)
    if not magic:
        # Empty file, special case
        continue
    elif magic == b"\x1f\x8b":
        # Gzipped
        handle = gzip.open(filename, "rt")
    elif magic[0:1] == b">":
        # Not gzipped, shoudl be plain FASTA
        handle = open(filename, "r")

    for line in handle:
        if line.startswith(">"):
            # The split will also take care of the new line character,
            # e.g. ">test\n" and ">test description here\n" both give "test"
            seq_id = line[1:].split(None, 1)[0]
            if seq_id in identifiers:
                handle.close()
                sys.exit("Repeated identifiers, e.g. %r" % seq_id)
            identifiers.add(seq_id)
    handle.close()
if not files:
    sys.stderr.write("No FASTA files given to check for duplicates\n")
    sys.exit(3)
elif files == 1:
    print("%i sequences" % len(identifiers))
else:
    print("%i sequences in %i FASTA files" % (len(identifiers), files))
