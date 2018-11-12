#!/usr/bin/env python
"""BLAST find and extend.

Run "find_and_extend.py -h" to see the help text, or read the associated
find_and_extend.xml and README.rst files which are available on GitHub at:
https://github.com/peterjc/galaxy_blast/tree/master/tools/find_and_extend

This requires Python and the NCBI BLAST+ tools to be installed and on the
``$PATH``.

You can also run this tool via Galaxy using the "find_and_extend.xml"
definition file. This is available as a package on the Galaxy
Tool Shed: http://toolshed.g2.bx.psu.edu/view/peterjc/find_and_extend
"""

from __future__ import print_function

import os
import shutil
import sys
import tempfile

from optparse import OptionParser


def run(cmd):
    """Run the given command line string."""
    return_code = os.system(cmd)
    if return_code:
        sys.exit("Error %i from: %s" % (return_code, cmd))


if "--version" in sys.argv[1:]:
    # TODO - Capture version of BLAST+ binaries too?
    print("BLAST find and extend v0.0.1")
    sys.exit(0)

try:
    threads = int(os.environ.get("GALAXY_SLOTS", "1"))
except ValueError:
    threads = 1
assert 1 <= threads, threads

# Parse Command Line
usage = """Use as follows:

$ python find_and_extend.py [options] -q query.fasta -d blast_database -o matches.fasta

There is additional guidance in the help text in the find_and_extend.xml
file, which is shown to the user via the Galaxy interface to this tool.
"""

parser = OptionParser(usage=usage)
parser.add_option("-q", "--query", dest="query",
                  default=None, metavar="FILE",  # required=True,
                  help="Input query FASTA filename (required)")
parser.add_option("-d", "--database", dest="database",
                  default=None, metavar="FILE",  # required=True,
                  help="Input BLAST nucleotide database (required)")
parser.add_option("-f", "--dbfasta", dest="dbfasta",
                  default=None, metavar="FILE",
                  help="FASTA file the database was made from. "
                  "If ommitted, looks for based on the DB name, "
                  "and failing that regenerates it with blastdbcmd.")
parser.add_option("-o", "--output", dest="output",
                  default=None, metavar="FILE",  # required=True,
                  help="Output FASTA filename (required)")
parser.add_option("-b", "--output_blast", dest="output_blast",
                  default=None, metavar="FILE",
                  help="Output BLAST tabular results (optional, for debugging)")
parser.add_option("-i", "--identity", dest="min_identity",
                  default="95",
                  help="Minimum percentage identity (optional, default 95)")
parser.add_option("-c", "--coverage", dest="min_coverage",
                  default="95",
                  help="Minimum HSP coverage (optional, default 95)")
parser.add_option("-x", "--max_target_seqs", dest="max_target_seqs",
                  default="1",
                  help="How many matches to return (BLAST+ setting -max_target_seqs, default 1)")
parser.add_option("--up", dest="up",
                  default="50",
                  help="Extend upstream (start) by this many base pairs (optional, default 50)")
parser.add_option("--down", dest="down",
                  default="50",
                  help="Extend downstream (end) by this many base pairs (optional, default 50)")
parser.add_option("-t", "--threads", dest="threads",
                  default=threads,
                  help="Number of threads when running BLAST. Defaults to the "
                       "$GALAXY_SLOTS environment variable if set, or 1.")
options, args = parser.parse_args()

try:
    from Bio.SeqRecord import SeqRecord
    from Bio import SeqIO
except ImportError:
    sys.exit("Missing Biopython")

if args:
    sys.exit("No positional arguments expected.")
if not options.query:
    sys.exit("Missing required argument for input FASTA file")
if not options.database:
    sys.exit("Missing required argument for BLAST database")
if options.query == options.dbfasta:
    sys.exit("Check your arguments, query & database FASTA files should be different.")

if not os.path.isfile(options.query):
    sys.exit("Missing input query FASTA file: %r" % options.query)
query_file = options.query

if not options.output:
    sys.exit("Output filename required, e.g. -o matches.fasta")
out_file = options.output

try:
    min_identity = float(options.min_identity)
except ValueError:
    sys.exit("Expected number between 0 and 100 for "
             "minimum identity, not %r" % min_identity)
if not (0 <= min_identity <= 100):
    sys.exit("Expected minimum identity between 0 and 100, not %0.2f" % min_identity)

try:
    min_coverage = float(options.min_coverage)
except ValueError:
    sys.exit("Expected number between 0 and 100 for "
             "minimum coverage, not %r" % min_coverage)
if not (0 <= min_coverage <= 100):
    sys.exit("Expected minimum coverage between 0 and 100, not %0.2f" % min_coverage)

try:
    max_target_seqs = int(options.max_target_seqs)
except ValueError:
    sys.exit("Expected positive integer for "
             "maximum matches (max_target_seqs), not %r" % max_target_seqs)
if max_target_seqs < 0:
    sys.exit("Expected positive integer for "
             "maximum matches (max_target_seqs), not %r" % max_target_seqs)

try:
    up_extend = int(options.up)
except ValueError:
    sys.exit("Expected positive or zero integer for "
             "number of bases to extend upstream, not %r" % options.up)
