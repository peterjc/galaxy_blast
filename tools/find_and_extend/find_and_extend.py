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
    print("BLAST RBH v0.1.11")
    sys.exit(0)

try:
    threads = int(os.environ.get("GALAXY_SLOTS", "1"))
except ValueError:
    threads = 1
assert 1 <= threads, threads

# Parse Command Line
usage = """Use as follows:

$ python find_and_extend.py [options] -q query.fasta -d draft_genome -o matches.fasta

There is additional guidance in the help text in the find_and_extend.xml
file, which is shown to the user via the Galaxy interface to this tool.
"""

parser = OptionParser(usage=usage)
parser.add_option("-q", "--query", dest="query",
                  default=None, metavar="FILE",
                  help="Input query FASTA filename (required)")
parser.add_option("-d", "--database", dest="database",
                  default=None, metavar="FILE",
                  help="Input BLAST nucleotide database (required)")
parser.add_option("-o", "--output", dest="output",
                  default=None, metavar="FILE",
                  help="Output FASTA filename (required)")
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

if args:
    sys.exit("No positional arguments expected.")

if not os.path.isfile(options.query):
    sys.exit("Missing input query FASTA file: %r" % options.query)
query_file = options.query

if not options.output:
    sys.exit("Output filename required, e.g. -o matches.fasta")
out_file = options.output

try:
    min_identity = float(options.min_identity)
except ValueError:
    sys.exit("Expected number between 0 and 100 for minimum identity, not %r" % min_identity)
if not (0 <= min_identity <= 100):
    sys.exit("Expected minimum identity between 0 and 100, not %0.2f" % min_identity)

try:
    min_coverage = float(options.min_coverage)
except ValueError:
    sys.exit("Expected number between 0 and 100 for minimum coverage, not %r" % min_coverage)
if not (0 <= min_coverage <= 100):
    sys.exit("Expected minimum coverage between 0 and 100, not %0.2f" % min_coverage)

try:
    max_target_seqs = int(options.max_target_seqs)
except ValueError:
    sys.exit("Expected positive integer for maximum matches (max_target_seqs), not %r" % max_target_seqs)
if max_target_seqs < 0:
    sys.exit("Expected positive integer for maximum matches (max_target_seqs), not %r" % max_target_seqs)

try:
    up_extend = int(options.up)
except ValueError:
    sys.exit("Expected positive or zero integer for number of bases to extend upstream, not %r" % options.up)
if up_extend < 0:
    sys.exit("Expected positive or zero integer for number of bases to extend upstream, not %r" % up_extend)

try:
    down_extend = int(options.down)
except ValueError:
    sys.exit("Expected positive or zero integer for number bases to extend downstream, not %r" % options.down)
if down_extend < 0:
    sys.exit("Expected positive or zero integer for number bases to extend downstream, not %r" % down_extend)

try:
    threads = int(options.threads)
except ValueError:
    sys.exit("Expected positive integer for number of threads, not %r" % options.threads)
if threads < 1:
    sys.exit("Expected positive integer for number of threads, not %r" % threads)

# TODO

cols = "qseqid sseqid bitscore pident qcovhsp qlen length"  # Or qcovs?
c_query = 0
c_match = 1
c_score = 2
c_identity = 3
c_coverage = 4
c_qlen = 5
c_length = 6

tie_warning = 0


def best_hits(blast_tabular, ignore_self=False):
    """Iterate over BLAST tabular output, returns best hits as 2-tuples.

    Each return value is (query name, tuple of value for the best hit).

    Tied best hits to different sequences are NOT returned.

    One hit is returned for tied best hits to the same sequence
    (e.g. repeated domains).
    """
    global tie_warning
    current = None
    best_score = None
    best = None
    col_count = len(cols.split())
    with open(blast_tabular) as h:
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
            a = parts[c_query]
            b = parts[c_match]
            if ignore_self and a == b:
                continue
            score = float(parts[c_score])
            qlen = int(parts[c_qlen])
            length = int(parts[c_length])
            # print("Considering hit for %s to %s with score %s..." % (a, b, score))
            if current is None:
                # First hit
                assert best is None
                assert best_score is None
                best = dict()
                # Now append this hit...
            elif a != current:
                # New hit
                if len(best) == 1:
                    # Unambiguous (no tied matches)
                    yield current, list(best.values())[0]
                else:
                    # print("%s has %i equally good hits: %s" % (a, len(best), ", ".join(best)))
                    tie_warning += 1
                best = dict()
                # Now append this hit...
            elif score < best_score:
                # print("No improvement for %s, %s < %s" % (a, score, best_score))
                continue
            elif score > best_score:
                # This is better, discard old best
                best = dict()
                # Now append this hit...
            else:
                # print("Tied best hits for %s" % a)
                assert best_score == score
                # Now append this hit...
            current = a
            best_score = score
            # This will collapse two equally good hits to the same target (e.g. duplicated domain)
            best[b] = (b, score, parts[c_score], parts[c_identity], parts[c_coverage], qlen, length)
    # Best hit for final query, if unambiguous:
    if current is not None:
        if len(best) == 1:
            yield current, list(best.values())[0]
        else:
            # print("%s has %i equally good hits: %s" % (a, len(best), ", ".join(best)))
            tie_warning += 1