if up_extend < 0:
    sys.exit("Expected positive or zero integer for "
             "number of bases to extend upstream, not %r" % up_extend)

try:
    down_extend = int(options.down)
except ValueError:
    sys.exit("Expected positive or zero integer for "
             "number of bases to extend downstream, not %r" % options.down)
if down_extend < 0:
    sys.exit("Expected positive or zero integer for "
             "number of bases to extend downstream, not %r" % down_extend)

try:
    threads = int(options.threads)
except ValueError:
    sys.exit("Expected positive integer for number of threads, not %r" % options.threads)
if threads < 1:
    sys.exit("Expected positive integer for number of threads, not %r" % threads)


base_path = tempfile.mkdtemp()
if options.output_blast:
    tabular_file = options.output_blast
else:
    tabular_file = os.path.join(base_path, "matches.tabular")
log = os.path.join(base_path, "blast.log")

db_fasta = None
if options.dbfasta:
    db_fasta = options.dbfasta
    db_dict = SeqIO.index(db_fasta, "fasta")
    if db_dict:
        sys.stderr.write("Indexed %i entries in %s\n" % (len(db_dict), db_fasta))
    else:
        sys.stderr.write("ERROR: %s does not seem to be a FASTA file (or is empty)" % db_fasta)
if not db_fasta:
    for ext in ("", ".fasta", ".fa", ".ffn", ".fna", ".faa"):
        tmp = options.database + ext
        if os.path.isfile(tmp):
            db_fasta = tmp
            db_dict = SeqIO.index(db_fasta, "fasta")
            if db_dict:
                sys.stderr.write("Indexed %i entries in %s\n" % (len(db_dict), db_fasta))
                break
            else:
                sys.stderr.write("WARNING: %s does not seem to be a FASTA file, ignoring it" % tmp)
if not db_fasta:
    db_fasta = os.path.join(base_path, "database.fasta")
    sys.stderr.write("Calling blastdbcmd to convert DB to a temporary FASTA files\n")
    run("blastdbcmd -db '%s' -entry all -out '%s'" % (options.database, db_fasta))
    db_dict = SeqIO.index(db_fasta, "fasta")
    sys.stderr.write("Indexed %i entries from database\n" % len(db_dict))


cols = "qseqid sseqid pident qcovhsp sstart send slen"  # Or qcovs?
c_query = 0
c_match = 1
c_identity = 2
c_coverage = 3
c_sstart = 4
c_send = 5
c_slen = 6

# print("Starting...")

# TODO - Report log in case of error?
# print("BLAST databases prepared.")
run('blastn -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
    % (options.query, options.database, tabular_file, cols, threads))
# print("BLAST search done.")


def extract_candidates(blast_tabular_filename):
    """Iterate over BLAST tabular, returning tuple.

    Yields tuple of (qseqid, sseqid, sstart, send, slen)

    Will apply the filters set at the command line.
    """
    col_count = len(cols.split())
    with open(blast_tabular_filename) as h:
        for line in h:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != col_count:
                # Using NCBI BLAST+ 2.2.27 the undefined field is ignored
                # Even NCBI BLAST+ 2.5.0 silently ignores unknown fields :(
                sys.exit("Old version of NCBI BLAST? Expected %i columns, got %i:\n%s\n"
                         "Note the qcovhsp field was only added in version 2.2.28\n"
                         % (col_count, len(parts), line))
            if float(parts[c_identity]) < min_identity or float(parts[c_coverage]) < min_coverage:
                continue
            yield parts[c_query], parts[c_match], int(parts[c_sstart]), int(parts[c_send]), int(parts[c_slen])


def generate_extended_records(tabular_file):
    """Yield SeqRecord objects based on BLAST hits."""
    for query, match, start, end, length in extract_candidates(tabular_file):
        # print(query, match, start, end, length)

        if start <= end:
            assert 1 <= start < end <= length
            reverse_comp = False
            left_cut = max(1, start - up_extend) - 1  # Python counting!
            right_cut = min(end + down_extend, length)
        else:
            assert 1 <= end < start <= length
            reverse_comp = True
            left_cut = max(1, end - down_extend) - 1  # Python counting!
            right_cut = min(start + up_extend, length)

        # This is what I wanted to do, but NCBI BLAST+ suite does not
        # allow this workflow unless you are using NCBI style naming:
        #
        # run('blastdbcmd -db %s -entry "%s" -range "%i-%i"'
        #     % (options.database, match, req_start, req_end))
        try:
            seq = db_dict[match].seq
        except KeyError:
            sys.exit("Inconsistency, can't find %s from BLAST result in FASTA file" % match)
        if len(seq) != length:
            sys.exit("Inconsistent length for %s from FASTA entry and BLAST result, %i vs %i"
                     % (match, len(seq), length))

        seq = seq[left_cut:right_cut]
        if reverse_comp:
            seq = seq.reverse_complement()

        yield SeqRecord(id="%s_plus_%s" % (query, match),
                        description="",
                        seq=seq)


count = SeqIO.write(generate_extended_records(tabular_file), out_file, "fasta")

sys.stderr.write("%i candidates\n" % count)

# Remove temp files...
shutil.rmtree(base_path)