def check_duplicate_ids(filename):
    """Check for duplicate identifiers in a FASTA file."""
    # Copied from tools/ncbi_blast_plus/check_no_duplicates.py
    # TODO - just use Biopython's FASTA parser?
    if not os.path.isfile(filename):
        sys.stderr.write("Missing FASTA file %r\n" % filename)
        sys.exit(2)
    identifiers = set()
    handle = open(filename)
    for line in handle:
        if line.startswith(">"):
            # The split will also take care of the new line character,
            # e.g. ">test\n" and ">test description here\n" both give "test"
            seq_id = line[1:].split(None, 1)[0]
            if seq_id in identifiers:
                handle.close()
                sys.stderr.write("Repeated identifiers, e.g. %r\n" % seq_id)
                sys.exit(3)
            identifiers.add(seq_id)
    handle.close()


def make_nr(input_fasta, output_fasta, sep=";"):
    """Make the sequences in a FASTA file non-redundant."""
    # TODO - seq-hash based to avoid loading everything into RAM?
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


# print("Starting...")
check_duplicate_ids(fasta_a)
if not self_comparison:
    check_duplicate_ids(fasta_b)

if options.nr:
    make_nr(fasta_a, tmp_a)
    if not self_comparison:
        make_nr(fasta_b, tmp_b)
    fasta_a = tmp_a
    fasta_b = tmp_b

# TODO - Report log in case of error?
run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"' % (makeblastdb_exe, dbtype, fasta_a, db_a, log))
if not self_comparison:
    run('%s -dbtype %s -in "%s" -out "%s" -logfile "%s"' % (makeblastdb_exe, dbtype, fasta_b, db_b, log))
# print("BLAST databases prepared.")
run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
    % (blast_cmd, fasta_a, db_b, a_vs_b, cols, threads))
# print("BLAST species A vs species B done.")
if not self_comparison:
    run('%s -query "%s" -db "%s" -out "%s" -outfmt "6 %s" -num_threads %i'
        % (blast_cmd, fasta_b, db_a, b_vs_a, cols, threads))
    # print("BLAST species B vs species A done.")


best_b_vs_a = dict(best_hits(b_vs_a, self_comparison))


count = 0
outfile = open(out_file, 'w')
outfile.write("#A_id\tB_id\tA_length\tB_length\tA_qcovhsp\tB_qcovhsp\tlength\tpident\tbitscore\n")
for a, (b, a_score_float, a_score_str,
        a_identity_str, a_coverage_str, a_qlen, a_length) in best_hits(a_vs_b, self_comparison):
    if b not in best_b_vs_a:
        # Match b has no best hit
        continue
    a2, b_score_float, b_score_str, b_identity_str, b_coverage_str, b_qlen, b_length = best_b_vs_a[b]
    if a != a2:
        # Not an RBH
        continue
    # Start with IDs, lengths, coverage
    values = [a, b, a_qlen, b_qlen, a_coverage_str, b_coverage_str]
    # Alignment length was an integer so don't care about original string
    values.append(min(a_length, b_length))
    # Output the original string versions of the scores
    if float(a_identity_str) < float(b_identity_str):
        values.append(a_identity_str)
    else:
        values.append(b_identity_str)
    if a_score_float < b_score_float:
        values.append(a_score_str)
    else:
        values.append(b_score_str)
    outfile.write("%s\t%s\t%i\t%i\t%s\t%s\t%i\t%s\t%s\n" % tuple(values))
    count += 1
outfile.close()
print("Done, %i RBH found" % count)
if tie_warning:
    sys.stderr.write("Warning: Sequences with tied best hits found, you may have duplicates/clusters\n")

# Remove temp files...
shutil.rmtree(base_path)
